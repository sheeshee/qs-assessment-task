import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

from db import get_connection
from main import app

BASE_DIR = Path(__file__).parent.parent


def init_db(sqlite_db):
    connection = sqlite3.connect(sqlite_db)
    # create the schema
    schema_sql = BASE_DIR / "setup/schema.sql"
    with open(schema_sql) as f:
        connection.executescript(f.read())
    connection.close()


@pytest.fixture
def empty_db():
    _, name = tempfile.mkstemp()
    app.config["DATABASE"] = name

    init_db(name)

    with app.app_context():
        conn = get_connection()
        yield conn

    os.remove(name)


@pytest.fixture
def populated_db(empty_db):
    db = empty_db
    db.execute(
        "INSERT INTO products (name, list_price) VALUES (?, ?)", ("Catamaran", 1000)
    )
    db.execute(
        "INSERT INTO products (name, list_price) VALUES (?, ?)", ("Dinghy", 200)
    )
    db.execute(
        "INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)", (1, 1, 90)
    )
    db.execute(
        "INSERT INTO orders (id, product_id, actual_price) VALUES (?, ?, ?)", (2, 2, 50)
    )
    return db


@pytest.fixture()
def client():
    return app.test_client()
