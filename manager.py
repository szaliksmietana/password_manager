import sys 
import getpass
import io
import sqlite3
from db import init_db, get_pass, add_pass, get_services, list_services
from crypto import encrypt_data, decrypt_data
from utils import generate_password, copy_clipboard, l1ne

def main():
    init_db()

    while True:
        l1ne()
        print("\nPassword Manager")
        print("\n1. Add password")
        print("\n2. Get password")
        print("\n3. Generate password")
        print("\n4. List of services")
        print("\n5. Exit")

        choice = input("\nChoose option: ")
        
        match choice:
            case "1":
                l1ne()
                service_name=input("Service name: ")
                username=input("Login: ")
                password = getpass.getpass("Password: ")
                try:
                    old_data = decrypt_data()
                    if not old_data:
                        old_data = ""
                except Exception as e:
                    print(f"Info: Creating a new encrypted file ({str(e)})")
                    old_data = ""
                
                new_data = old_data + f"{service_name} | {username} | {password}\n"
                encrypt_data(new_data)
                
                try:
                    add_pass(service_name, username)
                    print("Password saved!")
                except sqlite3.IntegrityError:
                    print("Service already exists in the database!")

            case "2":
                l1ne()
                if list_services():
                    selection = input("\nEnter service name or number: ")
                    
                    services = get_services()

                    if selection.isdigit() and 1 <= int(selection) <= len(services):
                        service_name = services[int(selection)-1]
                    else:
                        service_name = selection
                else:
                    service_name = input("Enter service name: ")
                
                entry = get_pass(service_name)

                if entry:
                    try:
                        data = decrypt_data()
                        found = False
                        for line in data.split("\n"):
                            if line and service_name in line.split("|")[0].strip():
                                password = line.split("|")[-1].strip()
                                copy_clipboard(password)
                                print(f"Password for {service_name} copied to clipboard!")
                                found = True
                                break
                        
                        if not found:
                            print("Password not found in encrypted storage.")
                    except Exception as e:
                        print(f"Error decrypting data: {str(e)}")
                else:
                    print("There is no such service in the database.")
                    
            case "3":
                l1ne()
                length = int(input("Length of password: "))
                password = generate_password(length)
                print(f"Generated {password} pasted to the clipboard!")
                copy_clipboard(password)

            case "4":
                list_services()

            case "5": 
                print("Bye!")
                sys.exit()

            case _:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()