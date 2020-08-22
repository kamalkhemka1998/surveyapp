from flask import Flask,request
from flask_restful import Api,Resource,abort
from flask import jsonify
from user import authenticate,identity
from flask_jwt import JWT, jwt_required, current_identity
import getemployees as gte
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'app@123!'
jwt=JWT(app,authenticate,identity)
api=Api(app)
CORS(app)

@app.route("/employees",methods=['GET', 'POST'])
def all_products():
    return jsonify(gte.get_all_employees())
    # json_data=request.get_json()
    # print(json_data)
    # return {"message":"succesful"}

@app.route('/userinfo') 
@jwt_required()
def protected():
    return '%s' % current_identity 

app.run(port=5000,debug=True)
