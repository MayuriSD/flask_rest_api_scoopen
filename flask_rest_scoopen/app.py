from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rest_emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=False
db = SQLAlchemy(app)


class Employee(db.Model):
   # __table__ = 'emp_info'
    id = db.Column('emp_id',db.Integer(),primary_key=True)
    name = db.Column('emp_name',db.String(20))
    address = db.Column('emp_address',db.String(30))
    email = db.Column('emp_email',db.String(20))
    contact = db.Column('emp_contact',db.Integer())
#
# db.create_all()

@app.route("/employee/",methods = ['POST'])
def add_emp():
    data = request.get_json()
    emp = Employee(id = data.get('id'),
                   name = data.get('name'),
                   address = data.get('address'),
                   email = data.get('email'),
                   contact =data.get('contact'))
    db.session.add(emp)
    db.session.commit()
    return json.dumps({"success" : "Employee Record Saved..!"})

@app.route("/employee/",methods = ['GET'])
def get_all_emp():
    emps = Employee.query.all()
    if emps:
        emplist = []
        for emp in emps:
            empdict = {"Employee id" : emp.id,
                           "Employee Name" : emp.name,
                           "Employee Address" : emp.address,
                           "Employee Email" : emp.email,
                           "Employee Contact" : emp.contact
            }
            emplist.append(empdict)
        return json.dumps(emplist)
    else:
        return {"Error" : "No Employees"}

@app.route("/employee/<int:eid>",methods = ['GET'])
def get_emp(eid):
    emp = Employee.query.filter_by(id=eid).first()
    if emp:
        emp_dict = {
            "Employee Id" : emp.id,
            "EMployee Name" : emp.name,
            "Employee Address" : emp.address,
            "Employee email" : emp.email,
            "Employee contact" : emp.contact,
        }
        return json.dumps(emp_dict)
    else:
        return json.dumps({"Fail" : f"No employee with given {eid}"})

@app.route("/employee/<int:eid>", methods=['PUT'] )
def update_emp(eid):
    emp = Employee.query.filter_by(id=eid).first()
    if emp:
        data = request.get_json()
        emp.name = data.get('emp_name')
        emp.address = data.get('emp_address')
        emp.email = data.get('emp_email')
        #emp.contact = data.get('emp_contact')
        db.session.commit()
        return json.dumps({"Success" : "Data updated successfully.."})
    else:
        return json.dumps({"Error" : f"Employee with id {eid} not present.."})

@app.route("/employee/<int:eid>",methods= ['DELETE'])
def del_emp(eid):
    emp = Employee.query.filter_by(id=eid).first()
    if emp:
        db.session.delete(emp)
        db.session.commit()
        return json.dumps({"Success" : f"Emplyee {eid} has been deleted successfully.."})
    else:
        return json.dumps({"Error" : f"Employee with id {eid} does not exists!!"})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
