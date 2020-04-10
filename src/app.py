from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGO_URI']:'mongodb://localhost/pytmongodb'

@app.route('/users', methods=['POST'])

def create_user():
    #recieve data
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    return {'message':'receive'}



if __name__ == "__main__":
        app.run(debug=True)