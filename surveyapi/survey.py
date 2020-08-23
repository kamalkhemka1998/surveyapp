from flask import Flask,request
from flask_restful import Api,Resource,abort
from flask import jsonify
import dbconfig as dbc
from flask_cors import CORS
from flask_cors import cross_origin
import json
from bson import json_util

app=Flask(__name__)
api=Api(app)
cors=CORS(app, resources={r"/surveydata": {"origins": "*"},r"/qdata":{"origins":"*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
Survey = dbc.get_client().SurveyData.survey
Questions=dbc.get_client().SurveyData.questions


@app.route("/surveydata",methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def post_sd():
    json_data=request.get_json()
    print(json_data)
    Survey.insert_one(json_data)
    return {"message":"data added succesfully"}

@app.route("/qdata",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def checkconnection():
    return {"message":"Connection Okay"}

@app.route("/qdata",methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def post_questions():
    json_data=request.get_json()
    print(json_data)
    Questions.insert_one(json_data)
    return {"message":"data added succesfully"}

@app.route("/qdata/<string:tid>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getqbytid(tid):
    pipeline=[
    {
        '$project': {
            '_id': 0
        }
    }, {
        '$match': {
            'topicID': tid
        }
    }
    ]

    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))

@app.route("/surveydata/<string:tid>/<string:refid>/<string:mcqname>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getcount(tid,refid,mcqname):
    pipeline=[
    {
        '$project': {
            '_id': 0, 
            'survey': 1
        }
    }, {
        '$unwind': {
            'path': '$survey'
        }
    }, {
        '$match': {
            'survey.topicid': tid
        }
    }, {
        '$unwind': {
            'path': '$survey.data'
        }
    }, {
        '$match': {
            'survey.data.ref': refid
        }
    }, {
        '$unwind': {
            'path': '$survey.data.response.mcq'
        }
    }, {
        '$match': {
            'survey.data.response.mcq.question': mcqname
        }
    }, {
        '$group': {
            '_id': '$survey.data.response.mcq.answer', 
            'count': {
                '$sum': 1
            }
        }
    }
]
    docs=[doc for doc in Survey.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))

@app.route("/qdataTID/<string:topicId>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getRefByTopicid(topicId):
    pipeline = [
        {
            '$match': {
                'topicID': topicId
            }
        }, {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$project': {
                'data.ref': 1, 
                '_id': 0
            }
        }
    ]

    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))


@app.route("/qdata/<string:tid>/<string:refId>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getOptByRefid(tid,refId):
    pipeline = [
    {
        '$project': {
            '_id': 0, 
            'topicID': 1, 
            'data': 1
        }
    }, {
        '$match': {
            'topicID': tid
        }
    }, {
        '$unwind': {
            'path': '$data'
        }
    }, {
        '$match': {
            'data.ref': refId
        }
    }, {
        '$project': {
            'data.questions.question': 1
        }
    }, {
        '$unwind': {
            'path': '$data.questions'
        }
    }
]

    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))

@app.route("/qdataTOPIC",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getTopicId():
    pipeline =[
    {
        '$project': {
            'topicID': 1, 
            'topicName': 1, 
            '_id': 0
        }
    }
]
    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))

@app.route("/qdataques/<string:tid>/<string:ref>/<string:question>",methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def getOptions(tid,ref,question):
    pipeline = [
        {
            '$match': {
                'topicID': tid
            }
        }, {
            '$unwind': {
                'path': '$data'
            }
        }, {
            '$match': {
                'data.ref': ref
            }
        }, {
            '$unwind': {
                'path': '$data.questions'
            }
        }, {
            '$match': {
                'data.questions.question': question
            }
        }, {
            '$unwind': {
                'path': '$data.questions.options'
            }
        }, {
            '$project': {
                'data.questions.options': 1, 
                '_id': 0
            }
        }
    ]
    docs=[doc for doc in Questions.aggregate(pipeline)]
    details=json.dumps(docs,default=json_util.default)
    return jsonify(json.loads(details))



    

app.run(port=5000,debug=True)