from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret_key'

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pysql"
)
cursor = connection.cursor()

# Create the employee table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        DepartmentID INT,
        Salary DECIMAL(10, 2),
        Email VARCHAR(100)
    )
""")
connection.commit()

# Home page to display employee list
@app.route('/')
def home():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

# Add new employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        salary = request.form['salary']
        email = request.form['email']

        cursor.execute("""
            INSERT INTO employees (FirstName, LastName, DepartmentID, Salary, Email) 
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, department_id, salary, email))
        connection.commit()
        flash('Employee added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add.html')

# Update employee details
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (id,))
    employee = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department_id = request.form['department_id']
        salary = request.form['salary']
        email = request.form['email']

        cursor.execute("""
            UPDATE employees 
            SET FirstName = %s, LastName = %s, DepartmentID = %s, Salary = %s, Email = %s
            WHERE EmployeeID = %s
        """, (first_name, last_name, department_id, salary, email, id))
        connection.commit()
        flash('Employee updated successfully', 'success')
        return redirect(url_for('home'))
    return render_template('update.html', employee=employee)

# Delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    cursor.execute("DELETE FROM employees WHERE EmployeeID = %s", (id,))
    connection.commit()
    flash('Employee deleted successfully', 'success')
    return redirect(url_for('home'))

# View employee details
@app.route('/view/<int:id>')
def view_employee(id):
    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (id,))
    employee = cursor.fetchone()
    return render_template('view.html', employee=employee)

if __name__ == '__main__':
    app.run(debug=True)
