from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    m3u_link = "https://raw.githubusercontent.com/3xbun/WLSIL-Website/master/iptv"
    return render_template('index.html', m3u_link=m3u_link)