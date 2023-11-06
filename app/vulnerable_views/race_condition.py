from app import app
from flask import render_template, request, flash, redirect
from uuid import uuid4
import threading
import time


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


me = UserBankAccount("Khazar", 104)

users = [
    UserBankAccount("User1"),
    UserBankAccount("User2"),
    UserBankAccount("User2"),
    UserBankAccount("User2"),
]


transfer = True


def transfer_amount(me, to, amount):
    global transfer
    if transfer:
        me.remove_amount(int(amount))
        to.add_amount(int(amount))
        transfer = False


@app.get("/race-condition")
def race_condition_get():
    context = {
        "balance": me.balance,
        "users": [(str(user.id), user.name, str(user.balance)) for user in users],
    }

    return render_template("vulnerable_templates/race_condition.html", **context)


@app.post("/race-condition")
def race_condition_post():
    global transfer
    amount = request.form.get("amount")
    to = request.form.get("to")

    if amount and to:
        try:
            filtered = list(filter(lambda user: str(user.id) == to, users))
            userAccount = filtered[0]

            if userAccount:
                threads = [
                    threading.Thread(
                        target=transfer_amount, args=(me, userAccount, amount)
                    ),
                    threading.Thread(
                        target=transfer_amount, args=(me, userAccount, amount)
                    ),
                    threading.Thread(
                        target=transfer_amount, args=(me, userAccount, amount)
                    ),
                    threading.Thread(
                        target=transfer_amount, args=(me, userAccount, amount)
                    ),
                ]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

        except IndexError:
            flash("You need to select a contact to transfer money", "danger")
        else:
            flash("Transfer is successfull", "success")
            transfer = True
    else:
        flash("Please fill the inputs to transfer money", "danger")

    return redirect("/race-condition")
