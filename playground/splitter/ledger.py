from splitter.models import Expense, Group, Member


class Ledger:
    def __init__(self, group: Group):
        self.group = group
        self.expenses: list[Expense] = []

    def add_expense(self, expense: Expense) -> None:
        raise NotImplementedError

    def balances(self) -> dict[Member, float]:
        raise NotImplementedError
