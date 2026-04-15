#IMPORTS
from flask import Flask, render_template, request, jsonify
import json
import config
import pymysql

#Configuration for Database
db = config.dbserver

#App Configuration
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/nameSearch", methods=['POST', 'GET'])
def studentSearch():
    if request.method == 'POST':
        name = request.form['studentName']
        id = request.form['studentID']
        data = []
        if(id != '' or name != ''):
            cursor = db.cursor()        
            if name:
                name = f"{name}%"
                cursor.execute("SELECT * from student where name LIKE %s", [name])
            if id:
                id = f"{id}%"
                cursor.execute("SELECT * from student where ID LIKE %s", [id])
                    
            data = cursor.fetchall()        
            cursor.close()
            print("Found: ", data)
        return render_template('results.html', data=data)
    if request.method == 'GET':
        
        return render_template('studentSearch.html')

@app.route("/addStudent", methods=['POST', 'GET'])
def addStudent():
    cursor = db.cursor()
    cursor.execute("SELECT dept_name from department")
    data = cursor.fetchall()
    depts = []
    for d in data:
        depts.append(d[0])
    print(depts)
    cursor.close()
    
    if request.method == 'POST':
        id = request.form['studentID']
        name = request.form['studentName']
        dept = request.form['studentDept']
        credit = request.form['studentCredit']
        cursor = db.cursor()
        if name and id and dept and credit:
            cursor.execute("INSERT INTO student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)", [id, name, dept, credit])
        cursor.close()
        db.commit()
        return render_template('studentAdd.html', depts = depts)

    if request.method == 'GET':
        return render_template('studentAdd.html', depts = depts)


@app.route("/schedule/<int:studentID>", methods=['GET'])
def getStudentSchedule(studentID):
    cursor = db.cursor()
    cursor.execute("SELECT s.name, t.ID, t.course_id, t.semester, t.year FROM student s JOIN takes t on s.id = t.id WHERE s.id = %s", (studentID))
    schedule = cursor.fetchall()
    cursor.close()
    years = []
    for section in schedule:
        if section[4] not in years:
            years.append(section[4])
    return render_template('studentSchedule.html', schedule=schedule, years=years)
    
@app.route("/schedule/<int:studentID>", methods=['POST'])
def filterStudentSchedule(studentID):
    year = request.form['filterYear']
    cursor = db.cursor()
    #FIND ALL YEARS
    cursor.execute("SELECT DISTINCT year FROM takes WHERE id = %s", (studentID))
    years = [row[0] for row in cursor.fetchall()]

    #FIND RELEVANT CLASSES
    cursor.execute("SELECT s.name, t.ID, t.course_id, t.semester, t.year FROM student s JOIN takes t on s.id = t.id WHERE s.id = %s AND t.year = %s", (studentID, year))
    schedule = cursor.fetchall()

    #RENDER
    cursor.close()
    return render_template('studentSchedule.html', schedule=schedule, years=years, selected_year = year)

if __name__ == '__main__':
    app.run(host="localhost", port=4500)