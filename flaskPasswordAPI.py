import sqlite3
import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
db = SQLAlchemy(app)

class Password(db.Model):
    primeKey = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(35), nullable = False)
    strength = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.password)
db.create_all()

@app.route('/savePass/<string:savedPass>', methods=['GET'])
def savePassword(savedPass):
    currentStrength = 0

    if len(savedPass) > 15:
        currentStrength += 1
    if re.search(r'[A-Z]', savedPass) is not None:
        currentStrength += 1
    if re.search(r'[a-z]', savedPass) is not None:
        currentStrength += 1
    if re.search(r'[0-9]', savedPass) is not None:
        currentStrength += 1
    if re.search('\W', savedPass) is not None:
        currentStrength += 1

    db.session.add(Password(password = savedPass, strength = currentStrength))
    db.session.commit()
    return jsonify({"password you saved": savedPass})

@app.route('/', methods = ["GET", "POST"])
def showPassword():
    passList = []
    for u in db.session.query(Password).all():
        passList.append(u.__dict__['password'])
    return jsonify({"All passwords": passList})


@app.route('/information/<int:givenInt>', methods = ["GET", "POST"])
def passwordInformation(givenInt):
    if givenInt > len(db.session.query(Password).all()) or givenInt < 1:
        return jsonify({"That Thing?": "It doesnt exist.  Please choose an existing password"})
    else:
        for u in db.session.query(Password).filter(Password.primeKey == givenInt).all():
            associatedPassword = (u.__dict__['password'])
            associatedStrength = (u.__dict__['strength'])
        return jsonify({"Password": associatedPassword, "Strength": associatedStrength})


app.run(debug=True)
