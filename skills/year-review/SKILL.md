---
name: year-review
description: Generates a visual year-in-review summary of Claude Code usage statistics. Shows activity heatmap, favorite model, token usage, session streaks, peak hours, and fun comparisons. Use when users ask for "year in review", "usage stats", "my stats", "usage summary", or want to see their Claude Code activity patterns.
allowed-tools: Bash, Read
---

# Claude Code Year in Review

Generate a condensed, visual summary of the user's Claude Code usage statistics.

## Step 1: Gather Data

Run the Python script:

```bash
python3 ~/.claude/skills/year-review/year_review.py
```

## Step 2: Render the Visual Summary

**CRITICAL FORMATTING RULES:**

1. **NO RIGHT BORDERS** - Only use left/top/bottom borders
2. **Single column layout** - Never use side-by-side sections
3. **Fixed bar width** - All progress bars max 20 characters
4. **Simple ASCII borders** - Use `─` for horizontal lines only
5. **Consistent spacing** - 2 spaces after emoji, align values

### Template (follow exactly):

```
╔══════════════════════════════════════════════════╗
║       🎊 CLAUDE CODE · YEAR IN REVIEW · 2025      ║
╚══════════════════════════════════════════════════╝

📅 [period_start] → [period_end] ([X] days)

─── 📊 OVERVIEW ───────────────────────────────────
Sessions: [X]    Prompts: [X]    Tool Calls: [X]
Output Tokens: [X]M    Projects: [X]
Favorite Model: [model_name]

─── ✍️  CODE IMPACT ────────────────────────────────
Lines Added:    +[X]     ████████████████████
Lines Removed:  -[X]     ████████████
Net Change:     +[X]     ████

Files Created: [X]    Files Edited: [X]

─── 💻 TECH STACK ─────────────────────────────────
[Lang1]      ████████████████████  [X]%
[Lang2]      ████████████          [X]%
[Lang3]      ████                  [X]%

─── 🔧 TOP TOOLS ──────────────────────────────────
Bash         ████████████████████  [X]
Read         ████████████████      [X]
Edit         ████████████          [X]
Write        ████████              [X]

─── ⚡ PRODUCTIVITY ───────────────────────────────
🔥 Busiest Day:    [date] ([X] messages)
🦉 Peak Hours:     [X]:00 - [Y]:00
📅 Power Day:      [weekday] ([X] prompts)
📈 Avg Prompts/Day: [X]

Weekly Rhythm:
Mon ██░░░░░░░░░░░░░░░░░░  [X]
Tue ████░░░░░░░░░░░░░░░░  [X]
Wed █████░░░░░░░░░░░░░░░  [X]
Thu ███████░░░░░░░░░░░░░  [X]
Fri █████████░░░░░░░░░░░  [X]
Sat ███████████░░░░░░░░░  [X]
Sun ████████████████████  [X]

─── 🏆 YOUR TITLE ─────────────────────────────────

        🦉 [TITLE IN CAPS] 🦉
     "[Tagline based on patterns]"

─── 💡 AI INSIGHTS ────────────────────────────────

[3-4 bullet points with emojis analyzing:]
- Time patterns (night owl, weekend warrior, etc.)
- Tech focus (full-stack, backend, data science, etc.)
- Tool preferences (automation-heavy, reading-heavy, etc.)
- Work style (debugging, greenfield, refactoring, etc.)

─── 🎯 2025 HIGHLIGHT REEL ────────────────────────

• [Inferred project/achievement 1]
• [Inferred project/achievement 2]
• [Inferred project/achievement 3]

──────────────────────────────────────────────────
        Thanks for coding with Claude! 🚀
```

## Bar Rendering Rules

Progress bars must be EXACTLY 20 characters wide:
- Use `█` (U+2588) for filled portions
- Use `░` (U+2591) for empty portions
- Calculate: `filled = int((value / max_value) * 20)`

Examples:
- 100%: `████████████████████`
- 50%:  `██████████░░░░░░░░░░`
- 25%:  `█████░░░░░░░░░░░░░░░`

## Coder Title & Insights

**Be creative!** Generate a unique, personalized title and tagline based on the user's actual patterns. Don't use a hardcoded list - analyze the data and craft something that feels specific to them.

Consider patterns like:
- Time of day (peak_hours, hour_distribution)
- Day preferences (weekday_distribution)
- Language mix (languages, file_types)
- Tool preferences (tools - Bash heavy? Read heavy?)
- Work style (prompts_with_errors, top_words like "fix", "implement", "refactor")
- Scale (total tokens, lines changed, sessions)

The title should feel earned and specific, not generic. A developer who codes at 2 AM in Python building automation scripts deserves a different title than someone who refactors TypeScript on Sunday afternoons.

## Tech Stack Interpretation

The script outputs both:
- `languages`: Grouped by language (Python, TypeScript, etc.)
- `file_types`: Raw extensions (.py, .tsx, .svelte, etc.)

Use your knowledge to interpret what these mean:
- `.prisma` → Database schemas, likely using Prisma ORM
- `.tsx` + `.ts` → React/Next.js TypeScript project
- `.ipynb` → Data science / Jupyter notebooks
- `.tf` → Infrastructure as Code with Terraform

Don't just list languages - infer what they're building.

## Important Guidelines

1. **Privacy**: Never show project names or prompt content
2. **Single column**: All sections stack vertically
3. **No right borders**: Hardest to align, provides little value
4. **Be concise**: Target one screen (40-50 lines max)
5. **Make it personal**: Use sample_prompts to infer what they built (generalized)
