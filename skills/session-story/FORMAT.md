# Story file format


```markdown
---
date: YYYY-MM-DD
slug: kebab-case-short
arc: one sentence, what changed in the world by session end
repos: ["<repo>@<hash>", "<other-repo>@<hash>"]
post-candidates: [which content pillar(s) this could feed: identity | capability | contribution]
status: raw
---

# <working title, a claim not a report>

## Hook
1-3 sentences. The tension that makes a stranger care. Not "we built X": what was hard, absurd, or newly possible.

## The world before
2-5 sentences. Starting state, the constraint that made this non-trivial, what existed already (so the delta is honest).

## Beats
Chronological. Each beat = intent -> action -> what actually happened. Surprises and dead ends inline, in order, with their real timestamps or sequence. This is the longest section. A beat that contains a failure keeps the error text or symptom verbatim.

## Wrong turns and gotchas
Each: what we believed, what was true, what it cost, the fix. Includes probe/tooling lies (things the checks said were fine but were not, or vice versa).

## Taste moments
the user's judgment, VERBATIM quotes, each with what it changed downstream. Corrections, vetoes, "I like this" moments, naming decisions. This section is the reason the file exists.

## The invariant
1-3 sentences. What transfers beyond this session. The compression, not a moral.

## Receipts
Bulleted: commits (repo + hash + one-liner), numbers with sources (sizes, counts, wall-clock, token spend), artifacts created (paths), anything screenshot-worthy and where it lives.

## Leftovers
Open threads, post angles noticed but not taken, follow-up builds this session made possible.
```

Section order is fixed. Empty sections are written as "None." rather than omitted (an empty Wrong turns section on a long session is a signal the extraction was lazy). Target length 60-150 lines; below 40 the beats are probably summarized, above 200 it is a transcript not a story.
