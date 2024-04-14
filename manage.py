import csv
from app import app, db
from models import Customer, Product, ProductOrder, Order
# from sqlalchemy.sql.expression import random
from sqlalchemy import func , select
from sqlalchemy import and_
import random

def drop_all():
    with app.app_context():
        db.drop_all()

def create_all():
    with app.app_context():
        db.create_all()

def import_data():
    with app.app_context():
        with open('data/customers.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:                                                          #Just to test the data with different balances. 
                customers = Customer(name=row[0], phone=row[1], balance=random.choice([100, 200, 300, -1000]))
                db.session.add(customers)

        with open('data/products.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:                                  #Defaulted it to 10 to test people who request more than the quantity available.
                products = Product(name=row[0], price=row[1], quantity=10)
                db.session.add(products)

        db.session.commit()
        

def random_data():
    # Changed a little bit of the code when creating a random order. 
    with app.app_context():
        for x in range(4):
            cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
            customer = db.session.execute(cust_stmt).scalar()

            order = Order(customer=customer)
            db.session.add(order)
            db.session.commit()

            total = 0  #This one is for the total. 
            for x in range(2):  
                prod_stmt = db.select(Product).order_by(func.random()).limit(1)
                product = db.session.execute(prod_stmt).scalar()

                quantity = random.randint(1, 5)
                # Needed a way to get the total price.
                total += float(product.price) * int(quantity)

                product_order = ProductOrder.query.filter_by(order_id=order.id, product_id=product.id).first()

                if product_order:
                    product_order.quantity += quantity
                else:
                    product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=quantity)
                    db.session.add(product_order)

            db.session.commit()  


    
        

if __name__ == "__main__":
    drop_all()
    create_all()
    import_data()
    random_data()
    
    