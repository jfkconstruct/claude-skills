# UI/UX Patterns Library

Reference for building apps that feel premium. Based on analysis of 100+ leading applications.

## Heuristics Framework

Score every screen 0-5:

| Heuristic | Weight | Question |
|-----------|--------|----------|
| **Clarity** | 1.0 | Can users immediately understand the purpose and next step? |
| **Cognitive Load** | 1.0 | How much mental effort is required? (Higher = lower load) |
| **Visual Hierarchy** | 1.0 | Are important elements visually prominent? |
| **Feedback** | 0.8 | Does UI confirm actions and communicate state? |
| **Accessibility** | 1.2 | Is it usable for everyone? (contrast, targets, etc.) |
| **Conversion Strength** | 1.3 | How compelling is the CTA presentation? |

- **Grayscale hierarchy pass:** review the screen with color removed; two reviewers must agree on the first, second, and third attention target. Judgment, not a scan.

---

## Pattern Categories

### Onboarding
| Pattern | When to Use |
|---------|-------------|
| Progress Indicator | Multi-step forms, wizards |
| Benefit-Oriented Headline | Value prop screens, landing pages |
| Hero Illustration | Welcome screens, empty states |
| Progressive Disclosure | Complex features, settings |
| Social Proof | Trust-building moments, paywalls |
| Onboarding Checklist | Post-signup activation |

### Navigation
| Pattern | When to Use |
|---------|-------------|
| Bottom Tab Bar (3-5) | Mobile apps with distinct sections |
| Bottom Tab + More Panel | 6+ nav items on mobile |
| Hamburger Menu | Desktop, settings, less-used features |
| Breadcrumbs | Deep hierarchies, admin panels |
| Command Palette | Power users, productivity apps |
| Floating Action Button | Single primary action per screen |

- **Navigation role separation:** tab bars hold destinations only; toolbars hold actions on the current context; menus hold secondary actions. A destination in a toolbar or an action in a tab bar is a finding.
- **Window-class adaptive rule:** design compact, medium, and expanded compositions; navigation transforms across them (tabs to rail to multi-pane). Distinct from the safe-area section below.

**Nav labels are predictable before the click.** Generic nouns a stranger can decode (Work, Writing, About), never private names (a product, a series, a "lab"). Private names go inside a section, not on its door; the hero teaches them. Same rule one level down: every card, link, and page title reads what it is, why you should care, then its name (`<plain descriptor> [outcome] · <Name>`); the name is the last word, never the first. Test: cover the site and ask what is behind each label. One content type per section: writing in one place, products in one place, no matter how many source sites got merged.

### Forms
| Pattern | When to Use |
|---------|-------------|
| Inline Validation | All forms with validation |
| Smart Defaults | Returning users, location-based |
| Input Masking | Phone, credit card, dates |
| Multi-Step Form | Long forms (>5 fields) |
| Error Summary | Complex forms, accessibility |

### Content
| Pattern | When to Use |
|---------|-------------|
| Infinite Scroll | Feeds, discovery, browsing |
| Card Layout | Lists, grids, mixed content |
| Empty State | First-time, filtered-to-zero |
| Skeleton Screen | Any async content load |
| Pull to Refresh | Lists, feeds |
- **Mixed-aspect media grid (fleet shelf):** never let a grid column width decide media size; fix the frame HEIGHT per row (`--frame-h`), let width follow aspect (phone shots narrow, landscape wide) with flex-wrap, and order DOM landscape-before-portrait so small screens get two-up portraits instead of a lone phone shot on a black ground. Thumbnails that hide the product need a tap-to-enlarge path (native `<dialog>`, n of m, arrow keys, focus returns).
- **Tables inside a grid column (a methodology page with a wide table):** a bare `1fr` column is `minmax(auto, 1fr)` and its floor is the content's min width, so a wide table widens the whole page and an `overflow-x: auto` wrapper never engages. Every single-column phone breakpoint uses `grid-template-columns: minmax(0, 1fr)` plus `min-width: 0` on the grid children; then the wrapper scrolls. Verify per route, not per site: the homepage passing 390px said nothing about the second page on the same deploy.

### Feedback
| Pattern | When to Use |
|---------|-------------|
| Toast Notification | Action confirmations |
| Loading Spinner | Waits < 3 seconds |
| Skeleton Screen | Waits > 1 second |
| Success Confirmation | Important actions |
| Error Message | Any error state |

**Feedback timing:**
- 0-100ms: Instant (haptic only)
- 100ms-1s: Loading spinner
- 1s+: Skeleton screen
- 3s+: Progress bar with estimate

- **Reversibility over confirmation:** undo for anything reversible; a confirm dialog only for severe, irreversible, expensive, or security-sensitive actions.

### Commerce
| Pattern | When to Use |
|---------|-------------|
| Paywall Modal | Feature gating, premium content |
| Pricing Table | Upgrade flows |
| Free Trial CTA | SaaS, subscriptions |

### Decision
| Pattern | When to Use |
|---------|-------------|
| Single Primary CTA | Every screen |
| Sticky CTA | Long pages, checkout |

**CTA hierarchy:**
1. Primary: Filled button, high contrast
2. Secondary: Outlined or ghost
3. Tertiary: Text link

- **Decisions, not screens, are the atomic design unit:** write "to decide X the user must know A, B, C and be able to do D, E", then compose the screen from those.

---

## Screen-by-Screen Checklist

**Clarity**
- [ ] Purpose obvious in 3 seconds
- [ ] Single primary action clear
- [ ] Labels unambiguous

**Hierarchy**
- [ ] Most important element largest/highest contrast
- [ ] Clear visual grouping
- [ ] Whitespace creating breathing room

**Feedback (state matrix, not a bullet list)**

Rows = every object and action on the screen. Columns = the states each one owes. A blank cell is a gap, not a default.

| | default | loading | empty | selected | editing | disabled | success | failure (retryable / not) | offline | permission-blocked | partial |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `<object or action>` | | | | | | | | | | | |

- [ ] Every row filled or explicitly marked N/A with a reason
- [ ] Failure states say retryable or not, and preserve the user's input on validation failure
- [ ] Empty states name the next action; disabled states say why
- [ ] Reversible actions get undo; confirm only for severe, irreversible, expensive, or security-sensitive

**Mobile**
- [ ] Touch targets ≥44px
- [ ] Thumb-reachable primary actions
- [ ] No horizontal scroll
- [ ] Input font-size ≥16px

**Accessibility**
- [ ] Color contrast ≥4.5:1
- [ ] Doesn't rely on color alone
- [ ] Proper heading structure

---

## Pattern Selection by Screen Type

| Screen Type | Essential Patterns |
|-------------|-------------------|
| Welcome/Splash | Hero illustration, Benefit headline, Single CTA |
| Signup/Login | Inline validation, Smart defaults, Social proof |
| Dashboard | Card layout, Visual hierarchy, Quick actions |
| List/Feed | Infinite scroll OR pagination, Pull to refresh, Empty state |
| Detail | Back button, Sticky CTA, Share button |
| Settings | Progressive disclosure, Inline validation, Confirmation dialogs |
| Checkout | Progress indicator, Minimal nav, Error summary |
| Paywall | Social proof, Pricing table, Free trial CTA |

---

## Best-in-Class Examples

- **Notion**: Progressive disclosure, templates as education
- **Duolingo**: Gamified onboarding, immediate value
- **Linear**: Speed as design principle, command palette
- **Airbnb**: Search-first, trust through reviews
- **Stripe**: Developer onboarding excellence
- **Figma**: Zero-friction start, real-time collaboration

---

## Standalone PWA (iOS / notched devices)

Hard-won from a standalone PWA on an iPhone 13 mini: the status bar / notch silently ate the logo, hamburger, and panel topbars. The rules that prevent it:

**The core rule: EVERY element anchored to a screen edge offsets by the matching `safe-area-inset`, not just the body or the header.** Padding the body is not enough, and fixing only the header is the classic half-fix. Audit each of these and give it the inset for the edge(s) it touches:

| Element | Edge | Offset it needs |
|---------|------|-----------------|
| Top header / app bar | top | `padding-top` includes `env(safe-area-inset-top)` |
| Footer / composer / bottom nav | bottom | `padding-bottom` includes `env(safe-area-inset-bottom)` |
| Left/right icon rail | top (+ side) | `padding-top` + the side inset |
| Slide-out drawer (`top:0; bottom:0`) | top | `padding-top: env(safe-area-inset-top)` |
| Fixed overlay panel (mobile `top:0`) | top | `padding-top: env(safe-area-inset-top)` |
| FAB / floating button | bottom/side | add the inset to its offset |
| Centered modal (`align-items:center`) | none | safe as-is; the card is centered, not edge-anchored |

**Setup that makes the insets resolve:** `<meta name="viewport" content="...,viewport-fit=cover">` plus `apple-mobile-web-app-capable=yes`. With `status-bar-style=black-translucent`, web content starts at y=0 UNDER the status bar, so the insets are load-bearing, not cosmetic.

**`box-sizing:border-box` gotcha:** a fixed-height bar (`height:56px`) does NOT clear the notch by adding `padding-top` alone, because border-box keeps total height at 56px and the padding eats the content. Grow the height too: `height: calc(56px + env(safe-area-inset-top)); padding-top: env(safe-area-inset-top);`. A content-height (no fixed height) bar clears it with padding alone.

**Trust nothing but the device.** Desktop browsers and most simulators report `env(safe-area-inset-*) = 0`, so the bug is invisible until a real notched phone. Verify on hardware before claiming it fixed.