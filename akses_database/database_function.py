import mysql.connector
import datetime

your_database_pass = "<your_password>"

def create_database():
    db = mysql.connector.connect(
        host = 'localhoxst',
        user = 'root',
        passwd = 'your_database_pass',
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS reminderDatabase")
    db.commit()
    mycursor.close() 
    db.close()

def create_table():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, name text, password text)")
    mycursor.execute("CREATE TABLE IF NOT EXISTS events (name text, date text, title text, content text)")
    db.commit()
    mycursor.close() 
    db.close()

def insert_user(name:str, password:str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor = db.cursor()

    mycursor.execute("INSERT INTO users (name,password) VALUES(%s, %s)", (name, password,))
    db.commit()
    mycursor.close() 
    db.close()
    
def get_user(name: str) -> list :
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE name=%s", (name,))
    result = mycursor.fetchall()
    
    return [result[0][i] for i in range(3)]

def get_user_name_all() -> list :
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = 'reminderDatabase'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM users")
    result = mycursor.fetchall()
    
    return [result[i][1] for i in range(len(result))]

def check_data(name: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor = db.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE name=%s", (name,))
    counter = 0 
    for i in mycursor:
        counter += 1
    if counter == 0:
        return 0
    else:
        return 1
    
def insert_event(name: str, date: str, title: str, content: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor = db.cursor()

    mycursor.execute(f"INSERT INTO events (name,date,title,content) VALUES(%s, %s, %s, %s)", (name, date, title, content,))
    db.commit()
    mycursor.close() 
    db.close()  

def is_available(date_id: str):
    now_date_id = str(datetime.date.today())
    array_1 = now_date_id.split('-') # 'dd-mm-yyyy'
    array_2 = date_id.split('/')

    if (int(array_2[2]) > int(array_1[0])):
        return True
    elif (int(array_2[2]) == int(array_1[0]) and int(array_2[0]) > int(array_1[1])):
        return True
    elif (int(array_2[2]) == int(array_1[0])) and (int(array_2[0]) == int(array_1[1]) and int(array_2[1]) >= int(array_1[2])):
        return True
    return False

def get_events(name: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = 'reminderDatabase'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM events WHERE name=%s", (name,))
    result = mycursor.fetchall()

    return [[result[i][j] for j in range(4)] for i in range(len(result))]

def update_event():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = 'reminderDatabase'
    )
    mycursor= db.cursor()
    mycursor.execute(f"SELECT * FROM events")
    result = mycursor.fetchall()
    
    date_unavailable = []
    for i in range(len(result)):
        if not is_available(result[i][1]) and not (result[i][1] in date_unavailable):
            date_unavailable += [result[i][1]]
    for date in date_unavailable:
        mycursor.execute(f"DELETE FROM events WHERE date=%s", (date,))
        
    db.commit()
    mycursor.close() 
    db.close()  
    
def delete_event(name: str, date: str, title: str, content: str):
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'your_database_pass',
        database = "reminderDatabase"
    )
    mycursor = db.cursor()

    mycursor.execute(f"DELETE FROM events WHERE name=%s AND date=%s AND title=%s AND content=%s", (name, date, title, content,))
    db.commit()
    mycursor.close() 
    db.close()  

create_database()
create_table()