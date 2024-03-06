
from flask import Flask
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sangam@123ABC",
  database="mydatabase"

)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM customers")


#
# return myresult

@app.route("/")
def home():
    myresult = mycursor.fetchone()
    return str(myresult)



app.run(port=5000)