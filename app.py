from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import scheduling_algorithm
import traceback

app = Flask(__name__)
app.config['DATABASE'] = 'your_database.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            case_type = request.form['case_type']
            last_hearing_date = request.form['last_hearing_date']

            db = get_db()
            cursor = db.cursor()

            # Insert data into the 'cases' table
            cursor.execute('INSERT INTO cases (case_type, last_hearing_date) VALUES (?, ?)',
                           (case_type, last_hearing_date))
            db.commit()

            # Retrieve all cases from the database
            cursor.execute('SELECT case_type, last_hearing_date FROM cases')
            previous_cases = cursor.fetchall()

            return render_template('index.html', schedule=scheduling_algorithm.schedule_case(case_type, last_hearing_date),
                                   previous_cases=previous_cases)

    except Exception as e:
        traceback.print_exc()
        return f"An error occurred: {e}"

    return render_template('index.html', schedule=None, previous_cases=None)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
