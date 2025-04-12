import sqlite3


DB_FILE = "passwords.db"

def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT UNIQUE NOT NULL, username TEXT NOT NULL)")
    con.commit()
    con.close()
    

def add_pass(service_name, username, password = None):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO passwords (service_name, username, password) VALUES (?, ?, ?)", 
                   (service_name, username, password))
        con.commit()
        print(f"Added to db: {service_name}, {username}")
    except sqlite3.IntegrityError as e:
        print(f"Error: {str(e)}")
    finally:
        con.close()
def get_pass(service_name):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("SELECT * FROM passwords WHERE service_name = ?", (service_name,))
    result = cur.fetchone()
    if result:
        print (f"Found the service: {result[1]}, Login={result[2]}")
    else:
        print(f"Not found the service: {service_name}")
    con.close()
    return result

def get_services():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    print("Looking for a list of services in database...")
    cur.execute("SELECT service_name FROM passwords")
    results = cur.fetchall()
    print(f"Found {len(results)} services in database.")
    con.close()
    return [result[0] for result in results]

def list_services():
    services = get_services()
    if services:
        print("\nAvailable Serivices:")
        for i, service in enumerate(services, 1):
            print(f"{i}. {service}")
        return True
    else:
        print("No saved services")
        return False
