import json
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog #IMPORTANT STEP
from config import db
from bson import ObjectId

app = Flask("spicebasket")

@app.route("/", methods=["GET"]) #root (/)
def home():
    return "This is the Home Page!"

#Create an about endpoint and show your name

@app.route("/about")
def about(): 
    return me["first"] + " " + me["last"]

@app.route("/myaddress")
def address():
    return f'{me["address"]["street"]} {me["address"]["number"]}'
    

#######################################################################
###################  API ENDPOINTS  ###################################
#######################################################################
# Position -> Test endpoints of REST APIs


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    results = []
    cursor = db.products.find({}) # get all data from the collection

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)

# POST Method to create new products
@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    db.products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)



# make an endpoint to send back how many products are in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items) #return the value


@app.route("/api/product/<id>", methods=["GET"])
def get_product(id):

    for prod in catalog:
        print (prod)
        if prod["_id"] == id:
            return json.dumps(prod)

    return abort(404, "Id does not match any product")


@app.route("/api/catalog/total", methods=["GET"])
def get_total():
        total = 0
        cursor = db.products.find({})
        for prod in cursor:
            total += prod["price"]
        return json.dumps(total)


@app.route("/api/products/<category>", methods=["GET"])
def products_by_category(category):
    results = []
    category = category.lower()
    for prod in catalog:
        if prod["category"].lower() == category:
            results.append(prod)

    return json.dumps(results)


@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products({})
    results = []
    for prod in cursor:
        cat = prod["category"]
        if not cat in results:
            results.append(cat)

    return json.dumps(results)


#get the cheapest product

@app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:
        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])
    return json.dumps(solution)




app.run(debug=True)

