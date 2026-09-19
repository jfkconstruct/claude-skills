---
name: ui-audit
description: Comprehensive UI/UX audit with hard ship gates, scoring framework, and actionable recommendations.
---

# UI/UX Audit

Perform a comprehensive UI/UX audit and generate actionable recommendations.

## Required Skills

Always load these skills before running an audit:
- `ui-patterns.md` - Pattern library, screen-type requirements, progressive disclosure definitions
- This file (heuristics, checklist, scoring)

The patterns skill provides the "what good looks like" reference. This skill provides the scoring framework. Both are needed for a complete audit.

## Process

1. **Load skills** - Read ui-patterns.md and ui-audit.md before starting
2. **Explore UI codebase** - Find SwiftUI views, React components, style files
3. **Match screen type** - Use Pattern Selection table from ui-patterns to identify required patterns
4. **Locate the failure, then score** - Walk the causal chain BEFORE any number: outcome, user model, mental model, findability, comprehension, affordance, accessibility, feedback, recovery, real-world result, verification. Name the first link that breaks; that is the finding. Then rate each screen/component 0-5. A score with no located cause is unactionable.
5. **Check pattern coverage** - Verify required patterns for the screen type are present
6. **Generate findings report** - Prioritized recommendations
7. **Categorize by effort** - Quick wins, medium effort, structural changes

## Heuristics (Score 0-5)

| Heuristic | Weight | Question |
|-----------|--------|----------|
| **Clarity** | 1.0 | Purpose obvious in 3 seconds? |
| **Cognitive Load** | 1.0 | How much mental effort required? |
| **Visual Hierarchy** | 1.0 | Important elements prominent? |
| **Feedback** | 0.8 | Confirms actions, communicates state? |
| **Responsive Scaling** | 1.1 | Feels native on all screen sizes without zoom? |
| **Accessibility** | 1.2 | Contrast, touch targets, usable by all? |
| **Conversion Strength** | 1.3 | How compelling is the CTA? |
| **Mental Model** | 1.0 | Can a first-time user predict what each thing does and where it lives, before clicking? |
| **AI Interaction** | 1.2 | For any AI capability: is the wrong-answer path designed (notice, inspect, correct, scope of correction, undo, human escalation)? Metric is appropriate reliance, never trust. Score N/A when the surface has no AI. |
| **Regression** | 1.0 | Does it hold up novice, expert, mobile, keyboard-only, screen reader, offline, interrupted mid-task, permission denied, and on a destructive action? |

## Ship gate (hard bounce)

Regardless of the weighted total, a critical flow scoring 0 or 1 on any of Accessibility, Feedback (state completeness), Clarity (action clarity), or Mental Model (problem fit) does not ship. Log the bounce with the failing heuristic and the causal-chain link from Process step 4.

## Checklist

**Clarity**
- [ ] Purpose obvious in 3 seconds
- [ ] Single primary action clear
- [ ] Labels unambiguous

**Hierarchy**
- [ ] Most important element largest/highest contrast
- [ ] Clear visual grouping
- [ ] Whitespace creating breathing room

**Feedback**
- [ ] Loading states for async
- [ ] Success confirmation for actions
- [ ] Error states with recovery path
- [ ] Web: INP <=200ms at p75 (200-500 needs work, >500 poor)

**State & Recovery**
- [ ] Input preserved on validation failure
- [ ] Every reversible action has undo; confirm only when irreversible, expensive, or security-sensitive
- [ ] Error copy says whether the user or system caused it and what to do next

**Mental Model**
- [ ] First-time user can predict what each control does before clicking
- [ ] Things live where a novice would look
- [ ] Naming matches the user's words, not engine terms

**AI Interaction (N/A if no AI)**
- [ ] Wrong answer is noticeable
- [ ] Source and evidence inspectable
- [ ] Correction possible
- [ ] Scope of a correction is stated
- [ ] Undo exists
- [ ] Human escalation path exists

**Regression**
- [ ] Novice, expert, mobile, keyboard-only, screen reader, offline, interrupted mid-task, permission denied, destructive action each walked once

**Responsive Scaling**
- [ ] Root font-size uses `clamp()` or responsive scaling (not fixed 16px)
- [ ] No `text-xs` (12px) for body content; minimum readable size is `text-sm` (14px)
- [ ] Tailwind breakpoint prefixes (`md:`, `lg:`, `xl:`) used for text and spacing on key elements
- [ ] Layout dimensions use viewport-relative units (`vw`, `vh`, `dvh`) or fluid values, not fixed px
- [ ] `clamp()`, `min()`, or `max()` used for fluid spacing/sizing where appropriate
- [ ] UI feels native at 1440px (laptop), 1920px (monitor), and 375px (mobile) without zoom

**Mobile**
- [ ] Touch targets >=44px iOS, 48dp Android (~48px at 1x); WCAG 2.2 target size AA 24x24 CSS px minimum, AAA 44x44
- [ ] Thumb-reachable primary actions
- [ ] No horizontal scroll
- [ ] Input font-size >=16px

**Accessibility**
- [ ] Color contrast >=4.5:1
- [ ] Doesn't rely on color alone
- [ ] Proper heading structure
- [ ] Text resizes to 200% without loss of content or function
- [ ] Line length 45-75 characters for body text

## Priority Ranking

- **P1**: Highest visual impact, quick to implement
- **P2**: Supporting elements, moderate effort
- **P3**: Polish items, nice-to-have

## Output Format

```markdown
## UI/UX Audit Report

### Overall Score: X/5

### Findings by Component

| Component | Score | Issues | Recommendations |
|-----------|-------|--------|-----------------|
| MainView  | 3.5   | Labels ambiguous | Add value hints |

### Quick Wins
1. [ ] Issue → Fix

### Medium Effort
1. [ ] Issue → Fix

### Structural Changes
1. [ ] Issue → Fix
```
