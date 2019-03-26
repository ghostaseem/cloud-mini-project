from flask import Flask, render_template, request, jsonify, json, url_for, abort, redirect, session,flash
import requests
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
API_WEATHER=app.config['API_WEATHER']
API_LOCATION = app.config['API_LOCATION']
db_name = "auth.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'thisiscloudcomputingapp'

db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username


def create_db():
    db.create_all()


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")


@app.route("/user/<username>/")
def user_home(username):
    """
    Home page for validated users.
    """
    url = 'https://api.ipgeolocation.io/ipgeo?apiKey={apiKey}&ip={ip}'
    last_url = url.format(apiKey=API_LOCATION, ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    r = requests.get(last_url)
    j = json.loads(r.text)
    a = j
    if not session.get(username):
        abort(401)

    return render_template("user_home.html", username=username, final=a)


@app.route("/logout/<username>")
def logout(username):
    """ Logout user and redirect to login page with success message."""
    session.pop(username, None)
    flash("successfully logged out.")
    return redirect(url_for('login'))



with open('myrecord.json') as weather:
    load_records = json.load(weather)


my_url = 'http://api.apixu.com/v1/current.json?key={API_KEY}&q={location}'

@app.route('/result', methods=['POST', 'GET'])
def my_form_post():
    location = request.form['text']
    final_url = my_url.format(API_KEY=API_WEATHER, location=location)
    resp = requests.get(final_url)
    a = resp.json()
    return render_template("result.html",result = a)


@app.route("/mylist", methods=['POST', 'GET'])
def cassandra():
    cluster = Cluster()
    session = cluster.connect()
    session.set_keyspace("people")
    cql = "SELECT mylist FROM mylist"
    qwe = session.execute(cql)
    rows = list(qwe)
    row_list = list(rows)
    return jsonify(row_list)

@app.route('/myrecord', methods=['GET', 'POST'])
def see_records():
    return jsonify(load_records)

if __name__ == '__main__':
    app.run('0.0.0.0', port="8080", debug=True)