import sqlite3

from flask import Blueprint, abort, jsonify, request

from db import get_connection

orders_pages = Blueprint("orders", __name__, url_prefix="/orders")


@orders_pages.route("/", methods=["GET"])
def list_orders():
    product_id = request.args.get("product_id")
    if product_id is not None:
        where_clause = f"WHERE product_id={product_id}"
    else:
        where_clause = ""

    conn = get_connection()
    orders_list = conn.execute("SELECT * FROM orders " + where_clause).fetchall()
    return jsonify(orders_list)


@orders_pages.route("/<order_id>", methods=["GET"])
def get(order_id):
    order = (
        get_connection()
        .execute("SELECT * FROM orders WHERE id=?", (order_id))
        .fetchall()
    )
    if len(order) == 0:
        return abort(404)
    elif len(order) > 1:
        # this condition should never happen as long as there is
        # a uniqueness constraint on id
        return abort(500)
    else:
        return jsonify(order[0])


@orders_pages.route("/<order_id>", methods=["DELETE"])
def delete(order_id):
    get_connection().execute("DELETE FROM orders WHERE id=?", (order_id))
    return jsonify(success=True)


@orders_pages.route("/<order_id>", methods=["PUT"])
def update(order_id):
    actual_price = request.get_json()["actual_price"]
    get_connection().execute(
        "UPDATE orders SET actual_price=? WHERE id=?", (actual_price, order_id)
    )
    return jsonify(success=True)


@orders_pages.route("/", methods=["POST"])
def post():
    data = request.get_json()
    try:
        get_connection().execute(
            "INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)",
            (data["id"], data["product_id"], data["actual_price"]),
        )
    except sqlite3.IntegrityError:
        return abort(409)
    return jsonify(success=True)


@orders_pages.route("/metrics", methods=["GET"])
def metrics():
    orders = (
        get_connection()
        .execute(
            "SELECT orders.id, product_id, actual_price, list_price FROM orders JOIN products ON orders.product_id = products.id"
        )
        .fetchall()
    )
    orders_with_discount_rate = list(map(discountify, orders))
    return jsonify(orders_with_discount_rate)


def discountify(order_entry):
    """
    Takes a dictionary of order id, product id, actual price and list price
    and returns a dictionary of id, product id and discount percentage
    """
    return dict(
        id=order_entry["id"],
        product_id=order_entry["product_id"],
        discount_percentage=calc_discount_rate(
            order_entry["list_price"], order_entry["actual_price"]
        ),
    )


def calc_discount_rate(list_price, actual_price):
    return (1 - actual_price / list_price) * 100
