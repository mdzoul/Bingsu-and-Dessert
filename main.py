from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired
import csv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    opening = StringField('Opening Time e.g. 8:00AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    dessert = SelectField('Dessert Rating',
                          choices=['🍧', '🍧🍧', '🍧🍧🍧', '🍧🍧🍧🍧', '🍧🍧🍧🍧🍧'],
                          validators=[DataRequired()])
    ambience = SelectField('Ambience Rating',
                           choices=['👍', '👍👍', '👍👍👍', '👍👍👍👍👍', '👍👍👍👍👍'],
                           validators=[DataRequired()])
    seats = SelectField('Seats Availability',
                        choices=['🪑', '🪑🪑', '🪑🪑🪑', '🪑🪑🪑🪑', '🪑🪑🪑🪑🪑'],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = form.data
        keys_to_remove = ['submit', 'csrf_token']
        for k in keys_to_remove:
            form_data.pop(k)
        with open('cafe-data.csv', 'a') as csv_file:
            csv_data = csv.writer(csv_file)
            csv_data.writerow(form_data.values())
        return redirect('/cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
