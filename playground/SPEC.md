# SPEC: Shared expense ledger

## Context

Our team goes on a lot of offsites and the "who owes whom" spreadsheet has become a mess. We want a small Python library, with a command-line interface on top, that tracks shared expenses for a group and tells people how to settle up.

The `splitter` package in this repo has a starting point. Extend it.

## Requirements

1. **Groups and members.** Create a group with a name and a home currency, and add members to it.
2. **Record an expense.** An expense has a payer, an amount, a currency, a description, and the members who shared it. By default the amount is split equally among those members.
3. **Balances.** Show each member's net balance: positive means they are owed money, negative means they owe.
4. **Settle up.** Suggest the minimum number of payments that would settle every balance in the group.
5. **Record a payment.** Record one member paying another back. This updates balances.
6. **Custom splits.** An expense can instead be split by exact amounts per member, or by percentages.
7. **Multiple currencies.** Expenses can be in any currency. Balances and settlements are reported in the group's home currency, using exchange rates supplied by the user.
8. **Persistence.** A group's ledger survives the process restarting.
9. **CLI.** `splitter add-expense`, `splitter balances`, `splitter settle`, `splitter pay`.
10. **Remove a member.** Members can leave a group.

## Non-functional

- Amounts are displayed to 2 decimal places.
- The balances in a group must always sum to exactly zero.
- No third-party runtime dependencies.
