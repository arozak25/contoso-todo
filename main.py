from app import *

@app.route('/register', methods=['GET','POST'])
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
@app.route('/', methods=['POST','GET'])
def login():
    data = request.form
    email = data['email']
    pw_hash = bcrypt.generate_password_hash(data['password'])
    a = mongo.db.user.find_one({'email':email})
    print(a['password'])
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
        return jsonify({
            'result':result,
            'status': 200
        })
    else:
        return jsonify({
            'result':'Not Found',
            'status':404

        })

@app.route('/edit', methods=['POST', 'GET'])
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








if __name__ == "__main__":
    app.run(debug=True)
