from flask import Flask, render_template, url_for, request, redirect, flash
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",      
        database="crud"
    )

@app.route("/")
def home():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("Select * FROM users")
    data = cursor.fetchall()
   
    cursor.close()
    con.close()
    
    return render_template("home.html",datas=data)

@app.route("/addUsers",methods=['GET','POST'])
def addUsers():
    if request.method == "POST":
        name = request.form.get("name")   
        city = request.form.get("city")   
        age  = request.form.get("age")
        con = get_db_connection()
        cursor = con.cursor() 
        cursor.execute(
            "INSERT INTO users (NAME,CITY,AGE) VALUES (%s,%s, %s)",
            [name, city, age])
        con.commit()
        
        cursor.close()
        con.close()
        flash('User Details Added')
      
        return redirect(url_for("home"))
    return render_template("addUsers.html")

@app.route("/editUser/<string:id>",methods=['GET','POST'])
def editUser(id):

    if request.method == "POST":
        name = request.form.get("name")   
        city = request.form.get("city")   
        age  = request.form.get("age")

        con = get_db_connection()
        cursor = con.cursor() 

        cursor.execute("update users set NAME=%s,CITY=%s,AGE=%s where ID=%s",[name,city,age,id])
        con.commit()
        cursor.close()
        con.close()
        flash('User Details Updated')
       
        return redirect(url_for("home"))
    
    con = get_db_connection() 
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users where ID=%s",[id])
    data = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editUser.html",datas=data)

@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):    
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)

    cursor.execute("delete FROM users where ID=%s",[id])
    con.commit()
    cursor.close()
    con.close()
    flash('User Details Deleted')
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.secret_key="abc123"
    app.run(debug=True)
