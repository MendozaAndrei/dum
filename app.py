from flask import *
import csv
from pathlib import Path
from db import db
from sqlalchemy import select
from flask import redirect, url_for
from models import Customer, Product, Order, ProductOrder

app = Flask(__name__)
#This will create a database file named "database.db" in the current directory pookie
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()
db.init_app(app)


@app.route("/") 
def home():
    """This is the homepage. Nothing will be shown here"""
    return render_template("base.html")

"""

================================CUSTOMERS================================
Contains
    main page       =This holds the list of customers that are available. 
                     Each customer name is linked to the orders they've made. 
    customer_detail = an API that holds a json format of the customer details.
                      This can be accessed through their customer ID's
    api view        = An API view that holds ALL the customers and their information in the database.
    METHODS
        DELETE      = This will delete the customer from the database.
        PUT         = This will update the customer's balance in the database.
        POST        = This will add a new customer to the database.
    
"""

# =========================================
from routes.api_customers import *
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_customer_id_bp, url_prefix="/api/customers/<int:customer_id>")

# =========================================


@app.route("/customers")
def customers():
    # staetement will hold the query that will be executed. Can be done in one line, but for safety, done with multiple
    statement = select(Customer).order_by(Customer.name)
    # Executed the statement and stores the records in the variable records
    records = db.session.execute(statement)
    #The records and converted into Scalars that can be accessed and iterated through. 
    app_data = records.scalars()
    #For the testing
    print(statement)
    return render_template("customers.html", customers=app_data)

@app.route("/customer/<int:customer_id>")
def customer_detail(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return "Customer not found", 404

    orders = Order.query.filter_by(customer_id=customer_id).all()

    for order in orders:
        order.total = sum([float(item.product.price) * float(item.quantity) for item in order.items])
    return render_template("customer_detail.html", customer=customer, orders=orders)



"""
================================PRODUCTS================================
This displays the products that are available in the "store".
The data is extracted from the Product database. 
This part needs more testing and understanding.

"""

from routes.api_products import *
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(api_products_id_bp, url_prefix="/api/products/<int:product_id>")

@app.route("/products")
def products():
    '''This is the products page. It will show all the products in the database.'''
    statement = select(Product).order_by(Product.name)
    records = db.session.execute(statement)
    app_data = records.scalars()
    return render_template("products.html", products=app_data)





"""

==========================ORDERS==========================
bane of my existence. Fuck this part. 


"""

@app.route("/orders")
def orders():
    '''This is the orders page. It will show all the orders listed in the database.'''
    statement = select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    
    orders = records.scalars().all()
    for order in orders:
        order.total = sum(float(item.product.price) * float(item.quantity) for item in order.items)
    
    return render_template("orders.html", orders=orders)

@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)

    customer = Customer.query.get(order.customer_id)

    # order.total = sum(float(item.product.price) * float(item.quantity) for item in order.items)
    # for order in orders:
    #     order.total = sum([float(item.product.price) * float(item.quantity) for item in order.items])
    order.total = sum(item.product.price * item.quantity for item in order.items)
    customer.balance -= order.total
    db.session.commit()
    return render_template("order_details.html", order=order, customer=customer)




from routes.api_orders import *
app.register_blueprint(api_orders_bp, url_prefix="/api/orders/")
app.register_blueprint(api_order_id_bp, url_prefix="/api/orders/<int:order_id>")

# @app.route("/api/orders")
# def order_json():
#     statement = db.select(Order).order_by(Order.id)
#     results = db.session.execute(statement)
#     data = []
#     for data_p in results.scalars():
#         json_record = {
#             "id": data_p.id,
#             "customer_id": data_p.customer_id,
            
#         }
#         data.append(json_record)
#     return jsonify(data)

@app.route("/orders/<int:order_id>/delete", methods = ["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    customer = Customer.query.get(order.customer_id)

    stm = db.select(ProductOrder).where(ProductOrder.order_id == order.id)
    res = db.session.execute(stm).scalars().all()
    for each in res:
        db.session.delete(each)
    
    db.session.delete(order)
    db.session.commit()

    db.session.refresh(customer)  # Refresh the customer object from the database
    if order in customer.orders:
        customer.orders.remove(order)  # Remove the order from the customer's list of orders
        db.session.commit()

    return redirect(url_for("orders"))

@app.route("/orders/<int:order_id>/update", methods=["POST"])
def order_update(order_id):
    # data = request.get_json()

    # if data is None or data.get('process') != True:
    #     return jsonify({"error": "Invalid request"}), 400

    # order = Order.query.get(order_id)

    # if order is None:
    #     return jsonify({"error": "Order not found"}), 404

    # [success, message] = order.process_method()

    # if success:
    #     return redirect(url_for("orders"))
    # else: 
    #     return jsonify({"error": message})
    order = db.get_or_404(Order, order_id)
    [result, error_message] = order.process_method(strategy="adjust")
    if result == False:
        return error_message, 400
    elif result == True:
        db.session.commit()
        return redirect(url_for("orders"))
if __name__=="__main__":
    app.run(debug=True, port=8388)


    
# @app.route("/api/customers")
# def customers_json():
    
#     statement = db.select(Customer).order_by(Customer.name)
#     results = db.session.execute(statement)
    
#     customers = [] #A list that will contain everything that needs to be known and will be pass through for iteration in the html file.
#     for customer in results.scalars():
#         json_record = {
#         "id": customer.id,
#         "name": customer.name,
#         "phone": customer.phone,
#         "balance": customer.balance,
#         } #This one however does not have the order things. Too lazy to do that. 
#         customers.append(json_record)
#     return jsonify(customers)


# An API view of a specific character passed through by their ID. 
# @app.route("/api/customers/<int:customers_id>")
# def customer_detail_json(customers_id):
#     statement = db.select(Customer).where(Customer.id == customers_id)
#     result = db.session.execute(statement)
#     products = []
#     for product in result.scalars():
#         json_record = {
#             "id": product.id,
#             "name": product.name,
#             "phone": product.phone,
#             "balance": product.balance
#         }
        
#         products.append(json_record)
        
#     return jsonify(products)
# This'll delete the item. The method is delete, so it will delete
# @app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
# def customer_delete(customer_id):
#     customer = Customer.query.get(customer_id)
#     db.session.delete(customer)
#     db.session.commit()
#     return"deleted", 204
# # 
#Will PUT new data into an existing Customer. If they no exist, returns an error.
# @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
# def customer_update(customer_id):
#     data = request.json
#     customer = db.get_or_404(Customer, customer_id)

#     if "balance" not in data:
#         return "Invalid request", 400
    
#     if not isinstance(data["balance"], (int, float)):
#         return "Invalid request: balance", 400
#     number = data["balance"]
#     new_number = round(number,3)
#     customer.balance = new_number
#     print(customer.name)
#     db.session.commit()
#     customers()
#     return "", 204
#Posting a NEW customer in the database. 
# @app.route("/api/customers", methods=["POST"])
# def customer_Post():
#     data = request.json

#     if "name" and "phone" not in data:
#         return "Invalid Request", 400
#     if not isinstance (data["name"], str):
#         return "Invalid Request", 400
#     if not isinstance(data["phone"], str):
#         return "Invalid Request", 400
    
    
#     db.session.add(Customer(name=data["name"], phone=data["phone"]))
    

#     return "", 201

# @app.route("/api/products")
# def products_json():
#     """Takes the data from products database and returns a JSON format of the data. THis is EVERYTHING"""
#     statement = db.select(Product).order_by(Product.name)
#     results = db.session.execute(statement)
#     products = [] # output variable
#     for product in results.scalars():
#         json_record = {
#         "id": product.id,
#         "name": product.name,
#         "price": product.price,
#         "quantity": product.quantity
#         }
#         products.append(json_record)
#     return jsonify(products)


# @app.route("/api/products/<int:product_id>")
# def product_detail_json(product_id):
#     """Returns an API view of the specified product formt he product_id. This is shown in a json format and not a webpage view."""
#     statement = db.select(Product).where(Product.id == product_id)
#     result = db.session.execute(statement)
#     products = [] # This will hold json that can be iterated once passed through when returned. 
#     for product in result.scalars():
#         json_record = {
#             "id": product.id,
#             "name": product.name,
#             "price": product.price,
#             "quantity": product.quantity
#         }
        
#         products.append(json_record)
        
#     return jsonify(products)

# @app.route("/api/products/<int:product_id>", methods=["DELETE"])
# def product_delete(product_id):
#     """Funciton is to delete a product through a delete method. It will remove the item with the specified product_id from the database."""
#     prod = Customer.query.get(product_id)
#     db.session.delete(prod)
#     db.session.commit()
#     return"deleted"




# @app.route("/api/products/", methods=["POST"])
# def prodcut_post():
#     """
#     This will add a new product to the database once it has been sent
#     Name and Price are necessary information to update the product.
#     """
#     data = request.json

#     if "name" not in data or "price" not in data:
#         return "Invalid Request", 400
#     if not isinstance (data["name"], str):
#         return "Invalid Request", 400
#     if not isinstance(data["price"], float):
#         return "Invalid Request", 400
#     if "quantity" not in data:
#         data["quantity"] = 0
    
#     db.session.add(Product(name=data["name"], price=data["price"], quantity=data["quantity"]))
#     db.session.commit()
#     db.session.commit()

#     return "", 204

# This one will update the product
# @app.route("/api/product/<int:product_id>", methods=['PUT'])
# def product_put(product_id):
#     data = request.json
#     product = db.get_or_404(Product, product_id)

#     attributes = ["name", "price", "quantity"]
#     # Since data is a dicitonary, we can use the .get(value) to iterate thorugh the keys and set the value 
#     updates = {attr: data.get(attr) for attr in attributes if attr in data}
#     print(updates)
#     if not updates:
#         return "Invalid request", 400

#     for attr, value in updates.items():
#         setattr(product, attr, value)
    
    
#     db.session.commit()
#     return "", 204



# @app.route("/orders", methods=["POST"])
# def create_order():
#     data = request.get_json()
#     customer = Customer.query.get(data["customer_id"])
#     if not customer:
#         return jsonify({"error": "Customer not found"}), 404

#     order = Order(customer_id=customer.id)
#     db.session.add(order)
#     db.session.commit()  # Commit the order to the database here

#     for item_data in data["items"]:
#         if "name" not in item_data or "quantity" not in item_data:
#             return jsonify({"error": "Invalid item data"}), 400

#         product = Product.query.filter_by(name=item_data["name"]).first()
#         if product:
#             product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=item_data["quantity"])
#             db.session.add(product_order)

#     db.session.commit()

#     return jsonify(order.to_json()), 201

# @app.route("/orders/<int:order_id>/delete", methods=["POST"])
# def order_delete(order_id):
#     order = db.get_or_404(Order, order_id)
#     db.session.flush()
#     db.session.delete(order)
#     db.session.commit()
#     return redirect(url_for("orders"))

# # Not even sure if this works properly. 
# @app.route("/api/orders/<int:order_id>", methods=["POST"])
# def order_update(order_id):
#     order = db.get_or_404(Order, order_id)
#     if order.strategy == "adjust":
#         order.process_method("adjust")
#     elif order.strategy == "reject":
#         order.process_method("reject")
        
#     elif order.strategy == "ignore":
#         order.process_method("ignore")
#     # else:
#         return f"This is not a valid strategy - {order.strategy}", 400
#         pass
#     db.session.commit()
    
#     return redirect(url_for("orders"))

# @app.route("/api/orders/<int:order_id>", methods=["POST"])

# def order_update(order_id):
#     order = db.get_or_404(Order, order_id)

#     if request.is_json:
#         strategy = request.get_json().get('strategy', 'adjust')  # Get strategy from request data
#     else:
#         strategy = 'adjust'

#     if strategy == "adjust":
#         order.process_method("adjust")
#     elif strategy == "reject":
#         order.process_method("reject")
#     elif strategy == "ignore":
#         order.process_method("ignore")
#     else:
#         return jsonify({"error": "Invalid strategy"}), 400

#     db.session.commit()
    
#     return redirect(url_for("orders"))