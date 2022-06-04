import json
from flask import Flask, abort
from about_me import me
from mock_data import catalog

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
    return json.dumps(catalog)

# make an endpoint to send back how many products are in the catalog
@app.route("/api/catalog/count", methods=["GET"])
def get_count():
    #Here...count how many products are in the list catalog
    counts = len(catalog)
    return json.dumps(counts) #return the value


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
        for prod in catalog:
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
    results = []
    for prod in catalog:
        cat = prod["category"]
        if not cat in results:
            results.append(cat)

    return json.dumps(results)


#get the cheapest product

@app.get("/api/product/cheapest")
def get_cheapest_product():
    solution = catalog[0]
    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod

    return json.dumps(solution)




app.run(debug=True)

