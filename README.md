
# Guide to Solution

1. Install necessary environment specified in `requirements.txt` (the only change here from the original file is the addition of pytest)
2. Check that the code base is in a working state by running `pytest`
3. Setup the "production" database by running `python setup/init_db.py`
4. Run the Flask server (in development mode) with `python main.py`
5. Go to `http://127.0.0.1:5000`
6. Use the form to input details for the order (e.g ID: 1, Product ID: 1, Actual Price: 900) and click Submit. This will create some order entries. I chose this method instead of directly editing `init_db.py` as I viewed this being more backwards compatible: the aim being to keep the setup mechanism identical to what I received. There are software solutions that handle this directly (e.g. Postman), but I wanted to practice my JavaScript a bit as well!
7. View the orders list at `http://127.0.0.1:5000/orders`


# Backend Test: Problem Statement
____

As a new developer at SpeedyBoats, your first task is to help the operational team to manage orders
and create some metrics.

They have asked you to create an API for them, based on the boilerplate code which they have provided for you.

Selling a boat is hard, it takes a lot of negotiation, this is why every boat has a __list price__ but the sale could happen on a different price.
Let's call that __actual price__.

Your tasks:
1. create the endpoints to manage the Orders
2. create a special endpoint and calculate the discount percentage by product.
___

__Discount Percentage for a product__

discount percentage = (1 - (total actual price / total list price) ) * 100


__Start Script__

Before you start the development, run the start script to populate the database with some default data.
There are 2 tables: Products and Orders. You don't have to worry about Products, it is populated for your convenience

```
python setup/init_db.py
```

### Your Task ###
1. Create API for Orders to help the sales team manage them.
When listing the Orders there should be an option to filter the response for a particular product


2. Create a special endpoint for the metrics.
This endpoint doesn't accept any parameter just returns the discount percentage per product based on the orders
