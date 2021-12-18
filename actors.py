from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from data import ACTORS
from modules import get_desc_cluster, get_names, get_actor, get_id, minmax_scaler, predict_cluster

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
    name = StringField('Nama item', validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below

@app.route('/', methods=['GET', 'POST'])
def index():
    # names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    # form = NameForm()
    # message = ""
    # if form.validate_on_submit():
    #     name = form.name.data
    #     if name.lower() in names:
    #         # empty the form field
    #         form.name.data = ""
    #         id = get_id(ACTORS, name)
    #         # redirect the browser to another route and template
    #         return redirect( url_for('actor', id=id) )
    #     else:
    #         message = "That actor is not in our database."
    # return render_template('index.html', names=names, form=form, message=message)
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

#@app.route('/actor/<id>')
#def actor(id):
@app.route('/cluster/<name>/<result>')
def cluster(name, result):
    # run function to get actor data based on the id in the path
    #id, name, photo = get_actor(ACTORS, id)
    days_slp, freq, amnt, cust, label = get_desc_cluster(int(result))
    if name == "Unknown":
        # redirect the browser to the error template
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', name=name, label=label, days=days_slp, freq=freq, amount=amnt, total=cust)

@app.route('/mba', methods=['GET', 'POST'])
def mba_index():
    form = MbaNameForm()
    message = ""
    if form.validate_on_submit():
        name_item = form.name_item.data
        pass
    return render_template('mba.html', form=form, message=message)

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
