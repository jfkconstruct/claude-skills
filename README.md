# Claude Code Skills for People Who Build with AI Agents

Five skills extracted from a working solo-builder harness. Each ran for months in daily use before publishing.

## Install

**Option A: Via Claude Code plugin marketplace**
```
/plugin marketplace add jfkconstruct/claude-skills
/plugin install build-skills@jfkconstruct-skills
```

**Option B: Copy to your skills directory**
Copy any folder from `skills/` into `.claude/skills/`

## Skills

| Skill | What it does | Trigger |
|-------|-------------|---------|
| **ui-audit** | Comprehensive UI/UX audit with hard ship gates, scoring framework, and actionable recommendations | When shipping a screen or component |
| **ui-patterns** | Pattern library, screen-type requirements, and disclosure rules | Loaded before ui-audit |
| **self-critique** | Structured critique pass on any draft, document, or skill: find the weakest claim, fix it, repeat | Before finalizing work |
| **ship-learn-next** | Turn a tutorial, transcript, or article into a ship-first plan of concrete reps | When you finish learning material |
| **session-story** | Extract session stories and structural decisions from build transcripts | End of session |
| **gif-loop-capture** | Turn a local HTML page or animation into an animated webp or mp4 loop with Playwright | When sharing results |

## How they were made

These skills came from working code. Each one solved a specific problem in the harness before being published. Read the SKILL.md file in each folder for full context, process, and examples.

## License

MIT. Copyright 2026 jfkconstruct.
