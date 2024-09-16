from flask import Flask, request, session, redirect, render_template, jsonify, url_for
import csv
import os
import uuid
from functools import wraps

app = Flask(__name__)
app.secret_key = '321'  # Change this to a secure key
PASSWORD_FILE = 'passwords.csv'
CSV_BASE_FILE = 'students_{}.csv'
STAFF_CSV_BASE_FILE = 'staff_{}.csv'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_passwords():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['password'])

def check_password(password):
    with open(PASSWORD_FILE, 'r') as file:
        reader = csv.reader(file)
        passwords = [row[0] for row in reader]
    return password in passwords

def add_password(password):
    with open(PASSWORD_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([password])

def init_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'roll_number', 'department', 'class_', 'date_of_birth', 'gender','address', 'phone_number', 'mail_id', 'marksheet', 'certificate'])

def init_staff_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'age', 'gender', 'date_of_joining', 'date_of_birth', 'address', 'phone_number','designation', 'department'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'login':
            password = request.form['password']
            if check_password(password):
                session['logged_in'] = True
                session['current_password'] = password
                return jsonify({'success': True, 'redirect': url_for('root')})
            else:
                return jsonify({'success': False, 'error': 'Invalid password.'})
        
        elif action == 'set_password':
            new_password = request.form['new_password']
            if not check_password(new_password):
                add_password(new_password)
                init_csv(CSV_BASE_FILE.format(new_password))
                init_staff_csv(STAFF_CSV_BASE_FILE.format(new_password))
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error': 'Password already exists.'})
    
    return render_template('login.html')

@app.route('/')
def root():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('index.html')

def get_csv_file():
    password = session.get('current_password')
    if password:
        return CSV_BASE_FILE.format(password)
    return None

def get_staff_csv_file():
    password = session.get('current_password')
    if password:
        return STAFF_CSV_BASE_FILE.format(password)
    return None

@app.route('/students', methods=['GET', 'POST'])
@login_required
def manage_students():
    csv_file = get_csv_file()

    if not csv_file:
        return jsonify({'error': 'No database file found.'}), 500

    if request.method == 'POST':
        data = request.json

        # Check for duplicates
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if (row['roll_number'] == data.get('roll_number') or
                        row['phone_number'] == data.get('phone_number') or
                        row['mail_id'] == data.get('mail_id')):
                        return jsonify({'error': 'Duplicate entry found.'}), 400

            # If no duplicates, add the student
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    data.get('name', ''),
                    data.get('roll_number', ''),
                    data.get('department', ''),
                    data.get('class_', ''),
                    data.get('date_of_birth', ''),
                    data.get('gender', ''),
                    data.get('address', ''),
                    data.get('phone_number', ''),
                    data.get('mail_id', ''),
                    data.get('marksheet', ''),
                    data.get('certificate', '')
                ])
            return jsonify({'message': 'Student added successfully'}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

  

    elif request.method == 'GET':
        students = []
        if os.path.exists(csv_file):
            try:
                with open(csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        students.append(row)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return jsonify(students), 200

@app.route('/students/<roll_number>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def student_details(roll_number):
    csv_file = get_csv_file()
    if not csv_file:
        return jsonify({'error': 'No database file found.'}), 500

    if request.method == 'GET':
        try:
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['roll_number'] == roll_number:
                        return jsonify(row), 200
            return jsonify({'error': 'Student not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'PUT':
        updated_data = request.json
        try:
            rows = []
            student_found = False
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['roll_number'] == roll_number:
                        row.update(updated_data)
                        student_found = True
                    rows.append(row)

            if not student_found:
                return jsonify({'error': 'Student not found'}), 404

            with open(csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return jsonify({'message': 'Student updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            rows = []
            student_found = False
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['roll_number'] != roll_number:
                        rows.append(row)
                    else:
                        student_found = True

            if not student_found:
                return jsonify({'error': 'Student not found'}), 404

            with open(csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return jsonify({'message': 'Student deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/staff', methods=['GET', 'POST'])
@login_required
def manage_staff():
    staff_csv_file = get_staff_csv_file()

    if not staff_csv_file:
        return jsonify({'error': 'No staff database file found.'}), 500

    if request.method == 'POST':
        data = request.json
        data['id'] = str(uuid.uuid4())  # Generate a unique ID for each staff member

        try:
            # Check for duplicates
            with open(staff_csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['phone_number'] == data.get('phone_number'):
                        return jsonify({'error': 'Duplicate phone number found.'}), 400

            # If no duplicates, add the staff
            with open(staff_csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    data['id'],
                    data.get('name', ''),
                    data.get('age', ''),
                    data.get('gender', ''),
                    data.get('date_of_joining', ''),
                    data.get('date_of_birth', ''),
                    data.get('address', ''),
                    data.get('phone_number', ''),
                    data.get('designation', ''),
                    data.get('department', '')
                ])
            return jsonify({'message': 'Staff added successfully', 'id': data['id']}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    elif request.method == 'GET':
        staff_list = []
        if os.path.exists(staff_csv_file):
            try:
                with open(staff_csv_file, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        staff_list.append(row)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return jsonify(staff_list), 200

@app.route('/staff/<staff_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def staff_details(staff_id):
    staff_csv_file = get_staff_csv_file()
    if not staff_csv_file:
        return jsonify({'error': 'No staff database file found.'}), 500

    if request.method == 'GET':
        try:
            with open(staff_csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['id'] == staff_id:
                        return jsonify(row), 200
            return jsonify({'error': 'Staff member not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'PUT':
        updated_data = request.json
        try:
            rows = []
            staff_found = False
            with open(staff_csv_file, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['id'] == staff_id:
                        row.update(updated_data)
                        staff_found = True
                    rows.append(row)

            if not staff_found:
                return jsonify({'error': 'Staff member not found'}), 404

            with open(staff_csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return jsonify({'message': 'Staff member updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            rows = []
            staff_found = False
            with open(staff_csv_file, 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row['id'] != staff_id:
                        rows.append(row)
                    else:
                        staff_found = True

            if not staff_found:
                return jsonify({'error': 'Staff member not found'}), 404

            with open(staff_csv_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            return jsonify({'message': 'Staff member deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_passwords()
    app.run(host="0.0.0.0", port=8005,debug=True,threaded=True)

