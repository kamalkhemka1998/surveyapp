from flask import Flask,request
from flask_restful import Api,Resource,abort
from flask import jsonify

app=Flask(__name__)
api=Api(app)

employees=[
    {
        'empno':'23',
        'ename':'Martin'
    },
    {
        'empno':'27',
        'ename':'Ghost' 
    }
]
# def abort_if_emp_doesnt_exist(todo_id):
#     :
#         abort(404, message="Emp {} doesn't exist".format(todo_id))    

class HelloWorld(Resource):
    def put(self,empno):
        json_data=request.get_json()
        for emp in employees:
            if(emp['empno']==empno):
                emp['empno']=json_data['data']
                return {"message" :"No errors"}
    def delete(self, empno):
        for emp in employees:
            if(emp['empno']==empno):
                employees.remove(emp)
        return '', 204

  

class secondworld(Resource):
        def post(self):
            json_data=request.get_json()
            print(json_data)
            emp={'empno':json_data['empno'],'ename':json_data['ename']}
            print(emp)
            employees.append(emp)
            return {"message":"data added succesfully"}

        def get(self):
            return jsonify(employees)
        
    
api.add_resource(HelloWorld, '/employees/empno/<string:empno>') 
api.add_resource(secondworld,'/employees')
# api.add_resource(HelloWorld,'/hello')

app.run(port=5000,debug=True)