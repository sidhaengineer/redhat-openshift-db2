from flask import Flask, render_template, request, session
import ibm_db

app = Flask(__name__)

app.secret_key = "this_is_secret_key"

conn = ibm_db.connect(
    "DATABASE=bludb; HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; PORT=30699;UID=sfh23392;PWD=s1zeAnhilBTfFUu9; SECURITY=SSL;sslcertificate=DigiCertGlobalRootCA.crt", '', '')
connState = ibm_db.active(conn)
print(connState)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/jobbrowse')
def jobbrowse():
    return render_template("job-list.html")

@app.route('/jobpost')
def jobpost():
    return render_template("job-post.html")

@app.route('/jobview')
def jobview():
    return render_template("job-view.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    global uemail
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        sql = "SELECT * FROM REGISTER_HC WHERE EMAILID = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        col = ibm_db.fetch_assoc(stmt)
        if col:
            session['email'] = email
            session['username'] = col['NAME']
            uemail = session['email']
            uname = col['NAME']
            return render_template("profile.html", name = uname, email = uemail)
        else:
            msg = "Invalid Credentials"
            return render_template("login.html", msg=msg)
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop("username", None)
    return render_template("index.html")

@app.route('/profile')
def profile():
    
    return render_template("profile.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ""
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        details = [name, email, password, role]
        print(details)    

        sql = "SELECT * FROM REGISTER_HC WHERE EMAILID = ?"
        stmt = ibm_db.prepare(conn, sql) # prepare for execution
        ibm_db.bind_param(stmt, 1, email) # binding the parameter
        # ibm_db.bind_param(stmt, 2, name)
        ibm_db.execute(stmt) # execute the statement
        acc = ibm_db.fetch_assoc(stmt)
        if acc:
            msg = "You have been already regirstered, please login"
            return render_template("login.html", msg=msg)         
        else:        
            sql = "INSERT INTO REGISTER_HC VALUES (?, ?, ?, ?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.bind_param(stmt, 3, password)
            ibm_db.bind_param(stmt, 4, role)
            ibm_db.execute(stmt)
            msg = "You have successfully registered, Please login!"
            return render_template("login.html", msg=msg)
        
    return render_template("login.html", msg=msg)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)