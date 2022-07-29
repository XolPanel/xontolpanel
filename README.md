# Getting started
### Step 1
- Fork <a href="https://github.com/XolPanel/xontolpanel">Repo</a> Ini
- Siapkan 1 (atau lebih) VPS Tumbal untuk sesajen (sudah terinstall autoscript vpn)
- Login Ke VPS Tumbal Tadi, copas command Berikut:
```
apt update && apt upgrade -y && curl -O https://raw.githubusercontent.com/XolPanel/xontolpanel/main/api.sh && bash api.sh
```
- simpan `AUTH KEY` untuk dipakai deploy ke herocrot nanti

### Step 2 (Deploy To Heroku)
- Buat Akun Heroku
- Klik Tombol Dibawah
<p align="center"><a href="https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FXolPanel%2Fxontolpanel&template=https%3A%2F%2Fgithub.com%2FXolPanel%2Fxontolpanel"><img src="https://www.herokucdn.com/deploy/button.png" alt="Deploy to Heroku" target="_blank"/></a></img></p>

- NOTE di kolom SERVER, wajib isi 2 SERVER. Contoh: `VPS-ASLI,vps-asli.com,7000;VPS-PALSU,vps-palsu.com,69696`
- klik deploy
- klik Manage App
- Klik `Open App`
- mengbingung / error?, tanya di <a href="https://t.me/XolPanelDC">Di Sini</a>
