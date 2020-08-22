import dbconfig as dbc


def get_all_employees():
    e = dbc.get_client().employee.emp
    pipeline=[
    {
        '$project': {
            'empno': 1 
            # 'ename': 1
        }
    }
    ]
    return ( [{'empno':str(x['empno'])} for x in e.aggregate(pipeline)])
    
get_all_employees()