from app import db, Customers

customerlist = [
    {'name' : 'Vishal Bharathi', 'email': 'vish@gmail.com', 'current_balance' : 500000},
    {'name' : 'Rahul parghi', 'email': 'rahul@gmail.com', 'current_balance' : 300000},
    {'name' : 'jaydeep chudasma', 'email': 'JD@gmail.com', 'current_balance' : 100000},
]

for i in customerlist:
    new_customer = Customers()
    new_customer.name = i['name']
    new_customer.email = i['email']
    new_customer.current_balance = i['current_balance']
    db.session.add(new_customer)
    db.session.commit()

print("finished")