from flask import Blueprint, jsonify, request
from db import db
from models import Customer, Product


api_customers_bp = Blueprint("api_customers", __name__)
@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    
    customers = [] #A list that will contain everything that needs to be known and will be pass through for iteration in the html file.
    for customer in results.scalars():
        json_record = {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "balance": customer.balance,
        } #This one however does not have the order things. Too lazy to do that. 
        customers.append(json_record)
    return jsonify(customers)


@api_customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.json 
    if ("name" not in data) or ("phone" not in data): 
        return "Invalid request", 400
    name = data["name"] 
    phone = data["phone"]
    if (not isinstance(name, str)) or (not isinstance(phone, str)):
        return "Invalid request: Datatype", 400
    
    if "balance" in data:
        if not isinstance(data["balance"], (int, float)):
            return "Invalid request: balance", 400
        balance = data["balance"]
    else: 
        balance = 0.0
    new_customer = Customer(name=name, phone=phone, balance=balance)
    db.session.add(new_customer)
    db.session.commit()
    return "A new customer was added!", 204







# Below requires SPECIFIC CustomerID

api_customer_id_bp = Blueprint("api_customer_id", __name__)



# @app.route("/api/customers/<int:customers_id>")
@api_customer_id_bp.route("/", methods=["GET"])
def customer_detail_json(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    result = db.session.execute(statement)
    products = []
    for product in result.scalars():
        json_record = {
            "id": product.id,
            "name": product.name,
            "phone": product.phone,
            "balance": product.balance
        }
        
        products.append(json_record)
        
    return jsonify(products)




# @app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
@api_customer_id_bp.route("/", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id)).scalar()
    db.session.delete(customer)
    db.session.commit()
    return "deleted", 204



# @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
@api_customer_id_bp.route("/", methods=["PUT"])
def customer_update(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id)

    if "balance" not in data:
        return "Invalid request", 400
    
    if not isinstance(data["balance"], (int, float)):
        return "Invalid request: balance", 400
    number = data["balance"]
    new_number = round(number,3)
    customer.balance = new_number
    print(customer.name)
    db.session.commit()
    return "", 204
# sd