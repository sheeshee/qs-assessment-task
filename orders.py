from flask import Blueprint, jsonify, abort, request
from db import get_connection

orders_pages = Blueprint('orders', __name__, url_prefix='/orders')


@orders_pages.route('/', methods=['GET'])
def list_orders():
    conn = get_connection()
    orders_list = conn.execute("SELECT * FROM orders").fetchall()
    return jsonify(orders_list)


@orders_pages.route('/<order_id>', methods=['GET'])
def get(order_id):
    order = get_connection().execute("SELECT * FROM orders WHERE id=?", (order_id)).fetchall()
    if len(order) == 0:
        return abort(404)
    elif len(order) > 1:
        # this condition should never happen as long as there is
        # a uniqueness constraint on id
        return abort(500)
    else:
        return jsonify(order[0])


@orders_pages.route('/<order_id>', methods=['DELETE'])
def delete(order_id):
    get_connection().execute("DELETE FROM orders WHERE id=?", (order_id))
    return jsonify(success=True)


@orders_pages.route('/<order_id>', methods=['PUT'])
def update(order_id):
    actual_price = request.get_json()["actual_price"]
    get_connection().execute(
        "UPDATE orders SET actual_price=? WHERE id=?",
        (actual_price, order_id)
    )
    return jsonify(success=True)


@orders_pages.route('/', methods=['POST'])
def post():
    data = request.get_json()
    get_connection().execute(
        "INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)",
        (data["id"], data["product_id"], data["actual_price"])
    )
    return jsonify(success=True)


@orders_pages.route('/metrics', methods=['GET'])
def metrics():
    pass
