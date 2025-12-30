# Claude Code Year in Review

A Claude Code skill that generates a personalized year-in-review summary with AI-powered insights about your coding patterns.

## What is this?

This skill analyzes your local Claude Code usage data and generates a visual summary of:
- **Code Impact**: Lines added/removed, files created/edited
- **Tech Stack**: Languages detected from actual file edits
- **Tool Usage**: Which Claude Code tools you use most
- **Time Patterns**: When you code, your power days, peak hours
- **AI Insights**: Personalized observations about your workflow
- **Coder Title**: A creative title based on your unique patterns

## Why we built this

The built-in `/stats` command shows basic usage numbers, but we wanted something more:
- **Insightful**: Not just numbers, but what they mean about how you work
- **Visual**: Easy to scan, fun to share
- **Personal**: AI-generated insights that feel specific to you
- **Private**: 100% local - nothing leaves your machine

## Sample Output

```
╔══════════════════════════════════════════════════╗
║       🎊 CLAUDE CODE · YEAR IN REVIEW · 2025      ║
╚══════════════════════════════════════════════════╝

📅 2025-11-15 → 2025-12-30 (45 days)

─── 📊 OVERVIEW ───────────────────────────────────
Sessions: 35    Prompts: 1,258    Tool Calls: 3,528
Output Tokens: 1.3M    Projects: 14
Favorite Model: opus-4-5

─── ✍️  CODE IMPACT ────────────────────────────────
Lines Added:    +12,065  ████████████████████
Lines Removed:   -9,065  ███████████████░░░░░
Net Change:      +3,000  █████░░░░░░░░░░░░░░░

Files Created: 237    Files Edited: 396

─── 💻 TECH STACK ─────────────────────────────────
Python       ████████████████████  57%
TypeScript   ███████████░░░░░░░░░  33%
Jupyter      ██░░░░░░░░░░░░░░░░░░   1%

─── 🔧 TOP TOOLS ──────────────────────────────────
Bash         ████████████████████  1,061
Read         ████████████████░░░░    854
Edit         ████████░░░░░░░░░░░░    396
Write        █████░░░░░░░░░░░░░░░    237

─── ⚡ PRODUCTIVITY ───────────────────────────────
🔥 Busiest Day:    Dec 21 (3,258 messages!)
🦉 Peak Hours:     21:00 - 00:00
📅 Power Day:      Sunday (383 prompts)
📈 Avg Prompts/Day: 28

Weekly Rhythm:
Mon ███░░░░░░░░░░░░░░░░░   63
Tue █████░░░░░░░░░░░░░░░   93
Wed █████░░░░░░░░░░░░░░░  103
Thu ████████░░░░░░░░░░░░  154
Fri ███████████░░░░░░░░░  207
Sat █████████████░░░░░░░  255
Sun ████████████████████  383

─── 🏆 YOUR TITLE ─────────────────────────────────

        🦉 MIDNIGHT WORKFLOW ARCHITECT 🦉
    "Building automation empires while the world sleeps"

─── 💡 AI INSIGHTS ────────────────────────────────

• 🦉 True night owl - your peak creativity hits between
  9 PM and midnight, with momentum carrying past 1 AM
• 📅 Sunday is your power day - you code 6x more on
  Sundays than Mondays. Weekend = build time.
• ⚡ Automation obsessed - 1,061 Bash calls shows you
  love scripting your way through problems
• 🔄 Full-stack builder - Python backends + TypeScript
  frontends, you're shipping complete systems

─── 🎯 2025 HIGHLIGHT REEL ────────────────────────

• Built workflow automation systems
• Shipped full-stack web applications
• Created data processing pipelines
• Integrated browser automation for testing

──────────────────────────────────────────────────
        Thanks for coding with Claude! 🚀
```

## Installation

### Option 1: Plugin Marketplace (Recommended)

```bash
/plugin marketplace add lupuletic/claude-code-year-review
/plugin install year-review
```

### Option 2: Manual Install

```bash
mkdir -p ~/.claude/skills/year-review

curl -so ~/.claude/skills/year-review/SKILL.md \
  https://raw.githubusercontent.com/lupuletic/claude-code-year-review/main/plugins/year-review/skills/year-review/SKILL.md

curl -so ~/.claude/skills/year-review/year_review.py \
  https://raw.githubusercontent.com/lupuletic/claude-code-year-review/main/plugins/year-review/skills/year-review/year_review.py
```

## Usage

After installation, open Claude Code and ask:

- "Show my year in review"
- "What are my usage stats?"
- "Generate my Claude Code summary"

## Requirements

- Claude Code v2.0.64 or later
- Python 3.8+
- Run `/stats` at least once to populate the cache

## How It Works

The skill reads from local Claude Code data files:

| Source | Data |
|--------|------|
| `~/.claude/stats-cache.json` | Sessions, tokens, model usage |
| `~/.claude/history.jsonl` | Prompts, timestamps, projects |
| `~/.claude/projects/*/*.jsonl` | Tool calls, file edits, code changes |

A Python script extracts raw statistics as JSON. Claude then renders a visual summary and generates personalized insights based on your patterns.

## Limitations

- Stats tracking started in Claude Code v2.0.64 (~November 2025)
- Lines of code only tracked for Edit/Write tool operations

## License

MIT License

## Contributing

PRs welcome! Ideas:

- [ ] Historical comparisons (week-over-week trends)
- [ ] Export to image/PNG
- [ ] Framework detection (React, Django, etc.)
- [ ] More creative title variations
