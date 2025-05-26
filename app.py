from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql24789',
    'database': 'retail_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM price_tracker ORDER BY updated_at DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', products=data)

@app.route('/add', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    price = request.form['price']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO price_tracker (product_name, price) VALUES (%s, %s)", 
                  (product_name, price))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM price_tracker WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)