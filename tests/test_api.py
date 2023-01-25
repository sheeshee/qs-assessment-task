import json


JSON_HEADER = {"content-type": "application/json"}


def test_orders_list(client, populated_db):
    response = client.get("/orders/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2


def test_orders_filter(client, populated_db):
    response = client.get("/orders/?product_id=1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [dict(id=1, product_id=1, actual_price=90)]


def test_orders_get_404(client, empty_db):
    response = client.get("/orders/1")
    assert response.status_code == 404


def test_orders_get_success(client, populated_db):
    response = client.get("/orders/1")
    assert response.status_code == 200
    assert json.loads(response.data) == dict(id=1, product_id=1, actual_price=90)


def test_orders_delete(client, populated_db):
    response = client.delete("/orders/1")
    assert response.status_code == 200
    order = populated_db.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order is None


def test_orders_update(client, populated_db):
    response = client.put(
        "/orders/1", data=json.dumps({"actual_price": 5}), headers=JSON_HEADER
    )
    assert response.status_code == 200
    order = populated_db.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order["actual_price"] == 5


def test_orders_post_success(client, empty_db):
    empty_db.execute(
        "INSERT INTO products (name, list_price) VALUES (?, ?)", ("Catamaran", 1000)
    )
    payload = dict(id=1, product_id=1, actual_price=75)
    response = client.post("/orders/", data=json.dumps(payload), headers=JSON_HEADER)
    assert response.status_code == 200
    order = empty_db.execute("SELECT * FROM orders WHERE id=1").fetchone()
    assert order == payload


def test_orders_post_error(client, populated_db):
    payload = dict(id=1, product_id=1, actual_price=75)
    response = client.post("/orders/", data=json.dumps(payload), headers=JSON_HEADER)
    assert response.status_code == 409


def test_orders_metrics(client, populated_db):
    response = client.get("/orders/metrics")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == [
        dict(id=1, product_id=1, discount_percentage=91),
        dict(id=2, product_id=2, discount_percentage=75),
    ]
