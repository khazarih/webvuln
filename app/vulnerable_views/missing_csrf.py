from app import app
from flask import render_template, request, flash, redirect
from app.vulnerable_views.utils import (
    UserBankAccount,
    one_transfer_at_a_time,
    transfer_amount,
)

me = UserBankAccount("Khazar", 104)

users = [
    UserBankAccount("User1"),
    UserBankAccount("User2"),
    UserBankAccount("User3"),
    UserBankAccount("Target"),
]


@app.get("/csrf")
def csrf_get():
    context = {
        "balance": me.balance,
        "users": [(str(user.id), user.name, str(user.balance)) for user in users],
    }

    return render_template("vulnerable_templates/missing_csrf.html", **context)


@app.post("/csrf")
def csrf_post():
    amount = request.form.get("amount")
    to = request.form.get("to")

    try:
        if me.balance < int(amount):
            flash("Insufficient funds", "danger")
            return redirect("/csrf")
    except:
        pass

    if amount and to:
        try:
            filtered = list(filter(lambda user: str(user.id) == to, users))
            userAccount = filtered[0]

            if userAccount:
                transfer_amount(me, userAccount, amount)

        except IndexError:
            flash("You need to select a contact to transfer money", "danger")
        else:
            flash("Transfer is successfull", "success")
            one_transfer_at_a_time.transfer = True
    else:
        flash("Please fill the inputs to transfer money", "danger")

    return redirect("/csrf")
