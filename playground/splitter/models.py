from dataclasses import dataclass, field


@dataclass(frozen=True)
class Member:
    name: str


@dataclass
class Group:
    name: str
    currency: str = "USD"
    members: list[Member] = field(default_factory=list)

    def add_member(self, name: str) -> Member:
        if any(m.name == name for m in self.members):
            raise ValueError(f"member {name!r} already in group")
        member = Member(name)
        self.members.append(member)
        return member

    def get_member(self, name: str) -> Member:
        for m in self.members:
            if m.name == name:
                return m
        raise KeyError(name)


@dataclass
class Expense:
    payer: Member
    amount: float
    description: str
    participants: list[Member]
