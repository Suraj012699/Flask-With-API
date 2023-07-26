from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///table.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    com_name = db.Column(db.String, nullable=False)
    job_role = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)


    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employees.query.all()
    employee_list = []
    for employee in employees:
        employee_dict = {
            'id' : employee.id,
            'name' : employee.name,
            'phone_no' : employee.phone_no,
            'com_name' : employee.com_name,
            'job_role' : employee.job_role,
            'location' : employee.location
        }
        employee_list.append(employee_dict)
    return jsonify({'employees':employee_list})


@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = Employees.query.get(employee_id)
    if employee:
        employee_dict = {
            'id' : employee.id,
            'name' : employee.name,
            'phone_no' : employee.phone_no,
            'com_name' : employee.com_name,
            'job_role' : employee.job_role,
            'location' : employee.location
        }
        return jsonify(employee_dict)
    return jsonify({'message': 'Employee not found'})

    
@app.route('/employees', methods=['POST'])
def add_employee():
    new_employee = Employees(
        id = request.json['id'],
        name = request.json['name'],
        phone_no = request.json['phone_no'],
        com_name = request.json['com_name'],
        job_role = request.json['job_role'],
        location = request.json['location'] 
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message':'Employee added successfully'})

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employees.query.get(employee_id)
    if employee:
        employee.name = request.json['name']
        employee.phone_no = request.json['phone_no']
        employee.com_name = request.json['com_name']
        employee.job_role= request.json['job_role']
        employee.location = request.json['location']
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'})
    return jsonify({'message': 'Employee not found'})

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employees.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
    return jsonify({'message': 'Employee not found'})

if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()