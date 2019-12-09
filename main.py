from app import *

@app.route('/register', methods=['POST'])
def CreateUser():
    GenerateUserId = uuid.uuid4()
    UserId = GenerateUserId
    password = request.form['password']
    pw_hash = bcrypt.generate_password_hash(password)
    email = request.form['email']
    existing_user = mongo.db.user.find_one({"email": email})
    fullName = request.form['fullName']
    address = request.form['address']
    phoneNumber = request.form['phoneNumber']
    role = request.form['role']
    verified = "No"
    profilePictureUrl = request.form['profilePictureUrl']
    createdAt = datetime.now()
    updatedAt = datetime.now()
    if existing_user is None:
        mongo.db.user.insert({'UserId': UserId ,'fullName': fullName,'email': email, 'password': pw_hash,'address':address,'phoneNumber':phoneNumber,'role':role,'verified':verified,'profilePictureUrl':profilePictureUrl,'createdAt':createdAt,'updatedAt':updatedAt})
        return jsonify({'message':'Registrasi berhasil !'})
    return jsonify({'message':'Email already exists'})

# Tambah Fitur Login
@app.route('/', methods=['POST'])
def login():
    data = request.form
    email = data['email']
    pw_hash = bcrypt.generate_password_hash(data['password'])
    a = mongo.db.user.find_one({'email':email})
    b = bcrypt.check_password_hash(a['password'],data['password'])
    result =[]
    if b == True:
        isi = mongo.db.user.find({'email':email})
        for doc in isi:
            result.append({
                'UserId':str(doc['UserId']),
                'fullName':doc['fullName'],
                'role':doc['role'],
                'verified':doc['verified']
            })
        access_token = create_access_token(identity=email)
        return jsonify({
            'result':result,
            'access_token':access_token,
            'status': 200
        })
    else:
        return jsonify({
            'result':'Not Found',
            'status':404

        })

@app.route('/edit', methods=['PUT'])
@jwt_required
def editData():
    fullName = request.form['fullName']
    address = request.form['address']
    phoneNumber = request.form['phoneNumber']
    profilePictureUrl = request.form['profilePictureUrl']
    email = request.form['email']
    updatequery = {'email': email}
    newvalues = {'$set': {'fullName': fullName, 'address': address, 'phoneNumber': phoneNumber,
                                  'profilePictureUrl': profilePictureUrl}}
    mongo.db.user.update_one(updatequery, newvalues)
    return jsonify({'message': 'Edit berhasil'})

@app.route('/forgetpassword', methods=['POST'])
def SendEmailForgetPassword():
    email = request.form['email']
    access_token = create_access_token(identity=email)

    msg = Message("EMAIL CONFIRMATION",
                  sender='EMAIL_VERIFICATION',
                  recipients=[email])
    msg.html = render_template('emails/email-verification.html')
    mail.send(msg)
    return jsonify({'message':'Buka email anda','access_token':access_token})

@app.route('/forgetpassword/changepassword',methods=['PUT'])
@jwt_required
def updateForgetPassword():
    email = get_jwt_identity()
    newpassword = request.form['newpassword']
    pw_hash = bcrypt.generate_password_hash(newpassword)
    print(email)
    updatequery = {'email': email}
    newvalues = {'$set': {'password': pw_hash}}
    mongo.db.user.update_one(updatequery, newvalues)

    return jsonify({'message':'success'})

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist



@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200



@app.route('/logout2', methods=['DELETE'])
@jwt_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


#######################################################################################################################

@app.route('/createtask/<id>', methods=['POST'])
@jwt_required
def newTask(id):
    GenerateToDoId = uuid.uuid4()
    form = request.form
    name = form['name']
    description = form['description']
    date = form['date']
    favorite = form['favorite']
    completed = False
    deleted = False
    userId = id
    createdAt = datetime.now()
    updatedAt = datetime.now()
    try:
        new_task = mongo.db.todo.insert(
                {
                    "toDoId":GenerateToDoId,
                    "name":name,
                    "description":description,
                    "date":date,
                    "favorite":favorite,
                    "completed":completed,
                    "deleted":deleted,
                    "userId":userId,
                    "createdAt":createdAt,
                    "updatedAt":updatedAt
                })
        if new_task and request.method == 'POST':
            return jsonify('Success!')
    except Exception as e:
        return e

@app.route('/showall', methods=['POST','GET'])
@jwt_required
def showalltodolist():
    user_id = "001"
    todolist = mongo.db.todo.find({'userId': user_id})
    result = []
    for alltodo in todolist:
        result.append({
            'toDoId':str(alltodo['toDoId']),
            'name':alltodo['name'],
            'description':alltodo['description'],
            'date':alltodo['date'],
            'favorite': alltodo['favorite'],
            'completed': alltodo['completed'],
            'deleted': alltodo['deleted'],
            'createdAt': alltodo['createdAt'],
            'updatedAt': alltodo['updatedAt'],
        })
    resp = jsonify({'result':result})
    return resp





if __name__ == "__main__":
    app.run(debug=True)
