from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)


@app.route('/welcome')
def welcomefunc():
    return render_template("welcome.html")


@app.route('/signin')
def signinfunc():
    return render_template("signin.html")


@app.route('/signup')
def signupfunc():
    return render_template("signup.html")


@app.route('/invitation', methods=['GET', 'POST'])
def invitepfunc():
    if request.method == "POST":
        connection = sqlite3.connect("htdatabase.db")
        name = str(request.form['friendname'])
        cursor = connection.cursor()
        query = 'UPDATE user_list set friends="yes" where name = ?'
        result = cursor.execute(query, [name])
        connection.commit()
        return render_template("invitation.html", friend=name)
    return render_template("invitation.html")


@app.route('/addfriends', methods=['GET', 'POST'])
def addfriendsfunc():
    if request.method == "POST":
        connection = sqlite3.connect("htdatabase.db")
        name = str(request.form['name'])
        cursor = connection.cursor()
        query = 'SELECT Name, Status FROM user_list where name= ? and friends="no"'
        result = cursor.execute(query, [name])
        result = result.fetchall()
        return render_template("addfriends.html", list1=result)
    return render_template("addfriends.html")


@app.route('/friends', methods=['GET', 'POST'])
def friendsfunc():
    connection = sqlite3.connect("htdatabase.db")
    cursor = connection.cursor()
    query = 'SELECT Name, Status FROM user_list where Friends="yes"'
    result = cursor.execute(query)
    result = result.fetchall()
    return render_template("friends.html", list1=result)


@app.route('/mylocations', methods=['GET', 'POST'])
def mylocationfunc():
    connection = sqlite3.connect("htdatabase.db")
    cursor = connection.cursor()
    query = 'SELECT Location, time_from, time_to FROM user_list where name="myself"'
    result = cursor.execute(query)
    result = result.fetchall()
    return render_template("mylocations.html", list1=result)


@app.route('/searchplace', methods=['GET', 'POST'])
def searchplacefunc():
    if request.method == "POST":
        location = str(request.form['location'])
        connection = sqlite3.connect("htdatabase.db")
        cursor = connection.cursor()
        cursor1 = connection.cursor()
        query1 = 'SELECT * FROM user_list where location = ? and Friends = "yes"'
        query2 = 'SELECT "Hidden User", Location, date,time_from, time_to, status friends FROM user_list where location = ? and Friends = "no"'
        result1 = cursor.execute(query1, [location])
        result1 = result1.fetchall()
        result2 = cursor1.execute(query2, [location])
        result2 = result2.fetchall()
        return render_template("searchplace.html", verify='true', list1=result1, list2=result2)
    return render_template("searchplace.html")


@app.route('/home', methods=['GET', 'POST'])
def homefunc():
    if request.method == "POST":
        status = str(request.form['status'])
        location = str(request.form['location'])
        loc_date = str(request.form['date'])
        time_from = str(request.form['from'])
        time_to = str(request.form['to'])
        connection = sqlite3.connect("htdatabase.db")
        cursor = connection.cursor()
        message = "Submit successful"
        query = 'Insert into user_list values("myself",?,?,?,?,?,"na")'
        result = cursor.execute(
            query, [location, loc_date, time_from, time_to, status])
        connection.commit()
        return render_template("home.html", message=message)
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)
