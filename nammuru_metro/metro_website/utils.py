import mysql.connector
import pandas as pd
import uuid
from datetime import datetime,timedelta
import qrcode
from io import BytesIO
import networkx as nx
import random
import string
from twilio.rest import Client

def getLineInfo(line_colour):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
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
        password="pass",
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
        password="pass",
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
    station_info = pd.DataFrame(result, columns=['station_id', 'station_name', 'start_date','number_of_platforms','visitors_yesterday'])
    
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
            "password": "pass",
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
        
def find_routes(start_station, end_station):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = db.cursor()

    # Fetch data from the MySQL table (replace 'your_table' with your table name)
    query = "SELECT start_station, end_station, price, duration FROM route"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Create a directed graph to represent the stations and connections
    G = nx.DiGraph()

    for row in rows:
        G.add_edge(row[0], row[1], price=row[2], duration=row[3])

    # Find all simple paths between the start and end station
    all_paths = list(nx.all_simple_paths(G, source=start_station, target=end_station))

    path_details = []

    # Calculate details for each path
    for path in all_paths:
        total_price = 0
        
        from datetime import datetime
        current_time = datetime.now()
        total_duration = current_time-current_time
        num_stations = len(path) - 1

        for i in range(len(path) - 1):
            total_price += G[path[i]][path[i+1]]['price']
            total_duration += G[path[i]][path[i+1]]['duration']
            if total_price<10:
                total_price=10
        path_details.append({
            "start_station": start_station,
            "end_station": end_station,
            "stations_between": num_stations-1,
            "price": total_price,
            "duration": total_duration,
            "path": path
        })

    cursor.close()
    db.close()

    path_details=pd.DataFrame(path_details)
    return path_details

def fetch_card_details_by_user_id(user_id):
    try:
        # Establish a connection to the local MySQL server
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="pass",
            database="metro1"
        )

        cursor = connection.cursor()

        # Call the stored procedure
        cursor.callproc('FetchCardDetailsByUserID', [user_id])

        # Fetch the results
        for result in cursor.stored_results():
            card_details = result.fetchall()

        # Create a Pandas DataFrame from the fetched data
        if card_details:
            # columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(card_details, columns=["Card_ID","Card_Balance","Last_Recharge_Amount","Last_Recharge_Time","Total_Savings","Number_Of_Trips"])
            return df
        else:
            return("Card doesn't exist .")

    except mysql.connector.Error as err:
        return(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def increment_card_balance(card_id, amount_to_add):
    try:
        # Establish a MySQL database connection
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="pass",
            database="metro1"
        )

        # Create a cursor
        cursor = conn.cursor()

        # Call the stored procedure
        cursor.callproc('IncrementCardBalance', (card_id, amount_to_add))

        # Commit the changes
        conn.commit()
        return(f"Card balance updated successfully for Card_ID {card_id}. Added: ${amount_to_add}")

    except mysql.connector.Error as err:
        return("Error:", err)
    finally:
        cursor.close()
        conn.close()

def check_balance(p_Ticket_Price, p_card_id):
    # Establish a MySQL database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Check if the card has sufficient balance for the ticket
    cursor.execute("SELECT Card_Balance FROM rider_card WHERE Card_ID = %s", (p_card_id,))
    card_balance = cursor.fetchone()

    if card_balance is not None and card_balance[0] >= p_Ticket_Price:
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False

def insert_ticket(p_Ticket_Price, p_Start_Station, p_End_Station, p_Mode_of_Purchase, p_card_id=None):
    # Generate a unique Ticket_ID using uuid
    p_Ticket_ID = str(uuid.uuid4())
    # Default values for Entry_Time and Exit_Time are NULL
    p_Entry_Time = None
    p_Exit_Time = None

    # Set Date_of_Purchase as the current day's date
    p_Date_of_Purchase = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if Start_Station and End_Station are the same
    if p_Start_Station == p_End_Station:
        return "Error: Start and End stations cannot be the same."

    # Check if the purchase mode is 'card'
    if p_Mode_of_Purchase == 'card':
        if not check_balance(p_Ticket_Price, p_card_id):
            return "Error: Insufficient balance on the card for this ticket purchase."

    # Establish a MySQL database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Create a QR code based on Ticket_ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(p_Ticket_ID)
    qr.make(fit=True)

    # Generate the QR code as bytes
    img = qr.make_image(fill_color="black", back_color="white")
    qr_img=img
    qr_code_bytes = BytesIO()
    img.save(qr_code_bytes)
    qr_code_bytes = qr_code_bytes.getvalue()

    # Call the stored procedure to insert the ticket (deduction of balance handled elsewhere)
    try:
        cursor.callproc('InsertTicket', (p_Ticket_ID, p_Ticket_Price, p_Entry_Time, p_Exit_Time, p_Date_of_Purchase, p_Start_Station, p_End_Station, p_Mode_of_Purchase, p_card_id, qr_code_bytes))
        conn.commit()
        li=[]
        li.append(p_Ticket_ID)
        if p_Mode_of_Purchase=="money":
            li.append(qr_code_bytes)
        return li
    except mysql.connector.Error as err:
        return("Error: ", err)
    finally:
        cursor.close()
        conn.close()
        
def get_most_recent_ticket(user_id):
    try:
        # Establish a connection to the MySQL server on localhost
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="pass",
            database="metro1"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Call the MySQL procedure
            cursor.callproc('GetMostRecentTicket', (user_id,))

            # Retrieve the result
            for result in cursor.stored_results():
                data = result.fetchall()
                if data:
                    # Convert the result to a Pandas DataFrame
                    df = pd.DataFrame(data, columns=['Ticket_ID', 'Ticket_Price', 'Entry_Time', 'Exit_Time', 'Date_of_Purchase', 'Start_Station', 'End_Station', 'Mode_of_Purchase', 'QR_Code'])
                    return df

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

    # Return an empty DataFrame if no data is found
    return pd.DataFrame()

def generate_qr_code(data):
    # Generate a QR code from the provided data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = BytesIO()
    img.save(img_bytes)
    return img_bytes.getvalue()

def generate_unique_parking_id():
    # Generate a unique Parking_ID using UUID
    return str(uuid.uuid4())

def insert_parking(station_id, user_id, vehicle_number, fee):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = db.cursor()

    # Generate a unique Parking_ID
    parking_id = generate_unique_parking_id()

    # Generate a default QR Code from the unique Parking_ID
    qr_code = generate_qr_code(parking_id)

    # Get the current timestamp
    timestamp = datetime.now()

    # Set the default status to active
    status = 1

    # Prepare and call the stored procedure
    try:
        cursor.callproc('InsertParking', (parking_id, fee, timestamp, status, qr_code, station_id, user_id, vehicle_number))
        db.commit()
        return "Parking record inserted successfully."
    except Exception as e:
        db.rollback()
        # return f"Error: {e}"
        return -1
    finally:
        cursor.close()
        db.close()

def fetch_parking_details(user_id):
    try:
        # Establish a connection to the local MySQL server
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="pass",
            database="metro1"
        )

        cursor = connection.cursor()

        # Call the stored procedure and pass the user_id as a parameter
        cursor.callproc('FetchParkingDetails', [user_id])

        # Fetch the result from the procedure
        results = cursor.stored_results()
        for result in results:
            rows = result.fetchall()

        # Create a Pandas DataFrame from the fetched data
        if rows:
            # columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows,columns=["Parking_ID","Fee","TimeStamp","Status","QR_Code","Station_id","Vehicle_Number"])
            return df
        else:
            return pd.DataFrame() # ("Parking doesn't exist.")

    except mysql.connector.Error as err:
        return("Error:", err)
    finally:
        cursor.close()
        connection.close()

def check_train_line(start_station, end_station):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = connection.cursor()

    try:
        # Get the Station_ID for the start_station and end_station
        cursor.execute("SELECT Station_ID FROM station WHERE Station_Name = %s", (start_station,))
        start_station_id = cursor.fetchone()

        cursor.execute("SELECT Station_ID FROM station WHERE Station_Name = %s", (end_station,))
        end_station_id = cursor.fetchone()

        if start_station_id and end_station_id:
            start_station_id = start_station_id[0]
            end_station_id = end_station_id[0]

            # Get the Line ID for the start station
            cursor.execute("SELECT Line_ID FROM has_and_part_of WHERE Station_ID = %s", (start_station_id,))
            start_line_id = cursor.fetchone()

            if start_line_id:
                # Check if both stations are part of the same Line_ID
                cursor.execute("SELECT Line_ID FROM has_and_part_of WHERE Station_ID = %s", (end_station_id,))
                end_line_id = cursor.fetchone()

                if end_line_id and start_line_id[0] == end_line_id[0]:
                    # Stations are on the same train line
                    # Get the line name for the start station
                    cursor.execute("SELECT Line_Colour FROM line WHERE Line_ID = %s", (start_line_id[0],))
                    start_line_name = cursor.fetchone()
                    return start_station, start_line_name[0], end_station
                else:
                    # If stations are on different lines, set the end_station to "Nadaprabhu Kempegowda Station, Majestic"
                    cursor.execute("SELECT Line_Colour FROM line WHERE Line_ID = %s", (start_line_id[0],))
                    start_line_name = cursor.fetchone()
                    end_station = "Nadaprabhu Kempegowda Station, Majestic"
                    return start_station, start_line_name[0], end_station

        # Handle cases where station names are not found
        return None, None, None

    finally:
        cursor.close()
        connection.close()

def find_nearest_station(start_station, start_line):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = connection.cursor()

    try:
        # Get the Line_ID corresponding to the provided start_line
        cursor.execute("SELECT Line_ID FROM line WHERE Line_Colour = %s", (start_line,))
        start_line_id = cursor.fetchone()

        if start_line_id:
            start_line_id = start_line_id[0]

            # Create a directed graph
            G = nx.DiGraph()

            # Get all routes from the route table and add them to the graph
            cursor.execute("SELECT START_STATION, END_STATION, DURATION FROM route")
            for row in cursor.fetchall():
                start, end, duration = row
                G.add_edge(start, end, duration=duration.total_seconds())  # Convert duration to seconds

            # Get all stations under the same line from the "has_and_part_of" table
            cursor.execute("SELECT distinct start_station,platform_number FROM schedule WHERE Line_colour = %s", (start_line,))
            same_line_stations_in_schedule = [row for row in cursor.fetchall()]

            # Calculate the shortest duration to reach each station under the same line
            shortest_durations = []
            for station1 in same_line_stations_in_schedule:
                try:
                    station = station1[0]
                    # if start_station=="Nagasandra ":
                    #     start_station="Nagasandra"
                    
                    duration = nx.shortest_path_length(G, source=start_station, target=station, weight='duration')
                    majestic_duration = nx.shortest_path_length(G, source=start_station, target="Nadaprabhu Kempegowda Station, Majestic", weight='duration')
                    majestic_duration_station = nx.shortest_path_length(G, source=station, target="Nadaprabhu Kempegowda Station, Majestic", weight='duration')
                    if duration + majestic_duration == majestic_duration_station:
                        shortest_durations.append([station1, duration])
                except nx.NetworkXNoPath:
                    # If there is no path, it's not reachable
                    pass

            return shortest_durations

    finally:
        cursor.close()
        connection.close()

def display_updated_durations(schedule_updates, min_time):
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="127.0.1.1",
        user="root",
        password="pass",
        database="metro1"
    )

    try:
        data = []

        for update in schedule_updates:
            station , duration_seconds = update
            station_name = station[0]
            platform_number = station[1]
            cursor = connection.cursor()
            # Fetch rows from the schedule table where the start station matches the station name in the list and time is greater than min_time
            cursor.execute("SELECT * FROM schedule WHERE START_STATION = %s AND time_of_arrival >= %s", (station_name, min_time))
            schedule_rows = cursor.fetchall()
            cursor.close()

            if schedule_rows:
                for row in schedule_rows:
                    # Calculate the updated duration
                    current_duration = row[2]  # Assuming that the current duration is stored in the third column
                    updated_duration = current_duration + timedelta(seconds=duration_seconds)

                    # Convert the updated duration to hh:mm:ss format
                    hours, remainder = divmod(updated_duration.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                    data.append((platform_number, duration_str))

        if data:
            # Create a DataFrame and rename the duration column to "time"
            df = pd.DataFrame(data, columns=["Platform", "time"])
            df.sort_values(by="time", inplace=True)

            return df

        return None

    finally:
        connection.close()

def main_function(start_station, end_station, min_time):
    # Step 1: Check the train line
    start_station, start_line, end_station = check_train_line(start_station, end_station)

    # Step 2: Find the nearest station
    shortest_durations = find_nearest_station(start_station, start_line)

    # Step 3: Display updated durations
    updated_durations = display_updated_durations(shortest_durations, min_time)

    # return start_station, start_line, end_station, updated_durations
    return updated_durations

def login_procedure(user_id, user_password):
    try:
        # Establish a connection to the local MySQL server
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="pass",
            database="metro1"
        )

        cursor = connection.cursor(buffered=True)

        # Call the stored procedure to check user credentials and retrieve information
        cursor.callproc('CheckUserCredentials', [user_id, user_password])
        connection.commit()

        # Fetch the result
        for result in cursor.stored_results():
            result_set = result.fetchall()
            if result_set:
                row = result_set[0]
                if 'Invalid Credentials' not in row:
                    user_id = row[0]  # Assuming the email address is the same as the username.
                    phone_number = row[1]
                    is_user = row[2]
                    phone_number = '+91' + str(phone_number)
                    # Generate an OTP
                    # otp = generate_otp()

                    # Send OTP via Gmail
                    # send_otp_via_sms(phone_number,otp)
                    
                    return user_id, is_user
                else:
                    return "Invalid Credentials", None, None

    except mysql.connector.Error as err:
        return str(err), None, None
    finally:
        cursor.close()
        connection.close()

def update_exit_time(ticket_id):
    # Establish a MySQL database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Check if Entry_Time exists for the specified ticket
    entry_time_query = "SELECT Entry_Time FROM ticket WHERE Ticket_ID = %s"
    cursor.execute(entry_time_query, (ticket_id,))
    entry_time = cursor.fetchone()
    if entry_time == (None,):
        return("Error: Entry_Time is not set for Ticket_ID:", ticket_id)

    # Get the current time
    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Call the stored procedure to update the Exit_Time
    try:
        cursor.callproc('UpdateExitTime', (ticket_id, exit_time))
        conn.commit()
        return("Exit time updated successfully for Ticket_ID:", ticket_id)
    except mysql.connector.Error as err:
        return("Error: ", err)
    finally:
        cursor.close()
        conn.close()
        
def update_entry_time(ticket_id):
    # Get the current time
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Establish a MySQL database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    # Create a cursor
    cursor = conn.cursor()

    # Call the stored procedure to update the Entry_Time
    try:
        cursor.callproc('UpdateEntryTime', (ticket_id, entry_time))
        conn.commit()
        return("Entry time updated successfully for Ticket_ID:", ticket_id)
    except mysql.connector.Error as err:
        # return("Error: ", err)
        return -1
    finally:
        cursor.close()
        conn.close()

def update_parking_status(parking_id):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = db.cursor()

    # Set the new status to "completed"
    new_status = 0

    # Prepare and execute the SQL update query
    try:
        update_query = "UPDATE parking SET Status = %s WHERE Parking_ID = %s"
        cursor.execute(update_query, (new_status, parking_id))
        db.commit()
        return "Parking record status updated to 'completed' successfully."
    except Exception as e:
        db.rollback()
        return f"Error: {e}"
    finally:
        cursor.close()
        db.close()












        
# def generate_otp():
#     digits = string.digits
#     otp = ''.join(random.choice(digits) for _ in range(6))
#     return otp

# def send_otp_via_sms(phone_number, otp):
#     account_sid = 'AC53cbce7e65f2914a4e0c9682269d66c5'
#     auth_token = 'fea8f9651055e72642cd6a12d777d5fb'
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         to=phone_number,
#         from_='+12512570659',
#         body=f'Your OTP is: {otp}'
#     )
    
def retrieve_ticket_details(start_time, end_time, input_date):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="pass",
        database="metro1"
    )

    cursor = connection.cursor()

    card_data = []
    money_data = []

    try:
        cursor.callproc('DisplayTicketDetails', (start_time, end_time, input_date))

        for result in cursor.stored_results():
            data = result.fetchall()
            columns = result.description
            card_data.extend([row for row in data if isinstance(row[1], str)])
            money_data.extend([row for row in data if not isinstance(row[1], str)])

        card_table = pd.DataFrame(card_data, columns=[col[0] for col in columns])
        money_table = pd.DataFrame(money_data, columns=[col[0] for col in columns])

        return card_table, money_table

    except mysql.connector.Error as error:
        print("Error retrieving data:", error)
        return None
    finally:
        cursor.close()
        connection.close()