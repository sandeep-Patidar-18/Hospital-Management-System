from flask import Flask ,request,render_template
from flask_mysqldb import MySQL
import config
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["MYSQL_HOST"]= config.MYSQL_HOST
app.config["MYSQL_USER"]= config.MYSQL_USER
app.config["MYSQL_PASSWORD"]=config.MYSQL_PASSWORD
app.config["MYSQL_DB"]=config.MYSQL_DB

mysql = MySQL(app)

@app.route("/")
def home():
    cursor= mysql.connection.cursor()
    cursor.execute("select * from users")
    data = cursor.fetchall()
    return str(data) 

@app.route("/registration", methods=["GET","POST"])
def registration():
    if request.method == "POST":
        name= request.form['name']
        email = request.form['email']
        password = request.form['password']
        hash_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor()
        cursor.execute(" INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,hash_password))
        mysql.connection.commit()
        cursor.close()
        return "you are successfully registered "
    return render_template("registration.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[3], password):
            
            
            
            return render_template("patient.html")
        
        return "invalid email or password"

    return render_template("login.html")
        
        
        
    
    
if __name__ == "__main__":
    app.run(debug=True)
