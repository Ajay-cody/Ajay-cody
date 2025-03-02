# import the flask
from flask import*

#import pymysql
import pymysql
import pymysql.cursors
# setting up file upload
import os
# initiate the app 
app=Flask(__name__)

# we need to import CORS  
# its cross origin resource sharing 
from flask_cors import CORS

CORS(app)

# define the routes 
@app.route("/api/signup",methods=["POST"])
def signup():
    gamername  = request.form["gamername"]
    gamerlevel = request.form["gamerlevel"]
    email      = request.form["email"]
    password   = request.form["password"]

    # connection to dbase 
    connection = pymysql.connect(host='localhost',user = 'root',password = '', database = 'gamingchronicle')

    # define your cursor 
    cursor = connection.cursor()

    # define your sql to insert values 
    sql = sql = "INSERT INTO gamer (gamer_name, gamer_level, email, password) VALUES (%s, %s, %s, %s)"

    
    # define your data
    data = (gamername,gamerlevel,email,password)

    # run the query 
    cursor.execute(sql,data)

    # commit changes 
    connection.commit()
     
    # Response 
    return jsonify({"message": "signup successful"})





# member signin/login 
@app.route("/api/signin", methods=["POST"])
def signin():
    # get user inputs from the form 
    email = request.form["email"]
    password = request.form["password"]
    # establish connection to database
    connection = pymysql.connect (host='localhost',user='root',password='',database='gamingchronicle')
    # define your cursor 
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # sql to select users
    sql= "select * from gamer where email = %s and password = %s"
    # define your data 
    data = (email,password)
    # execute/run query
    cursor.execute(sql,data)
    # check is user exists 
    # if exists return signin success
    # else return signin failed
    if cursor.rowcount==0:
        return jsonify({"message" : "Login failed"})
    else:
        # get user infomation upon success full login
        gamer = cursor.fetchone()
        return jsonify({"message" : "Login success","gamer": gamer})


# add product
@app.route("/api/add_products" , methods= ["POST"])
def app_products():
    # get user inputs from the form
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    product_photo=request.files["product_photo"]

#print and see user inputs
# print(product_name)
# print(product_description)
# print(product_cost)
# print(product_photo)

    # establish connection to database
    connection=pymysql.connect(host='localhost',user='root',password='',database='gamingchronicle')
    # define your cursor 
    cursor=connection.cursor()
    # define sql to insert products 
    sql = "insert into products (product_name,product_description,product_cost,product_photo) values(%s,%s,%s,%s)"
    # define data 
    data=(product_name,product_description,product_cost,product_photo)
    # execute
    cursor.execute(sql,data)
    # commit changes 
    connection.commit()
    # give Response 
    return jsonify({"message" : "product added successfully"})


# get all the products
# define the route
@app.route("/api/get_products",methods= ["GET"])
def get_products():
    connection=pymysql.connect(host='turbokid.mysql.pythonanywhere-services.com',user='turbokid',password='user1234',database='turbokid$default')
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    sql="select * from products"
    cursor.execute(sql)
    allproducts=cursor.fetchall()
    return jsonify(allproducts)



# run the application 
app.run(debug=True)