#!/usr/bin/env python3
"""
Claude Code Year in Review - Data Extraction
Extracts raw usage data for LLM-powered analysis.

Design principles:
- No hardcoded categorization - let LLM analyze semantically
- Use file extensions as reliable tech signal
- Provide raw data, not pre-interpreted insights

Data sources:
- ~/.claude/stats-cache.json (v2.0.64+)
- ~/.claude/history.jsonl
- ~/.claude/projects/*/*.jsonl
"""

import json
import sys
import logging
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# File extension to language mapping
# Design decision: Static dict vs Pygments/linguist library
# - Pygments: 500+ languages but requires `pip install pygments`
# - linguist: GitHub's data but requires network or large embedded file
# - Static dict: Zero dependencies, works offline, sufficient for grouping
#
# The script outputs BOTH 'languages' (grouped) AND 'file_types' (raw extensions)
# so Claude can interpret unknown extensions using its knowledge.
# To extend: just add entries below, or let Claude handle unknown extensions.
EXTENSION_TO_LANG = {
    # Web
    'js': 'JavaScript', 'jsx': 'JavaScript', 'mjs': 'JavaScript', 'cjs': 'JavaScript',
    'ts': 'TypeScript', 'tsx': 'TypeScript', 'mts': 'TypeScript',
    'vue': 'Vue', 'svelte': 'Svelte',
    'html': 'HTML', 'htm': 'HTML',
    'css': 'CSS', 'scss': 'SCSS', 'sass': 'Sass', 'less': 'Less',
    # Systems
    'py': 'Python', 'pyi': 'Python', 'pyx': 'Python',
    'rs': 'Rust',
    'go': 'Go',
    'c': 'C', 'h': 'C',
    'cpp': 'C++', 'cc': 'C++', 'cxx': 'C++', 'hpp': 'C++',
    'java': 'Java',
    'kt': 'Kotlin', 'kts': 'Kotlin',
    'swift': 'Swift',
    'rb': 'Ruby', 'erb': 'Ruby',
    'php': 'PHP',
    'cs': 'C#',
    'fs': 'F#', 'fsx': 'F#',
    'scala': 'Scala',
    'clj': 'Clojure', 'cljs': 'ClojureScript',
    'ex': 'Elixir', 'exs': 'Elixir',
    'erl': 'Erlang',
    'hs': 'Haskell',
    'ml': 'OCaml',
    'lua': 'Lua',
    'r': 'R',
    'jl': 'Julia',
    'zig': 'Zig',
    'nim': 'Nim',
    'dart': 'Dart',
    # Shell/Scripts
    'sh': 'Shell', 'bash': 'Shell', 'zsh': 'Shell',
    'ps1': 'PowerShell',
    # Data/Config
    'json': 'JSON', 'yaml': 'YAML', 'yml': 'YAML', 'toml': 'TOML',
    'xml': 'XML', 'graphql': 'GraphQL', 'gql': 'GraphQL',
    'sql': 'SQL',
    'prisma': 'Prisma',
    # Docs
    'md': 'Markdown', 'mdx': 'MDX', 'rst': 'reStructuredText',
    # Mobile
    'm': 'Objective-C', 'mm': 'Objective-C++',
    # Other
    'sol': 'Solidity', 'move': 'Move',
    'tf': 'Terraform', 'hcl': 'HCL',
    'dockerfile': 'Docker',
    'ipynb': 'Jupyter',
}


def load_data() -> tuple[dict, list[dict], list[dict]]:
    """Load all Claude Code data."""
    claude_dir = Path.home() / '.claude'

    # Stats cache
    stats: dict[str, Any] = {}
    stats_path = claude_dir / 'stats-cache.json'
    if stats_path.exists():
        try:
            with open(stats_path, encoding='utf-8') as f:
                stats = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load stats-cache.json: {e}")

    # History
    history: list[dict] = []
    history_path = claude_dir / 'history.jsonl'
    if history_path.exists():
        try:
            with open(history_path, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            history.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except IOError as e:
            logger.warning(f"Failed to read history.jsonl: {e}")

    # Session files
    sessions_data: list[dict] = []
    projects_dir = claude_dir / 'projects'
    if projects_dir.exists():
        for proj_dir in projects_dir.iterdir():
            if not proj_dir.is_dir() or proj_dir.name.startswith('.'):
                continue
            for session_file in proj_dir.glob('*.jsonl'):
                try:
                    with open(session_file, encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    sessions_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    continue
                except IOError:
                    continue

    return stats, history, sessions_data


def analyze_tools_and_files(sessions_data: list[dict]) -> dict:
    """Extract tool usage, file types, and code changes."""
    tool_counts: Counter = Counter()
    file_extensions: Counter = Counter()
    languages: Counter = Counter()
    lines_added = 0
    lines_removed = 0
    files_created = 0
    files_edited = 0

    for item in sessions_data:
        msg = item.get('message', {})
        if not isinstance(msg, dict):
            continue

        content = msg.get('content', [])
        if not isinstance(content, list):
            continue

        for block in content:
            if not isinstance(block, dict):
                continue

            if block.get('type') == 'tool_use':
                tool_name = block.get('name', 'unknown')
                tool_counts[tool_name] += 1

                inp = block.get('input', {})
                if not isinstance(inp, dict):
                    continue

                if tool_name in ('Edit', 'Write'):
                    file_path = inp.get('file_path', '')
                    if file_path:
                        # Extract extension
                        filename = file_path.split('/')[-1]
                        if '.' in filename:
                            ext = filename.rsplit('.', 1)[-1].lower()
                            if len(ext) <= 12 and ext.isalnum():
                                file_extensions[ext] += 1
                                # Map to language
                                lang = EXTENSION_TO_LANG.get(ext)
                                if lang:
                                    languages[lang] += 1

                        if tool_name == 'Write':
                            files_created += 1
                        else:
                            files_edited += 1

        # Line changes from structuredPatch
        tool_result = item.get('toolUseResult', {})
        if isinstance(tool_result, dict):
            patches = tool_result.get('structuredPatch', [])
            if isinstance(patches, list):
                for patch in patches:
                    if isinstance(patch, dict):
                        lines = patch.get('lines', [])
                        if isinstance(lines, list):
                            for line in lines:
                                if isinstance(line, str):
                                    if line.startswith('+') and not line.startswith('+++'):
                                        lines_added += 1
                                    elif line.startswith('-') and not line.startswith('---'):
                                        lines_removed += 1

    return {
        'tool_usage': dict(tool_counts.most_common(20)),
        'file_extensions': dict(file_extensions.most_common(15)),
        'languages_from_files': dict(languages.most_common(15)),
        'total_tool_calls': sum(tool_counts.values()),
        'lines_added': lines_added,
        'lines_removed': lines_removed,
        'lines_changed': lines_added + lines_removed,
        'files_created': files_created,
        'files_edited': files_edited,
    }


def analyze_prompts(history: list[dict]) -> dict:
    """Extract prompt statistics (no hardcoded categorization)."""
    prompt_lengths: list[int] = []
    project_count: Counter = Counter()
    prompts_with_code_blocks = 0
    prompts_with_errors = 0

    # Collect word frequency for LLM analysis (top action words)
    action_words: Counter = Counter()
    error_indicators = {'error', 'fail', 'bug', 'issue', 'broken', 'crash', 'exception', 'not working'}

    for item in history:
        prompt = item.get('display', '')
        if not prompt:
            continue

        prompt_lower = prompt.lower()
        prompt_lengths.append(len(prompt))

        project = item.get('project', '')
        if project:
            project_count[project.split('/')[-1]] += 1

        if '```' in prompt:
            prompts_with_code_blocks += 1

        if any(kw in prompt_lower for kw in error_indicators):
            prompts_with_errors += 1

        # Extract first few words (likely action/intent)
        words = prompt_lower.split()[:5]
        for word in words:
            # Filter to actionable words
            if len(word) > 2 and word.isalpha():
                action_words[word] += 1

    return {
        'total_prompts': len(history),
        'avg_prompt_length': round(sum(prompt_lengths) / len(prompt_lengths)) if prompt_lengths else 0,
        'prompts_with_code_blocks': prompts_with_code_blocks,
        'prompts_with_errors': prompts_with_errors,
        'project_count': len(project_count),
        'top_action_words': dict(action_words.most_common(30)),
    }


def calculate_time_patterns(stats: dict, history: list[dict]) -> dict:
    """Calculate when the user codes."""
    daily_activity = stats.get('dailyActivity', [])

    # Busiest day
    busiest = max(daily_activity, key=lambda x: x.get('messageCount', 0)) if daily_activity else {}

    weekday_counts: Counter = Counter()
    hour_counts: Counter = Counter()

    for item in history:
        ts = item.get('timestamp', 0)
        if ts:
            try:
                dt = datetime.fromtimestamp(ts / 1000)
                weekday_counts[dt.strftime('%A')] += 1
                hour_counts[dt.hour] += 1
            except (ValueError, OSError):
                continue

    # Find peak hours
    peak_hours = hour_counts.most_common(3)

    # Longest session
    longest = stats.get('longestSession', {})
    dur_ms = longest.get('duration', 0)

    return {
        'busiest_day_date': busiest.get('date', 'N/A'),
        'busiest_day_messages': busiest.get('messageCount', 0),
        'weekday_distribution': dict(weekday_counts),
        'hour_distribution': dict(hour_counts),
        'peak_hours': [(h, c) for h, c in peak_hours],
        'longest_session_hours': round(dur_ms / (1000 * 60 * 60), 1) if dur_ms else 0,
        'longest_session_messages': longest.get('messageCount', 0),
    }


def get_sample_prompts(history: list[dict], n: int = 20) -> list[str]:
    """Get diverse sample prompts for LLM to analyze semantically."""
    good_prompts: list[str] = []
    sensitive_keywords = {'password', 'secret', 'api_key', 'apikey', 'token', 'credential', 'private_key'}

    for item in history:
        prompt = item.get('display', '')
        prompt_lower = prompt.lower()

        # Filter criteria
        if (len(prompt) > 40 and
            '[Pasted text' not in prompt and
            '[Image' not in prompt and
            not any(kw in prompt_lower for kw in sensitive_keywords)):
            good_prompts.append(prompt[:200])

    if len(good_prompts) <= n:
        return good_prompts

    # Sample evenly across timeline
    step = len(good_prompts) // n
    return [good_prompts[i * step] for i in range(n)]


def main() -> int:
    """Main entry point."""
    stats, history, sessions_data = load_data()

    if not history and not stats:
        print(json.dumps({
            "error": "No Claude Code data found.",
            "hint": "Make sure you've used Claude Code (v2.0.64+) and run /stats at least once."
        }, indent=2))
        return 1

    # Gather analyses
    tool_analysis = analyze_tools_and_files(sessions_data)
    prompt_stats = analyze_prompts(history)
    time_patterns = calculate_time_patterns(stats, history)
    sample_prompts = get_sample_prompts(history, 20)

    # Model usage from stats cache
    model_usage = stats.get('modelUsage', {})
    models_breakdown = {}
    for model, data in model_usage.items():
        clean_name = (model
            .replace('claude-', '')
            .replace('-20251101', '')
            .replace('-20250929', '')
            .replace('-20250805', ''))
        models_breakdown[clean_name] = {
            'output_tokens': data.get('outputTokens', 0),
            'input_tokens': data.get('inputTokens', 0),
        }

    total_output = sum(m.get('outputTokens', 0) for m in model_usage.values())
    favorite_model = max(models_breakdown.items(), key=lambda x: x[1]['output_tokens'])[0] if models_breakdown else 'Unknown'

    first_date = stats.get('firstSessionDate', '')[:10] if stats.get('firstSessionDate') else 'Unknown'

    # Compile report - raw data for LLM to interpret
    report = {
        'meta': {
            'generated_at': datetime.now().isoformat(),
            'period_start': first_date,
            'period_end': datetime.now().strftime('%Y-%m-%d'),
            'data_note': 'Stats tracking started in Claude Code v2.0.64. Data may not cover full usage history.',
        },
        'summary': {
            'total_sessions': stats.get('totalSessions', 0),
            'total_prompts': prompt_stats['total_prompts'],
            'total_tool_calls': tool_analysis['total_tool_calls'],
            'total_output_tokens': total_output,
            'favorite_model': favorite_model,
            'projects_worked_on': prompt_stats['project_count'],
        },
        'code_changes': {
            'lines_added': tool_analysis['lines_added'],
            'lines_removed': tool_analysis['lines_removed'],
            'net_lines': tool_analysis['lines_added'] - tool_analysis['lines_removed'],
            'files_created': tool_analysis['files_created'],
            'files_edited': tool_analysis['files_edited'],
        },
        'languages': tool_analysis['languages_from_files'],
        'file_types': tool_analysis['file_extensions'],
        'tools': tool_analysis['tool_usage'],
        'models': models_breakdown,
        'time_patterns': time_patterns,
        'prompt_stats': {
            'avg_length_chars': prompt_stats['avg_prompt_length'],
            'with_code_blocks': prompt_stats['prompts_with_code_blocks'],
            'with_errors': prompt_stats['prompts_with_errors'],
            'top_words': prompt_stats['top_action_words'],
        },
        'sample_prompts': sample_prompts,
    }

    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
