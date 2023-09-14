import wtforms.validators
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, DateTimeField, SelectField
from wtforms.validators import DataRequired
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField('Location URL', validators=[DataRequired('Enter valid value please'),
                                                        wtforms.validators.URL()])
    opening_time = StringField('Opening time', validators=[DataRequired('Enter valid value please')])
    closing_time = StringField('Closing time', validators=[DataRequired('Enter valid value please')])
    coffee_rating = SelectField(u'Coffee Rating', validators=[DataRequired('Please select a valid rating.')],
                                choices=[('☕☕☕☕☕',
                                          '☕☕☕☕☕'),
                                         ('☕☕☕☕',
                                          '☕☕☕☕'),
                                         ('☕☕☕',
                                          '☕☕☕'),
                                         ('☕☕',
                                          '☕☕'),
                                         ('☕',
                                          '☕')])
    wifi_rating = SelectField(u'Wi-Fi Rating', validators=[DataRequired('Please select a valid rating.')],
                              choices=[('💪💪💪💪💪',
                                        '💪💪💪💪💪'),
                                       ('💪💪💪💪',
                                        '💪💪💪💪'),
                                       ('💪💪💪',
                                        '💪💪💪'),
                                       ('💪💪',
                                        '💪💪'),
                                       ('💪',
                                        '💪')])
    power_outlet_rating = SelectField(u'Power Outlet Rating',
                                      validators=[DataRequired('Please select a valid rating.')],
                                      choices=[('🔌🔌🔌🔌🔌',
                                                '🔌🔌🔌🔌🔌'),
                                               ('🔌🔌🔌🔌',
                                                '🔌🔌🔌🔌'),
                                               ('🔌🔌🔌',
                                                '🔌🔌🔌'),
                                               ('🔌🔌',
                                                '🔌🔌'),
                                               ('🔌',
                                                '🔌')])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', encoding='utf-8', mode='a') as cafe_form:
            data = f'{form.cafe.data},' \
                   f' {form.location_url.data},' \
                   f' {form.opening_time.data},' \
                   f' {form.closing_time.data},' \
                   f' {form.coffee_rating.data},' \
                   f' {form.wifi_rating.data},' \
                   f' {form.power_outlet_rating}'
            cafe_form.write(data)
        print("True!")
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        rows_without_heading = [i for i in list_of_rows[1:]]
        print(rows_without_heading)
    return render_template('cafes.html', cafes=list_of_rows, cafes_x=rows_without_heading)


if __name__ == '__main__':
    app.run(debug=True)
