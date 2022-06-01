import json
from flask import Flask
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
    return json.dumps(id)





app.run(debug=True)

