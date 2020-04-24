from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import AddChannel

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddChannel()

    if form.validate_on_submit():
        flash('Channal {} added succesfully'. format(form.channel.datra))
        return redirect(url_for('index'))

    return render_template('index.html', title="IPTV by 3xbun", form=form)