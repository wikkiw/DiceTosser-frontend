from flask import Flask, render_template, jsonify
import mysql.connector
import json

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'm7porHiFaNET4tja',
    'host': '10.5.32.16',
    'database': 'dicetoss'
}

TOSS_TABLE = "toss"
STATS_TABLE = "stats"

def init_stats(cnx):

    delete = "DELETE FROM " + STATS_TABLE
    insert = "INSERT INTO " + STATS_TABLE + " (toss, count) VALUES (%s, %s)"

    cursor = cnx.cursor()

    try:
        cursor.execute(delete)
        for char in ('A','B','C','D','E','F','X'):
            cursor.execute(insert, (char, 0))
    # just in case
    except mysql.connector.Error as e:
        print(e)

    cnx.commit()
    cursor.close()

    return

def delete_tosses(cnx):
    delete = "DELETE FROM " + TOSS_TABLE
    cursor = cnx.cursor()

    try:
        cursor.execute(delete)
    # just in case
    except mysql.connector.Error as e:
        print(e)

    cnx.commit()
    cursor.close()

    return

@app.route('/remove-data', methods=['POST'])
def remove_data():
    # Here, you would add your logic to remove data. For example:
    try:
        conn = get_db_connection()
        delete_tosses(conn)
        init_stats(conn)
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT toss, count FROM stats")
    result = cursor.fetchall()
    data = {row['toss']: row['count'] for row in result}
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    #conn = get_db_connection()
    app.run(debug=True)
    #conn.close()
