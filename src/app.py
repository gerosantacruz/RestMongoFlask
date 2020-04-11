from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/pymongodb"
mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():
    #recieve data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and password and email:
        hashedpassword = generate_password_hash(password)
        id= mongo.db.users.insert(
            {'username':username, 'email':email, 'password':password}
        )
        response = {
            'id': str(id),
            'username': username,
            'password': hashedpassword,
            'email': email,
        }
        return response
    else:
        return not_found()

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user_id(id):
   user = mongo.db.users.find_one({'_id': ObjectId(id)})
   response = json_util.dumps(user)
   return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' have been deleted succesfully'})
    return response

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password= request.json['password']

    if username and password and email:
        hashed_pass = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':{
            'username':username,
            'password': hashed_pass,
            'email': email
        }})
    response = jsonify({'message': 'User ' + id + ' have been updated succesfully'})
    return response



@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resoource not found: ' + request.url,
        'Status': 404
    })   
    response.status_code = 404
    return response 



if __name__ == "__main__":
        app.run(debug=True)