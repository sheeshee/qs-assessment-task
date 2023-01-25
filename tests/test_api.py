import pytest
import json
from main import app


JSON_HEADER = {'content-type': 'application/json'}


@pytest.fixture()
def client():
    return app.test_client()


def create_order_entry(db_conn):
    db_conn.execute("INSERT INTO products (name, list_price) VALUES (?, ?)", ('Catamaran', 1000))
    db_conn.execute("INSERT INTO products (name, list_price) VALUES (?, ?)", ('Dinghy', 200))
    db_conn.execute("INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)", (1, 1, 90))
    db_conn.execute("INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)", (2, 2, 50))


def test_orders_list(client, db_conn):
    create_order_entry(db_conn)
    response = client.get("/orders/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2


def test_orders_filter(client, db_conn):
    create_order_entry(db_conn)
    response = client.get("/orders/?product_id=1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [dict(id=1, product_id=1, actual_price=90)]


def test_orders_get_404(client, db_conn):
    response = client.get("/orders/1")
    assert response.status_code == 404


def test_orders_get_success(client, db_conn):
    create_order_entry(db_conn)
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert json.loads(response.data) == dict(id=1, product_id=1, actual_price=90)


def test_orders_delete(client, db_conn):
    create_order_entry(db_conn)
    response = client.delete("/orders/1")
    assert response.status_code == 200
    order = db_conn.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order is None


def test_orders_update(client, db_conn):
    create_order_entry(db_conn)

    response = client.put(
        "/orders/1",
        data=json.dumps({"actual_price": 5}),
        headers=JSON_HEADER
    )
    assert response.status_code == 200
    order = db_conn.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order["actual_price"] == 5


def test_orders_post_success(client, db_conn):
    db_conn.execute("INSERT INTO products (name, list_price) VALUES (?, ?)", ('Catamaran', 1000))
    payload = dict(
        id=1,
        product_id=1,
        actual_price=75
    )
    response = client.post("/orders/", data=json.dumps(payload), headers=JSON_HEADER)
    assert response.status_code == 200
    order = db_conn.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order == payload
