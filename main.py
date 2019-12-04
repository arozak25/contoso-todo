from app import *
from flask import jsonify,request,Flask,url_for,session,redirect,render_template
from datetime import datetime
import uuid


@app.route('/register', methods=['GET','POST'])
def CreateUser():
    GenerateUserId = uuid.uuid4()
    UserId = GenerateUserId
    password = request.form['password']
    email = request.form['email']
    existing_user = mongo.db.User.find_one({"email": email})
    fullName = request.form['fullName']
    address = request.form['address']
    phoneNumber = request.form['phoneNumber']
    role = request.form['role']
    verified = "No"
    profilePictureUrl = request.form['profilePictureUrl']
    createdAt = datetime.now()
    updatedAt = datetime.now()
    if existing_user is None:
        mongo.db.user.insert({'UserId': UserId ,'fullName': fullName,'email': email, 'password': password,'address':address,'phoneNumber':phoneNumber,'role':role,'verified':verified,'profilePictureUrl':profilePictureUrl,'createdAt':createdAt,'updatedAt':updatedAt})
        return jsonify({'message':'Registrasi berhasil !'})
    return jsonify({'message':'Email already exists'})

# Tambah Fitur Login
@app.route('/', methods=['POST','GET'])
def login():
    data = request.form
    email = data['email']
    password = data['password']
    find_user = mongo.db.user.find({"email":email,"password":password})
    result = []
    if find_user is None:
        return jsonify({"message":"Data Not Found"}), 200
    else:
        for cs in find_user:
            result.append(
					{
						'id':str(cs['UserId']),
						'name':cs['fullName'],
                        'email':cs['email']
					}
				)
        access_token = create_access_token(identity=email)
        return jsonify(
            {
                'result':result,
                'access_token':access_token,
                'status':200
            }
        )










#
# @app.route('/register/userdata', methods=['GET','POST'])
# def InsertDataUser():
#     fullName = request.form['fullName']
#     address = request.form['address']
#     phoneNumber = request.form['phoneNumber']
#     profilePictureUrl = request.form['ProfilePictureUrl']
#     updatequery = {'email': 'dandungjnjnjn@gmail.com'}
#     newvalues = {'$set': {'fullName': fullName, 'address': address, 'phoneNumber': phoneNumber,'profilePictureUrl':profilePictureUrl}}
#
#     mongo.db.user.update_one(updatequery,newvalues)

if __name__ == "__main__":
    app.run(debug=True)
