from flask import Blueprint, jsonify, request
from db import db
from models import Product, Customer, Order

api_products_bp = Blueprint("api_products", __name__)
@api_products_bp.route("/", methods=["GET"])
def prodcuct_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = [] # output variable
    for product in results.scalars():
        json_record = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
        }
        products.append(json_record)
    return jsonify(products)




# @app.route("/api/products/", methods=["POST"])
@api_products_bp.route("/", methods=["POST"])
def prodcut_post():
    """
    This will add a new product to the database once it has been sent
    Name and Price are necessary information to update the product.
    """
    data = request.json

    if "name" not in data or "price" not in data:
        return "Invalid Request", 400
    if not isinstance (data["name"], str):
        return "Invalid Request", 400
    if not isinstance(data["price"], float):
        return "Invalid Request", 400
    if "quantity" not in data:
        data["quantity"] = 0
    
    db.session.add(Product(name=data["name"], price=data["price"], quantity=data["quantity"]))

    db.session.commit()

    return "", 204


api_products_id_bp = Blueprint("api_product_id", __name__)

# @app.route("/api/products/<int:product_id>")
@api_products_id_bp.route("/", methods=["GET"])
def product_detail_json(product_id):
    """Returns an API view of the specified product formt he product_id. This is shown in a json format and not a webpage view."""
    statement = db.select(Product).where(Product.id == product_id)
    result = db.session.execute(statement)
    products = [] # This will hold json that can be iterated once passed through when returned. 
    for product in result.scalars():
        json_record = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
        
        products.append(json_record)
        
    return jsonify(products)


# @app.route("/api/product/<int:product_id>", methods=['PUT'])
@api_products_id_bp.route("/", methods=["PUT"])
def product_put(product_id):
    data = request.json
    product = db.get_or_404(Product, product_id)

    attributes = ["name", "price", "quantity"]
    # Since data is a dicitonary, we can use the .get(value) to iterate thorugh the keys and set the value 
    updates = {}
    for attr in attributes:
        if attr in data:
            updates[attr] = data.get(attr)
    if not updates:
        return "Invalid request", 400

    for attr, value in updates.items():
        setattr(product, attr, value)
    
    
    db.session.commit()
    return "", 204

@api_products_id_bp.route("/", methods=["DELETE"])
# @app.route("/api/products/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    """Funciton is to delete a product through a delete method. It will remove the item with the specified product_id from the database."""
    prod = Product.query.filter_by(id=product_id).first()
    db.session.delete(prod)
    db.session.commit()
    return"deleted"


