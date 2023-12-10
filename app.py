from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc1234!'
app.config['MYSQL_DB'] = 'flaskcontacts'
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize MySQL connection
mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contacts')
        data = cur.fetchall()
        cur.close()
        return render_template('index.html', contacts=data)
    except Exception as e:
        print(f"Error querying contacts: {str(e)}")
        return 'An error occurred while fetching contacts.'

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO contacts(fullname, phone, email) VALUES(%s, %s, %s)', (fullname, phone, email))
            mysql.connection.commit()
            flash('Contact Added Successfully')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error adding contact: {str(e)}")
            return f'An error occurred while adding the contact. Error details: {str(e)}'

@app.route('/edit/<id>')
def edit_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
        data = cur.fetchall()
        cur.close()
        print(data[0])
        return render_template('edit-contact.html', contact=data[0])
    except Exception as e:
        print(f"Error editing contact: {str(e)}")
        return 'An error occurred while editing the contact.'

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
    """, (fullname, email, phone, id))
    mysql.connection.commit()    
    flash('Contact Updated Successfully')
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM contacts WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Contact Removed Successfully')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting contact: {str(e)}")
        return 'An error occurred while deleting the contact.'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
