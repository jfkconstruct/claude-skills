# Claude Code Skills for People Who Build with AI Agents

Six skills extracted from a working solo-builder harness. Five ran for months in daily use before publishing; release-gate is the newest, published the day its harness counterpart shipped.

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
| **ui-audit** | UI/UX audit: locate the failure in the causal chain, score 0-5, bounce on a hard ship gate. Ships with its pattern library (`ui-patterns.md`) | When shipping a screen or component |
| **self-critique** | Structured critique pass on any draft, document, or skill: find the weakest claim, fix it, repeat | Before finalizing work |
| **ship-learn-next** | Turn a tutorial, transcript, or article into a ship-first plan of concrete reps | When you finish learning material |
| **session-story** | Extract session stories and structural decisions from build transcripts | End of session |
| **gif-loop-capture** | Turn a local HTML page or animation into an animated webp or mp4 loop with Playwright | When sharing results |
| **release-gate** | Deterministic grounding check between "the agent says done" and "it ships": every date, id, URL, hash in the output must appear in the evidence, else a fallback ships. Ships with `release_gate.py` and its tests | Before releasing any model-written brief, PR description, or report unread |

## How they were made

These skills came from working code. Each one solved a specific problem in the harness before being published. Read the SKILL.md file in each folder for full context, process, and examples.

## License

MIT. Copyright 2026 jfkconstruct.
