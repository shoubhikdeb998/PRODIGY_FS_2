from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'

# Create DB table
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    conn.close()
    return render_template('dashboard.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        if name and position and department:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO employees (name, position, department) VALUES (?, ?, ?)", (name, position, department))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            flash("All fields are required.")
    return render_template('add_employee.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        c.execute("UPDATE employees SET name=?, position=?, department=? WHERE id=?", (name, position, department, id))
        conn.commit()
        return redirect(url_for('dashboard'))
    c.execute("SELECT * FROM employees WHERE id=?", (id,))
    employee = c.fetchone()
    conn.close()
    return render_template('update_employee.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
