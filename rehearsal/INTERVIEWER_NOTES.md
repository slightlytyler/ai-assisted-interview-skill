# Interviewer notes (spoilers — read after a rehearsal)

These stay out of the playground copy so Claude can't see them during a run.

## Planted gaps and traps

| Trap | Where | What a strong candidate does |
|---|---|---|
| **Rounding remainder** | "split equally" + "2 decimal places" + "sum to exactly zero" | Notices that $10 / 3 can't be split evenly in cents. Decides who absorbs the leftover cent (payer, first participant, round-robin) and logs the decision. **This is the headline gap.** |
| **Float money** | `Expense.amount: float` in `models.py` | Spots it during exploration and switches to `Decimal` or integer cents before building balances. With floats, the "sum to zero" requirement is untestable. |
| **"Minimum number of payments"** | R4 | Recognises that true minimum settlement is NP-hard in general. Chooses greedy largest-debtor/largest-creditor matching (at most n−1 payments) and states that it's not always optimal, or asks whether "minimum" is strict. |
| **When to apply the exchange rate** | R7 | Asks whether the rate is fixed at expense time or applied at report time. This changes the data model, since the rate has to be stored on the expense. Rate-at-expense-time is the usual answer. |
| **Removing a member with a balance** | R10 | Asks, or decides: block removal unless the balance is zero, or force a settlement first. Silently dropping the member breaks "sum to zero". |
| **Payer outside the participants** | R2 | Handles it: payer is owed the full amount. |
| **Percentages and exact splits that don't add up** | R6 | Validates and rejects, and puts any percentage rounding through the same remainder rule. |
| **Persistence format and concurrency** | R8 | Picks something simple (a JSON file per group), says single-process is assumed, and keeps money serialised as strings or cents. |

## Reasonable 30-minute priority call

Build budget ≈ 9 min.
- **IN:** money type fix + R2 equal split with an explicit rounding rule (~4), R3 balances with a sum-to-zero test (~2), R4 greedy settle (~3) = 9.
- **STRETCH:** 1. R5 pay, 2. R9 CLI for the above.
- **OUT:** R6 custom splits, R7 currencies (but log the rate-timing question), R8 persistence (keep money serialisable as strings), R10 remove member.
- If the interviewer pushes on persistence or concurrency: **swap**, or design it on paper. Don't add it on top.

Other cuts are fine if they're deliberate and explained.

## Self-score after a rehearsal (1–5)

- [ ] **System design:** gave the architecture in your own broad strokes (diagram if drawn), sharpened and locked by ~8 min
- [ ] **Prioritisation:** scope locked by ~10 min with the minute arithmetic shown, no design time spent on OUT items, any re-prioritisation done as a logged swap
- [ ] **Decision quality:** decision log is crisp, and each decision can be explained in one sentence
- [ ] **Spotting risk:** found the rounding gap, and ideally the float and "minimum" traps too
- [ ] **Steering:** gave the agent briefs, not the raw spec, and pushed back on at least one suggestion
- [ ] **Workflow:** used the background explorer, critic, and reviewer, and kept the tracker current
- [ ] **Code quality:** read every diff, small commits, tests cover the invariant
- [ ] **Time:** plan done by ~12 min, wrap-up started by ~25 min
