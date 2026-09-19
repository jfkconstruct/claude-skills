---
name: session-story
description: Extract a build session's story (narrative, problem-solving, wrong turns, the user's judgment calls, receipts) into blog-post source material at stories/. Use at the end of any substantive build session, when the user says "capture this session" or "story of what we did", or when mining an old transcript for a post. Raw material, never a drafted post.
---

# Session story extraction

Turn the session that just happened into durable source material for a blog post. This is UPSTREAM of drafting: a story file holds the narrative and the judgment, so a post can be written weeks later by a session that was not there.

FORMAT.md in this directory is the output format. Match its altitude: beats and receipts, not a summary.

## Procedure

0. Score first, write second: draft the full story into a scratch file, then gate it before it lands. It passes only if it has at least one wrong turn, at least one verbatim user quote, and a named invariant. A draft missing any of the three is low signal; stop at the source, do not file it.
1. Output path: `stories/YYYY-MM-DD-<slug>.md` (repo root). One file per story; a session with two unrelated arcs gets two files.
2. Fill every FORMAT.md section from the session in context. Running after the fact, mine the transcript or the git log for the receipts first, then write.
3. Hard rules:
   - **the user's words verbatim.** Their reactions, corrections, and one-liners are the judgment payload (a one-line reaction is worth more than any summary of it). Quote, don't polish.
   - **Failures stay in.** The wrong turn, the probe that lied, the cache that bit: the debugging IS the story. A story with no friction is a press release, bounce it.
   - **Numbers carry sources.** Commit hashes, file sizes, token counts, wall-clock. Unverifiable claims get cut, not hedged.
   - **Voice-neutral.** This is source material; the user's voice gets applied at drafting time (a later drafting pass). No em dashes even here.
   - **The invariant is required.** One to three sentences on what transfers beyond this session. If you cannot name one, say so explicitly; that is itself information.
4. Append one line to `stories/INDEX.md`: `- [date] <slug>: <one-line hook> (status: raw)`.
5. Commit the story file on its own, if the repo uses git: `process: session story <slug>`. Never sweep unrelated staged changes into it.

## Relationship to the judgment-extraction loop

The format encodes a compressed version of the user's recursive judgment extraction (experience -> externalize -> tension -> invariant -> compress -> codify): Beats = experience externalized, Taste moments = the judgment located, The invariant = the compression, this skill = the codify step. The full ChatGPT-authored articulation is inspo, not canon; do not import its prose into stories.

## Known gotchas

- Receipts survive a session; the hook, the wrong turns, the invariant, and the leftovers do not. Write them BEFORE clearing context, or they are gone.
- Prompting a model with texture targets (sentence-length mixes) produces a metronome; keep the prompt spec-only and edit a flat draft by hand.
