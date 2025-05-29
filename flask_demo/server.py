from flask import Flask, make_response, request
from flask import request
import json
import os


app = Flask(__name__)

# --- Constants ---
DATA_FILE = 'data/data.json'

# --- Data funcs ---
def read_data():
    if not os.path.exists(DATA_FILE):
        return []
        print("no data")
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Routes ---

@app.route('/')
def index():
    return ({"message: ": "Hello world!"}, 204)

@app.route('/index_explicit')
def index_explicit():
    resp = make_response({"Message: ": "Hello world"})
    resp.status_code = 204
    return resp

# route for GET /data_stats
@app.route("/data_stats")
def get_data_stats():
    data = read_data()
    if data:
        return {"message": f"Data length: {len(data)}."}
    else:
        return {"message": "No data"}, 500

# checked if data in file
@app.route("/data")
def get_data():
    data = read_data()
    if data:
        return data
    else:
        return {"message": "No data"}, 500

# route to search by name
@app.route("/name_search")
def name_search():
    """ Find person in db

    returns:
        json: if found status 200
        404: if not found
        400: if arg is missing
        422: if arg is invalid
    """

    # get arg q from request
    query = request.args.get('q')

    # check if q is missing
    if query is None:
        return {"message": "Querry paramteter 'q' missing"}, 400

    # check is query is invalid
    if query.strip() == "" or query.isdigit():
        return {"message": "Invalid input param"}, 422

    data = read_data()

    # iterate through data
    for person in data:
        if query.lower() in person["first_name"].lower():
            return person, 200

    # if no match return 404
    return {"message": "person not found"}, 404


# --- API enpoints ----


# GET /person/id
@app.route("/person/<id>")
def person_id(id):
    data = read_data()
    for person in data:
        if person['id'] == str(id):
            return person
    return {"message": "Person not found"}, 404

# POST /person
@app.route("/person", methods=['POST'])
def create_person():
    new_person = request.get_json()

    if not new_person:
        return {"message": "No data provided"}, 422

    data = read_data()
    data.append(new_person)
    write_data(data)

    return {"message": "Success. Person added"}, 200

# PUT /person/id
@app.route("/person/<id>", methods = ['PUT'])
def edit_person(id):
    new_person_data = request.get_json()

    if not new_person_data:
        return {"message": "no data provided"},422
    
    data = read_data()
    for i, person in enumerate(data):
        if person['id'] == id:
            data[i] = new_person_data
            write_data(data)
            return {"message": f"data successfully updated for person with id {id}"}
    return {"message": "Person not found"},404
    
# DELETE /person/id
@app.route("/person/<id>", methods = ['DELETE'])
def delete_person(id):
    data = read_data()
    for person in data:
        if person['id'] == str(id):
            data.remove(person)
            return {"message": f"Person with ID {id} deleted"}, 200
    return {"message": "person not found"}, 404

# count endpoint to return total number of persons in data
@app.route("/count")
def count():
    data = read_data()
    data_len = len(data)
    return {"Total number of persons": data_len}, 201

# error hendling
@app.errorhandler(404)
def errorhandler(error):
    return {"message": "API method does not exist."}, 404
