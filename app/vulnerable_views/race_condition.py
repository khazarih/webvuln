from app import app
from flask import render_template, request, flash, redirect
from app.vulnerable_views.utils import UserBankAccount, one_transfer_at_a_time, transfer_amount
import threading

me = UserBankAccount("Khazar", 104)

users = [
    UserBankAccount("User1"),
    UserBankAccount("User2"),
    UserBankAccount("User2"),
    UserBankAccount("User2"),
]


@app.get("/race-condition")
def race_condition_get():
    context = {
        "balance": me.balance,
        "users": [(str(user.id), user.name, str(user.balance)) for user in users],
    }

    return render_template("vulnerable_templates/race_condition.html", **context)


@app.post("/race-condition")
def race_condition_post():
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
            one_transfer_at_a_time.transfer = True
    else:
        flash("Please fill the inputs to transfer money", "danger")

    return redirect("/race-condition")
