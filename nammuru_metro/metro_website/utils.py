import mysql.connector
import pandas as pd
import uuid
from datetime import datetime

def getLineInfo(line_colour):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Saketh$12485",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Call the MySQL procedure
    cursor.callproc('GetLineInfo', (line_colour,))

    # Fetch the result as a table
    result1 = []
    for result_cursor in cursor.stored_results():
        result1 = result_cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Saketh$12485",
        database="metro1"
    )
    cursor = conn.cursor()
    cursor.callproc('GetStationsByLineColor', (line_colour,))

    # Fetch the result as a list of dictionaries
    result2 = []
    for result_cursor in cursor.stored_results():
        result2 = result_cursor.fetchall()

    # Close the cursor and connection
    cursor.close()

    conn.close()

    # Convert the result into a DataFrame for better table-like representation
    line_info = pd.DataFrame(result1, columns=['LINE_ID', 'LINE_COLOUR', 'NUMBER_OF_STATIONS','TOTAL_DISTANCE','RIDERS_YESTERDAY','START_STATION','END_STATION'])
    station_list = pd.DataFrame(result2, columns=['Station_Name'])
    
    return line_info,station_list
    
def getStationInfo(station_name):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Saketh$12485",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Call the MySQL procedure
    cursor.callproc('GetStationInfo', (station_name,))

    # Fetch the result as a table
    result = []
    for result_cursor in cursor.stored_results():
        result = result_cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Convert the result into a DataFrame for better table-like representation
    station_info = pd.DataFrame(result, columns=['station_id', 'station_name', 'start_date','number of platforms','visitors_yesterday'])
    
    return station_info

def generate_card_id():
    # Generate a unique Card_ID using UUID
    card_id = str(uuid.uuid4())
    return card_id

def insert_user_and_rider_card(user_id, user_password, mobile_number, parking_id=None, is_user=1):
    try:
        # Create a MySQL connection
        db_config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "Saketh$12485",
            "database": "metro1"
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Generate a unique Card_ID
        card_id = generate_card_id()

        # Insert into the user table
        user_insert_query = "INSERT INTO user (User_ID, User_Password, MOBILE_NUMBER, Card_ID, Parking_ID, IS_USER) VALUES (%s, %s, %s, %s, %s, %s)"
        
        # Check if parking_id is provided, and if not, set it to -999999
        if parking_id is None:
            parking_id = -999999
        
        user_insert_values = (user_id, user_password, mobile_number, card_id, parking_id, is_user)
        cursor.execute(user_insert_query, user_insert_values)

        # Insert into the rider_card table
        rider_card_insert_query = "INSERT INTO rider_card (Card_ID, Card_Balance, Last_Recharge_Amount, Last_Recharge_Time, Total_Savings, Number_of_Trips, User_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        rider_card_insert_values = (card_id, 0, 0, datetime.now(), 0, 0, user_id)
        cursor.execute(rider_card_insert_query, rider_card_insert_values)

        # Commit the changes
        connection.commit()

        return f"User and Rider Card inserted successfully with Card_ID: {card_id}"

    except mysql.connector.Error as err:
        return f"Error: {err}"

    finally:
        cursor.close()
        connection.close()