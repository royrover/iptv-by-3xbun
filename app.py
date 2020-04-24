from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///channel.db'
db = SQLAlchemy(app)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(32), nullable=False)
    url = db.Column(db.Text, nullable=False)
    logo = db.Column(db.Text)
    status = db.Column(db.String(4), nullable=False, default='Alive')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Channel {}: {}>'.format(self.id, self.channel)
    

@app.route('/')
def index():
    m3u_link = "https://raw.githubusercontent.com/3xbun/WLSIL-Website/master/iptv"

    channels = Channel.query.order_by(Channel.channel).all()
    return render_template('index.html', m3u_link=m3u_link, channels=channels)

@app.route('/delete/<id>')
def delete(id):
    channel = Channel.query.get(id)
    db.session.delete(channel)
    db.session.commit()

    return redirect(url_for('index'))