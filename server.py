from flask import Flask, request
import sqlite3

#Create instance of the class
app = Flask(__name__)

#Define connection and cursor
connection = sqlite3.connect('SIS.db', check_same_thread=False)
cursor = connection.cursor()


#Get all students
@app.route('/getstudents')
def get_students():
    data = []
    for row in cursor.execute("SELECT id, first_Name, last_Name, age, gender FROM student ORDER BY id"):
        resultDictionary = {
            "id":row[0],
            "first_name":row[1],
            "last_name":row[2],
            "age":row[3],
            "gender":row[4],
        }
        data.append(resultDictionary)
    return data

@app.route('/getstudent')
def get_student():
    check_id = 1
    idVal = request.args.get('id') 
    data = []
    for row in cursor.execute("SELECT id, first_Name, last_Name, age, gender FROM student ORDER BY id"):
        if check_id == int(idVal):
            resultDictionary = {
                "id":row[0],
                "first_name":row[1],
                "last_name":row[2],
                "age":row[3],
                "gender":row[4]
            }
            data.append(resultDictionary)
        check_id = check_id+1
    return data

@app.route('/addstudent')
def add_student():
    firstName = request.args.get('firstname') 
    lastName = request.args.get('lastname') 
    age = request.args.get('age') 
    gender = request.args.get('gender') 
    inputs = (int(highestID)+1, firstName, lastName, int(age), gender)
    cursor.execute("INSERT INTO student (id, first_Name, last_Name, age, gender) VALUES(?, ?, ?, ?, ?)", inputs)
    connection.commit()
    get_students()
    return ("Added student in id "+str(int(highestID)+1))
    
@app.route('/editstudent')
def edit_student():
    idVal = request.args.get('id') 
    firstName = request.args.get('firstname') 
    lastName = request.args.get('lastname') 
    age = request.args.get('age') 
    gender = request.args.get('gender') 
    cursor.execute("UPDATE student SET first_Name = (?) WHERE id = (?)", (firstName, idVal))
    cursor.execute("UPDATE student SET last_Name = (?) WHERE id = (?)", (lastName, idVal))
    cursor.execute("UPDATE student SET age = (?) WHERE id = (?)", (age, idVal))
    cursor.execute("UPDATE student SET gender = (?) WHERE id = (?)", (gender, idVal))
    connection.commit()
    return ("Updated student in id "+str(idVal))

@app.route('/deletestudent')
def delete_student():
    idVal = request.args.get('id') 
    cursor.execute("DELETE FROM student WHERE id IN (?)", [int(idVal)])
    connection.commit()
    return ("Deleted student with id of "+str(idVal))



highestID = 0
for row in cursor.execute("SELECT first_Name, last_Name, age, gender FROM student ORDER BY id"):
    highestID = highestID+1
    
if __name__ == '__main__':
    app.run(debug=True)