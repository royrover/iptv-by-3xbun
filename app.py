from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from pythainlp.util import thai_strftime

app = Flask(__name__, static_url_path='')
app.jinja_env.globals['thai_strftime'] = thai_strftime
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///channel"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(32), nullable=False)
    url = db.Column(db.Text, nullable=False)
    logo = db.Column(db.Text)
    status = db.Column(db.String(4), nullable=False, default='Alive')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Channel {}: {}>'.format(self.id, self.channel)
    

@app.route('/')
def index():
    m3u_link = "https://raw.githubusercontent.com/3xbun/WLSIL-Website/master/iptv"

    channels = Channel.query.order_by(Channel.channel).all()
    return render_template('index.html', m3u_link=m3u_link, channels=channels)

@app.route('/delete/<id>')
def delete(id):
    channel = Channel.query.get_or_404(id)
    db.session.delete(channel)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit(id):
    ch = Channel.query.get_or_404(id)

    return render_template('edit.html', ch=ch)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    ch = Channel.query.get_or_404(id)
    ch.channel = request.form['channel']
    ch.url = request.form['url']
    ch.logo = request.form['logo']
    if request.form.get('status') == None: ch.status = 'Dead'
    else: ch.status = 'Alive'
    ch.date_created = datetime.now()

    db.session.commit()

    with open('iptv-by-3xbun', "w") as test:

        channels = Channel.query.all()
        for ch in channels:
            test.write('\n#EXTINF:-1 tvg-logo="{}", {}\n' .format(ch.logo, ch.channel))
            test.write('{}' .format(ch.url))


    return redirect(url_for('edit', id=ch.id))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        channel = request.form['channel']
        url = request.form['url']
        logo = request.form['logo']
        
        if request.form.get('status') == None: status = 'Dead'
        else: status = 'Alive'

        ch = Channel(channel=channel, url=url, logo=logo)
        db.session.add(ch)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/read')
def read():
    with open("iptv-by-3xbun", "r") as f:
        content = f.read()

    return content