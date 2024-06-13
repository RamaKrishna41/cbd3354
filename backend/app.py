import os
import psycopg2
import logging
from flask import Flask, request, render_template

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

app = Flask(__name__)

# Use environment variables to configure the database connection
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME')}' "
    f"user='{os.getenv('DB_USER')}' "
    f"password='{os.getenv('DB_PASSWORD')}' "
    f"host='{os.getenv('DB_HOST')}'"
)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Establish a connection to the database
try:
    conn = get_db_connection
    cur = conn.cursor()
    logging.info("Connected to the database successfully.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")

# SQL command to create a table named "users" in the "test" schema
create_table_sql = """
CREATE TABLE IF NOT EXISTS test.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255)
);
"""

try:
    # Execute the SQL command to create the table
    cur.execute(create_table_sql)
    cur.close()
    conn.close()
    logging.info("Table 'users' created successfully.")
except Exception as e:
    logging.error(f"Error creating table 'users': {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        username = request.form['username']
        email = request.form['email']
        cur.execute("INSERT INTO test.users (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Data inserted successfully.")
        return "Submitted!"
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {e}")
        return "Error submitting data. Please try again."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
