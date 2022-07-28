# Free Web Panel VPN, REPO > https://github.com/XolPanel/xontolpanel
# ganti credit = titit copot

import requests
from flask import *
from sqlalchemy import create_engine
import requests, re, datetime, base64, json, os
import datetime as DT
BOT_TOKEN = os.environ.get("BOT_TOKEN")
AUTH_KEY = os.environ.get("AUTH_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL").replace("postgres://","postgresql://")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
DARK_MODE = os.environ.get("DARK_MODE")
SERVER = os.environ.get("SERVER").split(";")
server = []
for z in SERVER:
	s = z.split(",")
	server.append({"name":s[0],"host":s[1],"harga":s[2]})

db = create_engine(DATABASE_URL, pool_pre_ping=True)
db.begin()
db.execute("CREATE TABLE IF NOT EXISTS userz (saldo varchar DEFAULT 0, email varchar, password varchar, username varchar)")
db.execute("CREATE TABLE IF NOT EXISTS transaksi (username varchar, tanggal varchar, akun varchar, harga varchar, status varchar)")
db.execute(f"CREATE TABLE IF NOT EXISTS admin (username varchar DEFAULT '{ADMIN_USERNAME}', password varchar DEFAULT '{ADMIN_PASSWORD}')")
db.execute("INSERT INTO admin (username,password) VALUES (%s,%s);", (ADMIN_USERNAME,ADMIN_PASSWORD))
token = BOT_TOKEN
app = Flask(__name__)
app.secret_key = "XolPanel"
requests = requests.Session()
requests.headers.update({"AUTH_KEY":AUTH_KEY})
if DARK_MODE.lower() == "yes":
	templates = {"index":"findex1.html",
		     "delete":"delete.html",
		     "register":"register.html",
		     "topup":"topup.html",
		     "index_admin":"admin_index1.html",
		     "login_admin":"admin_signin.html",
		     "login":"signin.html",
		     "signup":"signup.html",
		     "404":"404.html",
		     "sshbuat":"sshbuat.html",
		     "sshtrial":"sshtrial.html"}
else:
	templates = {"index":"flight_index1.html",
		     "delete":"light_delete.html",
		     "register":"light_register.html",
		     "topup":"light_topup.html",
		     "index_admin":"light_admin_index1.html",
		     "login_admin":"light_admin_signin.html",
		     "login":"light_signin.html",
		     "signup":"light_signup.html",
		     "404":"light_404.html",
		     "sshbuat":"light_sshbuat.html",
		     "sshtrial":"light_sshtrial.html"}

@app.errorhandler(404)
def error404(e):
	return render_template(templates["404"])

#ADMIN DASHBOARD
@app.route("/admin/home")
def adminHome():
	x = request.cookies.get("admin")
	if not x:
		return redirect("/admin/login")
	else:
		xjs = eval(x)
		members = db.execute("SELECT * FROM userz").fetchall()
		return render_template(templates["index_admin"],nama=xjs["username"],tipe="Admin",servers=str(len(server)), members=str(len(members)) )

@app.route("/admin/login", methods=["POST","GET"])
def adminLogin():
	if request.method == "GET":
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			xjs = eval(x)
			members = db.execute("SELECT * FROM userz").fetchall()
			return render_template(templates["index_admin"],nama=xjs["username"],tipe="Admin",servers=str(len(server)), members=str(len(members)) )
	else:
		auth = db.execute("SELECT * from admin").fetchone()
		username = request.form["username"]
		password = request.form["password"]
		if not username:
			flash("Invalid Username")
			return redirect("/admin/login")
		elif not password:
			flash("Invalid Password")
			return redirect("/admin/login")
		elif not password and not username:
			flash("Invalid Password Or Username")
			return redirect("/admin/login")
		else:
			if username == auth[0] and password == auth[1]:
				res = make_response(redirect("/admin/home"))
				xc = {"username":username,"password":password}
				res.set_cookie("admin",str(xc))
				return res
			else:
				flash("Invalid Password Or Username")
				return redirect("/admin/login")

@app.route("/admin/topup", methods=["GET","POST"])
def adminTopup():
	if request.method == "GET":
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			xjs = eval(x)
			members = db.execute("SELECT * FROM userz").fetchall()
			acc = [x[1] for x in db.execute("SELECT * FROM userz").fetchall()]
			return render_template(templates["topup"],nama=xjs["username"],tipe="Admin",servers=str(len(server)), members=str(len(members)), accounts=acc )
	else:
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			saldo = request.form["saldo"]
			email = request.form.get("email")
			current_saldo = db.execute("SELECT saldo FROM userz WHERE email = %s", (email) ).fetchone()[0]
			saldoz = int(saldo) + int(current_saldo)
			db.execute("UPDATE userz SET saldo = %s WHERE email = %s", (saldoz,email))
			flash(Markup(f"<strong>TopUp Sukses!</strong> Berhasil Menambahkan {saldo} Ke {email}"))
			return redirect("/admin/topup")

@app.route("/admin/delete",methods=["GET","POST"])
def adminDelete():
	if request.method == "GET":
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			xjs = eval(x)
			acc = [x[1] for x in db.execute("SELECT * FROM userz").fetchall()]
			members = db.execute("SELECT * FROM userz").fetchall()
			return render_template(templates["delete"],nama=xjs["username"],tipe="Admin",servers=str(len(server)), members=str(len(members)), accounts=acc)
	else:
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			email = request.form.get("email")
			db.execute("DELETE FROM userz WHERE email = %s", (email) )
			flash("Akun Sukses Di Hapus")
			return redirect("/admin/delete")


@app.route("/admin/register", methods=["GET","POST"])
def adminRegister():
	if request.method == "GET":
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			xjs = eval(x)
			members = db.execute("SELECT * FROM userz").fetchall()
			return render_template(templates["register"],nama=xjs["username"],tipe="Admin",servers=str(len(server)), members=str(len(members)))
	else:
		x = request.cookies.get("admin")
		if not x:
			return render_template(templates["login_admin"])
		else:
			members = [x[1] for x in db.execute("SELECT * FROM userz").fetchall()]
			username = request.form["username"]
			email = request.form["email"]
			password = request.form["password"]
			saldo = request.form["saldo"]
			if email in members:
				flash("Email Already Exist!")
				return redirect("/admin/register")
			elif not username:
				flash(Markup("Invalid Username"))
				return redirect("/admin/register")
			elif not email:
				flash(Markup("Invalid Email"))
				return redirect("/admin/register")
			elif not password:
				flash(Markup("Invalid Password"))
				return redirect("/admin/register")
			elif not saldo:
				flash(Markup("Invalid Saldo"))
				return redirect("/admin/register")
			else:
				db.execute("INSERT INTO userz (username,email,password,saldo) VALUES (%s,%s,%s,%s);", (username,email,password,saldo))
				flash(Markup(f"<strong>Register Sukses!</strong><br>Username: {username}<br>Email: {email}<br>Password: {password}<br>Saldo: {saldo}"))
				return redirect("/admin/register")


#MEMBER DASHBOARD
@app.route("/")
@app.route("/home")
def home():
	x = request.cookies.get("auth")
	if not x:
		return redirect("/login")
	else:
		xjs = eval(x)
		username = db.execute("SELECT username FROM userz WHERE email = %s", (xjs["email"])).fetchone()[0]
		trans = db.execute("SELECT * FROM transaksi WHERE username = %s", (username)).fetchall()
		username = db.execute("SELECT username FROM userz WHERE email = %s", (xjs["email"],)).fetchone()[0]
		saldo = db.execute("SELECT saldo FROM userz WHERE email = %s", (xjs["email"],)).fetchone()[0]
		return render_template(templates["index"],nama=username,tipe="Member",servers=str(len(server)),saldo=saldo, trans=trans)

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == "GET":
		x = request.cookies.get("auth")
		if x:
			xjs = eval(x)
			print(xjs)
			username = db.execute("SELECT username FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			return redirect("/home")
		else:
			return render_template(templates["login"])
	else:
		email = request.form["email"]
		password = request.form["password"]
		exist = [z[0] for z in db.execute("SELECT email FROM userz").fetchall()]
		if email not in exist:
			flash(Markup("Email Doesn't Exist, Please <a href='/signup'>Sign Up</a> First"))
			return redirect("/login")
		else:
			pw = db.execute("SELECT password FROM userz WHERE email = %s",(email,)).fetchone()[0]
			if password == pw:
				username = db.execute("SELECT username FROM userz WHERE email = %s",(email,)).fetchone()[0]
				res = make_response(redirect("/home"))
				xc = {"email":email,"password":password}
				res.set_cookie("auth",str(xc))
				return res
			else:
				flash(Markup("Incorrect Password"))
				return redirect("/login")

@app.route("/signup", methods=["GET","POST"])
def signup():
	if request.method == "GET":
		x = request.cookies.get("auth")
		if x:
			return redirect("/home")
		else:
			return render_template(templates["signup"])
	else:
		username = request.form["username"]
		email = request.form["email"]
		password = request.form["password"]
		exist = [z[0] for z in db.execute("SELECT email FROM userz").fetchall()]
		if not username:
			flash(Markup("Invalid Username"))
			return redirect("/signup")
		elif not email:
			flash(Markup("Invalid Email"))
			return redirect("/signup")
		elif not password:
			flash(Markup("Invalid Password"))
			return redirect("/signup")
		elif email in exist:
			flash(Markup("Email Already Exist"))
			return redirect("/signup")
		else:
			db.execute("INSERT INTO userz (username,email,password) VALUES (%s,%s,%s);", (username,email,password,))
			flash(Markup("Signup Success, Please <a href='/login'>Log In</a>"))
			return render_template(templates["signup"])

@app.route("/ssh/buat", methods=["GET","POST"])
def sshBuat():
	print(server)
	if request.method == "GET":
		x = request.cookies.get("auth")
		if x:
			xjs = eval(x)
			username = db.execute("SELECT username FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
		else:
			return redirect("/login")
	elif request.method == "POST":
		x = request.cookies.get("auth")
		if x:
			xjs = eval(x)
			username = db.execute("SELECT username FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			saldo = db.execute("SELECT saldo FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			if int(saldo) <= 0:
				flash(Markup("Saldo Kamu Dibawah 0, Tidak Bisa Membuat Akun!!"))
				return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
			else:
				user = request.form["username"]
				pw = request.form["password"]
				serverv = request.form.get("server").split(",")
				exp = request.form.get("exp")
				salkur = int(serverv[1]) * int(exp)
				if int(saldo) < int(salkur):
					flash(Markup("Saldo Tidak Cukup"))
					return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
				elif not user:
					flash(Markup("Username Tidak Dapat Kosong"))
					return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
				elif not pw:
					flash(Markup("Password Tidak Dapat Kosong"))
					return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
				else:
					x = requests.get("http://"+serverv[0]+f":6969/adduser/exp?user={user}&password={pw}&exp={exp}")
					if x.text == "success":
						db.execute("UPDATE userz SET saldo = %s WHERE email = %s", (str(int(saldo) - int(salkur)), xjs["email"]))
						exp = datetime.datetime.today() + datetime.timedelta(days=int(exp))
						exp = exp.strftime("%Y-%m-%d")
						expd = "{:%B %d, %Y}".format(datetime.datetime.strptime(str(exp),"%Y-%m-%d"))
						db.execute("INSERT INTO transaksi (username,tanggal,akun,harga,status) VALUES (%s,%s,%s,%s,%s)", (username, expd, "Akun SSH", salkur, "Sukses") )
						flash(Markup(f"""<strong>Premium SSH Account<br>
—<br>
Hostname: {serverv[0]}<br>
Username: {user}<br>
Password: {pw}<br>
Expiry: {expd}<br>
—<br>
Port Info:<br>
Websocket SSL: 443<br>
Websocket HTTP: 80<br>
Dropbear: 993, 445<br>
OpenSSH: 22<br>
SSL/TLS: 443, 777<br>
—<br>
Websocket Payload:<br>
GET / HTTP/1.1[crlf]Host: {serverv}[crlf]Connection: Upgrade[crlf][crlf]</strong>"""))
						return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)
					else:
						flash(Markup("Username Already Exist"))
						return render_template(templates["sshbuat"],nama=username,tipe="Member",serverz=server)


@app.route("/ssh/trial", methods=["GET","POST"])
def sshTrial():
	if request.method == "GET":
		x = request.cookies.get("auth")
		if x:
			xjs = eval(x)
			username = db.execute("SELECT username FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)
		else:
			return redirect("/login")
	elif request.method == "POST":
		x = request.cookies.get("auth")
		if x:
			xjs = eval(x)
			username = db.execute("SELECT username FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			saldo = db.execute("SELECT saldo FROM userz WHERE email = %s",(xjs["email"],)).fetchone()[0]
			if int(saldo) <= 0:
				flash(Markup("Saldo Kamu Dibawah 0, Tidak Bisa Membuat Trial"))
				return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)
			else:
				user = request.form["username"]
				pw = request.form["password"]
				serverv = request.form.get("server").split(",")[0]
				if not user:
					flash(Markup("Username Tidak Dapat Kosong"))
					return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)
				elif not pw:
					flash(Markup("Password Tidak Dapat Kosong"))
					return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)
				else:
					exp = "1"
					today = DT.date.today()
					later = today + DT.timedelta(days=1)
					expz = later.strftime("%Y-%m-%d")
					expd = "{:%B %d, %Y}".format(datetime.datetime.strptime(str(expz),"%Y-%m-%d"))
					db.execute("INSERT INTO transaksi (username,tanggal,akun,harga,status) VALUES (%s,%s,%s,%s,%s)", (username, expd, "Trial SSH", "0", "Sukses") )
					x = requests.get("http://"+serverv+f":6969/adduser/exp?user={user}&password={pw}&exp={exp}")
					if x.text == "success":
						msg = f"""
*** Hostname:** `{serverv}`
**• Username:** `{user}`
**• Password:** `{pw}`
**• Expiry:** `{exp}`
━━━━━━━━━━━━━━━━
**– Port Info:**
**• Websocket SSL:** `443`
**• Websocket HTTP:** `80`
**• Dropbear:** `993, 445`
**• OpenSSH:** `22`
**• SSL/TLS:** `443, 777`
━━━━━━━━━━━━━━━━
**– Websocket Payload:**
`GET / HTTP/1.1[crlf]Host: {serverv}[crlf]Connection: Upgrade[crlf][crlf]`
━━━━━━━━━━━━━━━━

"""
						flash(Markup(f"""<strong>Trial SSH Account<br>
<hr><br>
Hostname: {serverv}<br>
Username: {user}<br>
Password: {pw}<br>
Expiry: {expd}<br>
<hr><br>
Port Info:<br>
Websocket SSL: 443<br>
Websocket HTTP: 80<br>
Dropbear: 993, 445<br>
OpenSSH: 22<br>
SSL/TLS: 443, 777<br>
<hr><br>
Websocket Payload:<br>
GET / HTTP/1.1[crlf]Host: {serverv}[crlf]Connection: Upgrade[crlf][crlf]</strong>"""))
						return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)
					else:
						flash(Markup("Username Already Exist"))
						return render_template(templates["sshtrial"],nama=username,tipe="Member",serverz=server)

