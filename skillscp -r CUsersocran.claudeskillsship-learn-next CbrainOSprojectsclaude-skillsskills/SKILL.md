---
name: self-critique
description: "Systematically critique and improve any output, document, or skill. Use when: reviewing your own work, improving a draft, stress-testing a framework, or iterating on anything that needs to be better. Triggers: 'critique this', 'what's wrong with this', 'how can I improve this', 'review my work', 'iterate on this'."
---

# Self-Critique

## The Loop

```
IDENTIFY → RANK → SPECIFY → VALIDATE → (repeat if needed)
```

Each phase has specific cognitive moves. Don't skip phases.

---

## Phase 1: IDENTIFY (What's wrong?)

**Goal:** Surface all issues without filtering.

**Cognitive Moves:**

1. **HOW vs WHAT check**
   - Does this tell someone HOW to do it, or just WHAT to do?
   - Can a novice execute this? If not, it's too abstract.

2. **Weakest-link scan**
   - Which section is weakest relative to its importance?
   - Where does quality drop off?

3. **Absence check**
   - What's obviously missing?
   - What question would a skeptic ask that isn't answered?

4. **Friction test**
   - Where would someone get stuck trying to use this?
   - What requires re-reading to understand?

5. **Bloat check**
   - What could be cut without losing value?
   - What's there to sound smart vs. to be useful?

**Output:** Raw list of all issues found. No filtering yet.

---

## Phase 2: RANK (Pareto filter)

**Goal:** Ruthlessly prioritize. Most issues don't matter.

**The Pareto Question:**
> "If I could only fix ONE thing, which creates the most value?"

**Cognitive Moves:**

1. **Impact sort**
   - High impact + easy fix → Do first
   - High impact + hard fix → Do second
   - Low impact → Probably skip

2. **Kill the perfectionism**
   - What's a "nice to have" disguised as important?
   - What am I fixing for me vs. for the user?

3. **Dependency check**
   - Does fixing X automatically fix Y?
   - What's the root issue vs. symptoms?

**Decision Rule:** Identify the 2-3 changes that create 80% of the improvement. Everything else is polish.

**Output:** Prioritized short list (max 3-5 items).

---

## Phase 3: SPECIFY (Make it concrete)

**Goal:** Turn vague critiques into specific fixes.

**Cognitive Moves:**

1. **Write the fix, not the problem**
   - Bad: "This section is unclear"
   - Good: "Replace paragraph 2 with: [exact new text]"

2. **Additive vs. Subtractive**
   - Am I adding something missing, or removing something harmful?
   - Subtractive fixes are often higher leverage

3. **Time-box test**
   - Can I implement this fix in <5 minutes?
   - If not, break it down further

4. **Show the delta**
   - Before: [what it says now]
   - After: [what it should say]

**Output:** Specific, actionable fixes with concrete language.

---

## Phase 4: VALIDATE (Did it work?)

**Goal:** Confirm improvement, catch regressions.

**Cognitive Moves:**

1. **The use test**
   - Would I actually use this improved version?
   - Does it solve the problem better?

2. **Complexity check**
   - Did I make it more complex or more useful?
   - Complexity without value = regression

3. **Fresh eyes pass**
   - Read from the beginning as if first time
   - What's still confusing?

4. **Completion test**
   - What's still missing after fixes?
   - Is another loop needed, or is this good enough?

**Decision Rule:** Stop when additional iteration yields diminishing returns. "Good enough to ship" beats "perfect but stuck."

**Output:** Go/no-go decision. Either ship it or run another loop.

---

## Anti-Patterns

**Critique theater:**
Listing issues to look thorough without prioritizing. 20 minor issues ≠ useful critique.

**Perfectionism spiral:**
Running infinite loops. Know when to stop.

**Vague complaints:**
"This could be better" without specifying how. Not actionable = not useful.

**Scope creep:**
Critique becomes redesign. Stay focused on improving THIS thing, not building something new.

**Critique without creation:**
Tearing down without building up. Always pair problems with solutions.

---

## When to Use Each Phase

| Situation | Start At |
|-----------|----------|
| First draft review | Phase 1 (full scan) |
| Quick polish | Phase 3 (already know what's wrong) |
| Major revision | Phase 1 → full loop |
| Final check | Phase 4 only |

---

## Integration

This skill pairs with:
- **idea-expander** → Expand first, then critique
- **flowcraft** → Critique catches what flowcraft polishes
- Any output that needs iteration before shipping

---

## Example Application

**Input:** A skill document that tells WHAT to do but not HOW.

**IDENTIFY:**
- Modes are descriptive, not procedural
- No cognitive moves, just labels
- CHALLENGE section is weak relative to importance
- Missing INVERT mode

**RANK:**
1. Add cognitive HOW (highest impact)
2. Strengthen CHALLENGE (weak + important)
3. Add INVERT (easy + valuable)

**SPECIFY:**
1. For each mode, add "Cognitive Moves:" with 3-4 specific mental operations
2. Add attack checklist to CHALLENGE with concrete questions
3. Add INVERT mode with 4 cognitive moves, ~10 lines

**VALIDATE:**
- Each mode now executable by novice? ✓
- CHALLENGE has teeth? ✓
- INVERT adds value without bloat? ✓
- Ship it.
