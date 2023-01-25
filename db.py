import sqlite3

from flask import g


def dict_factory(cursor, row):
    """
    Returns rows if sqlite3 as a dict with values mapped to columns

    Taken from
    https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
    """
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_connection():
    if not hasattr(g, "sqlite_db"):
        from main import app

        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = dict_factory
        g.sqlite_db = conn
    return g.sqlite_db
