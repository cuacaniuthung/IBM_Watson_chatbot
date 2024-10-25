
import os
os.add_dll_directory("C:\\Users\\MSI GF63\\anaconda3\\Lib\\site-packages\\clidriver\\bin")

from flask import Flask, request, redirect, render_template
import ibm_db

app = Flask(__name__)

# DB2 connection details
dsn = "DATABASE=bludb;HOSTNAME=change;PORT=change;PROTOCOL=TCPIP;UID=change;PWD=change;SECURITY=SSL"

@app.route('/')
def index():
    # Retrieve the list of students from DB2
    conn = ibm_db.connect(dsn, "", "")
    students = []
    if conn:
        sql = "SELECT Ten_Sinh_Vien, Ngay_Sinh, Ma_SV, Chuyen_Nganh FROM students"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        while result:
            students.append(result)
            result = ibm_db.fetch_assoc(stmt)
        ibm_db.close(conn)

    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    dob = request.form['dob']
    student_id = request.form['student_id']
    major = request.form['major']
    
    # Insert into DB2
    conn = ibm_db.connect(dsn, "", "")
    if conn:
        insert_sql = f"INSERT INTO students (Ten_Sinh_Vien, Ngay_Sinh, Ma_SV, Chuyen_Nganh) VALUES ('{name}', '{dob}', '{student_id}', '{major}')"
        ibm_db.exec_immediate(conn, insert_sql)
        ibm_db.close(conn)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']
    
    # Delete from DB2
    conn = ibm_db.connect(dsn, "", "")
    if conn:
        delete_sql = f"DELETE FROM students WHERE Ma_SV='{student_id}'"
        ibm_db.exec_immediate(conn, delete_sql)
        ibm_db.close(conn)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
