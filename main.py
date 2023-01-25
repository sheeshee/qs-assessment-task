from flask import Flask, g
from orders import orders_pages

app = Flask(__name__)
app.register_blueprint(orders_pages)
app.config['DATABASE'] = "db.sqlite3"


# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == "__main__":
    app.run()
