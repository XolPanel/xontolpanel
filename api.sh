echo -n "[+] Input Your Auth_Key: "
read AUTH
apt update && apt upgrade -y
apt install python3-pip python3
pip3 install flask
tee -a api.service<<END
[Unit]
Description=My Project
After=network.target

[Service]
WorkingDirectory=/usr/bin
ExecStart=/usr/bin/python3 /usr/bin/api.py 0.0.0.0 $AUTH
Restart=always

[Install]
WantedBy=multi-user.target
END

systemctl start api
systemctl enable api
echo "[+] API Installation Completed."
