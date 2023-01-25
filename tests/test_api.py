import pytest
import json
from main import app

@pytest.fixture()
def client():
    return app.test_client()



def test_orders_list(client, db_conn):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO products (name, list_price) VALUES (?, ?)", ('Catamaran', 1000))
    cur.execute("INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)", (1, 1, 90))
    db_conn.commit()
    response = client.get("/orders/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
