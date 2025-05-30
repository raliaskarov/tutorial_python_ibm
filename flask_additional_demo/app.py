# Import libraries
from flask import Flask, request, url_for, redirect, render_template
import json
import os

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
DATA_FILE = 'data/transactions.json'

# --- Data funcs ---
def read_data():
    if not os.path.exists(DATA_FILE):
        return []
        print("no data")
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- helper functions ---

# total balance
def get_total_balance(transactions):
    return sum(t['amount'] for t in transactions)


# --- Routes ---

# Read operation
@app.route('/')
def get_transactions():
    transactions = read_data()
    total_balance = get_total_balance(transactions)
    print(f"Got total_balance: {total_balance}")
    return render_template('transactions.html', transactions=transactions, total_balance=total_balance)

# Create operation
@app.route('/add', methods = ["GET", "POST"])
def add_transaction():
    transactions = read_data()
    if request.method == 'POST':

        # collection form input
        transaction = {
            'id': len(transactions) +1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        # update database
        transactions.append(transaction)
        write_data(transactions)

        # redirect to list of transactions
        return redirect(url_for("get_transactions"))

    return render_template("form.html")


# Update operation
@app.route('/edit_transaction/<int:transaction_id>', methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    transactions = read_data()
    if request.method == 'POST':
        # collect inputs
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                # update item
                transaction['date'] = date
                transaction['amount'] = amount
                # push to data
                print(f"got data for transaction id: {transaction_id} \n \n {transaction}")
                write_data(transactions)
                break
        return redirect(url_for("get_transactions"))

    # if GET find trasaction by ID
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    # else error
    return {"message": "Transaction not found"}, 404

# Delete operation
@app.route('/delete_transaction/<int:transaction_id>', methods = ["GET", "POST"])
def delete_transaction(transaction_id):
    transactions = read_data()
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            write_data(transactions)
            break
    return redirect(url_for("get_transactions"))


# Route for GET POST search_transactions
@app.route('/search', methods = ["GET", "POST"])
def search():
    transactions = read_data()
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        
        filtered_transactions = []
        for transaction in transactions:
            if (transaction['amount'] >= min_amount) & (transaction['amount'] <= max_amount):
                filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions = filtered_transactions) 

    # if GET render all transactions
    return render_template("search.html")  

# Route for GET /balance
@app.route('/balance')
def balance():
    transactions = read_data()
    total_balance = get_total_balance(transactions)
    return {"totalBalance": total_balance}

# Run the Flask app
if __name__=="__main__":
    app.run(debug=True)