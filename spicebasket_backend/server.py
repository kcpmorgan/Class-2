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
    
    try:
        product = request.get_json()
        errors = ""

        if not "title" in product or len(product["title"]) < 5:
            errors = "Title is required and should have at least 5 chars"

        if not "image" in product:
            errors += ", Image is required"

        if not "price" in product or product["price"] < 1:
            errors += ", Price is required and should be >= 1"

        if errors:
            return abort(400, errors)

        db.products.insert_one(product)
        product["_id"] = str(product["_id"])

        return json.dumps(product)

    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")


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
    try:
        if not ObjectId.is_valid(id):
            return abort(400, "Invalid id")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
            return abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)

    except:
        return abort(500, "Unexpected error")




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
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
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




########################################################################
#######################  COUPON CODES  #################################
########################################################################


# get all
@app.route("/api/coupons", methods=["GET"])
def get_all_coupons():
    cursor = db.coupons.find({})
    results = []
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)

    return json.dumps(results)


# save coupon code
@app.route("/api/coupons", methods=["post"])
def save_coupon():
    coupon = request.get_json()

    db.coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)


# get CC by code





app.run(debug=True)

