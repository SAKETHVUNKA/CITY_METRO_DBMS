import mysql.connector
import pandas as pd

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