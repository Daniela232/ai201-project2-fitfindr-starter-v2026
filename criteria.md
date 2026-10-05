# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** I picked 4 of 5 because my search is a plain keyword overlap match, not true semantic search. Some phrasings a user might use won't share enough keywords with the listing's title or description to score above zero, even when a matching item genuinely exists.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** 5 of 5 is reasonable here because this path is a deterministic code check, not a model call. If `search_listings` correctly returns an empty list, the branch either stops before `suggest_outfit` or it doesn't. There's no legitimate reason for this to vary run to run, unlike criterion 1, which depends on keyword overlap actually finding a match.

---

## 3. Something about state

For 5 different queries that match at least one listing, the item id in `session["selected_item"]` after search matches the item id actually passed into `suggest_outfit()` and into `create_fit_card()`, in 5 of 5 tries.

**Why this target:** I picked 5 of 5 because this is a code-level check, not a model call — the session either carries the right id through or it doesn't. There's no reason for this to vary run to run if the plumbing is built correctly, so any failure here is a real bug, not noise.



---

## 4. Something about the fit card

For 5 different items, the generated fit card mentions the item's exact price at least once, in at least 4 of 5 tries.

**Why this target:** I picked 4 of 5 because the fit card calls the model, and wording varies — it might phrase the price as "$38" one time and "around $38" another, or occasionally drop it if the prompt doesn't enforce it strongly enough. Some slack accounts for genuine wording variation without excusing a caption that never mentions price at all.



---

## 5. Your choice

For 5 queries with different max_price values, every listing search_listings returns has a price less than or equal to the stated ceiling, across all results, in 5 of 5 tries.

**Why this target:** I picked 5 of 5 because this is a deterministic filter in search_listings, not a model call. If it's implemented correctly, every result should respect the ceiling every time — any violation points to a real bug in the filter logic, not natural variation.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
