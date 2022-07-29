### XontolPanel ###
# /etc/systemd/systemd/api.service Example:
'''
[Unit]
Description=My Project
After=network.target
[Service]
WorkingDirectory=/usr/bin
ExecStart=/usr/bin/python3 /usr/bin/api.py 0.0.0.0 YourAuth
Restart=always

[Install]
WantedBy=multi-user.target
'''
# replace 'YourAuth' To whatever you want.
### XontolPanel ####

import os,json
from flask import *
import subprocess, random, re,sys
std = subprocess.PIPE
app = Flask(__name__)
auth = sys.argv[2]

import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

@app.route("/trial-ssh")
def trial_ssh():
	if request.headers.get("AUTH_KEY") == auth:
		trial = subprocess.check_output("echo trial`</dev/urandom tr -dc X-Z0-9 | head -c4`", shell=True).decode("ascii")
		subprocess.check_output(f'useradd -e `date -d "1 days" +"%Y-%m-%d"` -s /bin/false -M {trial}', shell=True)
		subprocess.check_output(f'usermod --password $(echo 1 | openssl passwd -1 -stdin) {trial}', shell=True)
		return trial + ":" + "1"
	else:
		return redirect("http://t.me/XolPanel")

@app.route("/adduser/exp")
def add_user_exp():
	if request.headers.get("AUTH_KEY") == auth:
		u = request.args.get("user")
		p = request.args.get("password")
		exp = request.args.get("exp")
		try:
			subprocess.check_output(f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {u}', shell=True)
			subprocess.check_output(f'usermod --password $(echo {p} | openssl passwd -1 -stdin) {u}', shell=True)
		except:
			return "error"
		else:
			return "success"
	else:
		return redirect("http://t.me/XolPanel")

@app.route("/deluser")
def deluser():
	if request.headers.get("AUTH_KEY") == auth:
		u = request.args.get("user")
		try:
			subprocess.check_output(f'userdel -f {u}', shell=True)
		except:
			return "error"
		else:
			return "success"
	else:
		return redirect("http://t.me/XolPanel")

app.run(host=sys.argv[1], port=6969)
