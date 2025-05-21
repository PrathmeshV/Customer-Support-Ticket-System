from flask import Flask, request, jsonify , render_template
from flask_cors import CORS
from datetime import datetime

import mysql.connector

app = Flask(__name__)
CORS(app)

import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@123",
            database="Ticket_SQL_DB"
        )
        if con.is_connected():
            return con
    except Error as e:
        print(f"MySQL Connection Error: {e}")
        return None


@app.route('/')
def home():
    return render_template('insert_user.html')



@app.route('/insertUser', methods=['POST'])
def insert_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection  error"}), 500
    cursor = db.cursor(dictionary=True)
    try:
        
        cursor.callproc('CheckUserExists', [name, email])
        
        for result in cursor.stored_results():
            user = result.fetchone()

        if user:
            return jsonify({"message": "User exists!", "user": user}), 200
        else:
            return jsonify({"message": "User not found!"}), 404 
       
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        if db and db.is_connected():
            db.close()

@app.route('/submitTicket', methods=['POST'])
def submit_ticket():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    
    category = data.get('category')
   

    if not all([title, description, category]):
        return jsonify({"error": "Missing fields"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection  error"}), 500

    try:
        cursor = db.cursor()
        query = """
            INSERT INTO Ticket (title, description,  category) 
            VALUES (%s, %s, %s )
        """
        cursor.execute(query, (title, description, category))
        db.commit()
        return jsonify({"message": "Ticket submitted successfully!"}), 200

    except Exception as e:
        print(f"Submit Ticket error: {str(e)}")
        return jsonify({"error": "Failed to submit ticket"}), 500
    finally:
        if db and db.is_connected():
            db.close()


@app.route('/updateTicketStatus', methods=['POST'])
def update_ticket_status():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    new_status = data.get('status')
    emp_id = data.get('emp_id')
    category = data.get('category')

    if not all([ticket_id, new_status, emp_id, category]):
        db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection   error"}), 500
    cursor = db.cursor()

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection error"}), 500
    cursor = db.cursor()
    try:
        # 1. Update ticket table
        update_ticket_query = """
            UPDATE ticket
            SET status = %s
            WHERE ticket_id = %s
        """
        cursor.execute(update_ticket_query, (new_status, ticket_id))
        
        # 2. Insert into admin_action_log
        insert_log_query = """
        db.commit()
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_log_query, (emp_id, ticket_id, category, new_status, datetime.now()))

        db.commit()

        return jsonify({"message": "Ticket status updated and action logged successfully!"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()


from flask import session

@app.route('/getDashboardData', methods=['GET'])
def get_dashboard_data():
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.id AS user_id,
                u.name AS userName,
                u.email,
                t.ticket_id,
                t.title,
                t.priority,
                t.category,
                t.status
            FROM user1 u
            JOIN ticket t ON u.id = t.user_id
           
        """)
        #  WHERE u.id = user_id
        result = cursor.fetchall()
        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Dashboard data fetch failed"}), 500

    finally:
        db.close()


@app.route('/submitFeedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()

    
    rating = data.get('rating')
    comments = data.get('comments', '')

    if not  rating:
        return jsonify({"error": "Missing  rating"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        query = "INSERT INTO Feedback ( rating, comment) VALUES (%s, %s)"
        cursor.execute(query, ( rating, comments))
        db.commit()
        return jsonify({"message": "Feedback submitted successfully!"}), 200

    except Exception as e:
        print(f"Feedback submit error: {str(e)}")
        return jsonify({"error": "Failed to submit feedback"}), 500
    finally:
        if db and db.is_connected():
            db.close()

@app.route('/getTicketsForAdmin', methods=['post'])
def get_tickets_for_admin():
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                t.ticket_id,
                t.title,
                t.description,
                t.category,
                t.status,
                u.name AS userName
            FROM ticket t
            JOIN user1 u ON t.user_id = u.id
        """)
        result = cursor.fetchall()
        return jsonify(result), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Dashboard data fetch failed"}), 500

    finally:
        db.close()

@app.route('/updateTicketStatusV2', methods=['POST'])
def update_ticket_status_v2():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    new_status = data.get('status')
    emp_id = data.get('emp_id')
    category = data.get('category')

    if not all([ticket_id, new_status, emp_id, category]):
        return jsonify({"error": "Missing fields"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection error"}), 500

    try:
        cursor = db.cursor()
        # Update ticket status
        update_ticket_query = """
            UPDATE ticket
            SET status = %s
            WHERE ticket_id = %s
        """
        cursor.execute(update_ticket_query, (new_status, ticket_id))

        # Insert into admin_action_log
        insert_log_query = """
            INSERT INTO admin_action_log (emp_id, ticket_id, category, action, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_log_query, (emp_id, ticket_id, category, new_status, datetime.now()))

        db.commit()

        return jsonify({"message": "Ticket status updated and action logged successfully!"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        if db and db.is_connected():
            db.close()


if __name__ == '__main__':
    print("Server is running on port 5000")
    app.run(debug=True)