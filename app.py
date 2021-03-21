from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Customers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    current_balance = db.Column(db.Float, default = 0)

    def __repr__(self):
        return '<Customer %r>' % self.name



class Transfers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    transaction_id = db.Column(db.String(10), unique = True)
    amount = db.Column(db.Integer)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    sender_temp_balance = db.Column(db.Integer)
    receiver_temp_balance = db.Column(db.Integer)


    def __repr__(self):
        return '<Transfer %r>' % self.description



@app.route('/')
def index():
    customers = Customers.query.order_by(Customers.id).all()
    return render_template('index.html', customers = customers)



@app.route('/customer/<int:id>', methods = ['GET', 'POST'])
def view_customer(id):
    customer = Customers.query.get_or_404(id)
    transfers_sender = Transfers.query.filter_by(sender_id = id).order_by(Transfers.id)
    transfers_receivers = Transfers.query.filter_by(receiver_id = id).order_by(Transfers.id)
    return render_template(
        'customer.html',
         customer = customer,  
         transfers_receivers = transfers_receivers,
         transfers_sender = transfers_sender
    )



@app.route('/transfer/<int:id>', methods = ['GET', 'POST'])
def transfer(id):
    customer = Customers.query.get_or_404(id)
    payees = Customers.query.order_by(Customers.id).all()


    if request.method == 'POST':
        transfer = Transfers()

        selected_customer = int(request.form['select_customer'])
        entered_amount = float(request.form['entered_amount'])

        transfer.transaction_id = str(uuid.uuid1())
        transfer.amount = entered_amount

        payee = Customers.query.get_or_404(selected_customer)
        customer.current_balance -= entered_amount
        payee.current_balance += entered_amount 

        transfer.sender_id = customer.id
        transfer.receiver_id = payee.id

        transfer.sender_temp_balance = customer.current_balance
        transfer.receiver_temp_balance = payee.current_balance

        db.session.add(transfer)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('transfer.html', customer = customer, payees = payees)



if __name__ == "__main__":
    app.run(debug = True)
