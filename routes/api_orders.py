from flask import Blueprint, jsonify, request, redirect, url_for
from db import db
from models import Order, ProductOrder, Customer, Product

api_orders_bp = Blueprint("api_orders", __name__)

# All orders data
@api_orders_bp.route("/", methods=["GET"])
def orders_json():
    statement = db.select(Order).order_by(Order.id) 
    results = db.session.execute(statement)
    orders = []
    for order in results.scalars().all(): 
        orders.append(order.to_json())
    return jsonify(orders)

# Create new order
@api_orders_bp.route("/", methods = ["POST"])
def create_order():
    data = request.json
    #A error handler where it will capture if the customer_id or items is not set.
    if "customer_id" not in data or "items" not in data:
        return "Missing customer_id or items", 400
    # An error handler where it will detect if the name or quantity is not set. 
    for each in data["items"]:
        if "name" not in each or "quantity" not in each:
            return "Missing name or quantity", 400
        
        
        
    customer = db.get_or_404(Customer, data["customer_id"])
    items = data["items"]
    new_order = Order(customer = customer)
    db.session.add(new_order)

    for item in items:
        stm = db.select(Product).where(Product.name == item["name"])
        product = db.session.execute(stm).scalar()
        
        if product is None:
            return "", 400
        #if the product availability is LESS than Item Quantity. 
        if product.availability < item["quantity"]:
            return "", 400
        
        po = ProductOrder(order = new_order, product = product, quantity = item["quantity"])
        db.session.add(po)

    db.session.commit()
    return "", 204

api_order_id_bp = Blueprint("api_order_id", __name__)



@api_order_id_bp.route("/", methods=["PUT"])
def process_order_put(order_id):
    print(":LSKDJF:LSDKJF:SDLKJFSDLK:JFS:DLKJFDS")
    order = Order.query.filter_by(id=order_id).first()
    data = request.get_json()

    
    if not data.get('process', False):
        return "", 400

    strategy = data.get('strategy', 'adjust')
    print(strategy) # Debugging to check what strategy is
    print(data["strategy"]) # Debugging to check what this displays
    if strategy not in ['adjust', 'reject', 'ignore']:
        return "", 400

    [success, message] = order.process_method(data["strategy"])
    if not success:
        return "", 400
    else:
        success = jsonify({"message": message})
        
    return "", 200


# Proess an order (no json required, default strategy = "adjust")
@api_order_id_bp.route("/", methods=["POST"])
def process_order_no_json(order_id):
    order = db.get_or_404(Order, order_id)
    order.process_method()
    return redirect(url_for("orders"))


@api_order_id_bp.route("/", methods=["GET"])
def order_json(order_id):
    order = Order.query.filter_by(id=order_id).first()
    #order.process_method()
    return jsonify(order.to_json())

