from flask import Blueprint, jsonify
from db import get_connection

orders_pages = Blueprint('orders', __name__, url_prefix='/orders')


@orders_pages.route('/', methods=['GET'])
def list_orders():
    conn = get_connection()
    cursor = conn.cursor()
    orders_list = cursor.execute("SELECT * FROM orders").fetchall()
    return jsonify(orders_list)


@orders_pages.route('/<order_id>', methods=['GET'])
def get(order_id):
    pass


@orders_pages.route('/<order_id>', methods=['DELETE'])
def delete(order_id):
    pass


@orders_pages.route('/<order_id>', methods=['PUT'])
def update(order_id):
    pass


@orders_pages.route('/', methods=['POST'])
def post():
    pass


@orders_pages.route('/metrics', methods=['GET'])
def metrics():
    pass
