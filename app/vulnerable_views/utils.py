from uuid import uuid4


class OneTransferAtATime:
    def __init__(self) -> None:
        self.transfer = True


one_transfer_at_a_time = OneTransferAtATime()


def transfer_amount(me, to, amount):
    global one_transfer_at_a_time

    if one_transfer_at_a_time.transfer:
        me.remove_amount(int(amount))
        to.add_amount(int(amount))
        one_transfer_at_a_time.transfer = False


class UserBankAccount:
    def __init__(self, name, balance=0) -> None:
        self.id = uuid4()
        self.name = name
        self.balance = balance

    def add_amount(self, amount):
        self.balance += amount

    def remove_amount(self, amount):
        if (self.balance - amount) >= 0:
            self.balance -= amount
