from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from modules import get_desc_cluster, minmax_scaler, predict_cluster, search

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Nama Anda', validators=[DataRequired()])
    days_since_last_purchase = IntegerField('Hari sejak terakhir pembelian', validators=[DataRequired(), NumberRange(min=0, max=None)])
    frequency = IntegerField('Jumlah barang yang dibeli', validators=[DataRequired(), NumberRange(min=0, max=None)])
    amount = IntegerField('Total Harga Pembelian', validators=[DataRequired(), NumberRange(min=0, max=None)])
    submit = SubmitField('Submit')

class MbaNameForm(FlaskForm):
    name_item = StringField('Nama item', validators=[DataRequired()])
    submit = SubmitField('Search')

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        days_slp = form.days_since_last_purchase.data
        freq = form.frequency.data
        amnt = form.amount.data
        normalized_data = minmax_scaler(days_slp, freq, amnt)
        result = predict_cluster(normalized_data)
        return redirect( url_for('cluster', name=name, result=result[0]) )
    return render_template('index.html', form=form, message=message)

@app.route('/cluster/<name>/<result>')
def cluster(name, result):
    days_slp, freq, amnt, cust, label = get_desc_cluster(int(result))
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        return render_template('segmen.html', name=name, label=label, days=days_slp, freq=freq, amount=amnt, total=cust)

@app.route('/mba', methods=['GET', 'POST'])
def mba_index():
    form = MbaNameForm()
    message = ""
    if form.validate_on_submit():
        name_item = form.name_item.data
        return redirect( url_for('res_mba', name=name_item) )
    return render_template('mba.html', form=form, message=message)

@app.route('/res_mba/<name>')
def res_mba(name):
    res = search(name)
    return render_template('mba_res.html', values=res, barang=name)

# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
