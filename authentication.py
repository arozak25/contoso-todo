from app import *
from flask import jsonify,request,Flask,url_for,session,redirect,render_template
import uuid
import datetime

@app.route('/register', methods=['GET','POST'])
def CreateUser():
    GenerateUserId = uuid.uuid4()
    UserId = GenerateUserId
    password = request.form['password']
    email = request.form['email']
    existing_user = mongo.db.User.find_one({"email": email})
    fullName = request.form['fullName']
    address = request.form['fullName']
    phoneNumber = request.form['fullName']
    role = request.form['fullName']
    verified = "No"
    profilePictureUrl = request.form['fullName']
    createdAt = datetime.now()
    updatedAt = datetime.now()
    if existing_user is None:
        mongo.db.user.insert({'UserId': UserId ,'fullName': fullName,'email': email, 'password': password,'address':address,'phoneNumber':phoneNumber,'role':role,'verified':verified,'profilePictureUrl':profilePictureUrl,'createdAt':createdAt,'updatedAt':updatedAt})
        return jsonify({'message':'Registrasi berhasil !'})
    return jsonify({'message':'Email already exists'})
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