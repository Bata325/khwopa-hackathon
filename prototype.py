import sqlite3
from twilio.rest import Client

def init_db():
    conn = sqlite3.connect("vehicles.sqlite")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_number TEXT PRIMARY KEY,
            phone_number TEXT NOT NULL
        )
        """
    )
    conn.commit()

    
    try:
        cursor.execute("ALTER TABLE vehicles ADD COLUMN violations INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("'violations' column already exists.")
        else:
            print(f"Error updating schema: {e}")

    conn.close()

def add_vehicle(vehicle_number, phone_number):
    conn = sqlite3.connect("vehicles.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO vehicles(vehicle_number, phone_number) VALUES (?, ?)",
            (vehicle_number, phone_number),
        )
        conn.commit()
        print(f"Vehicle {vehicle_number} added with phone number {phone_number}.")
    except sqlite3.IntegrityError:
        print(f"Vehicle number {vehicle_number} already exists.")
    conn.close()

def get_phone_number(vehicle_number):
    conn = sqlite3.connect("vehicles.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT phone_number FROM vehicles WHERE vehicle_number = ?",
        (vehicle_number,),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def increment_violations(vehicle_number):
    conn = sqlite3.connect("vehicles.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE vehicles SET violations = violations + 1 WHERE vehicle_number = ?",
        (vehicle_number,),
    )
    conn.commit()
    conn.close()

def send_sms(vehicle_number, message, is_followup=False):
    phone_number = get_phone_number(vehicle_number)
    if not phone_number:
        print(f"No phone number found for vehicle {vehicle_number}.")
        return

    
    account_sid = "ACda8bf1e34f96c33c845738c7a8d8663d"
    auth_token = "6fecfb4510e49060fd81148221e2643b"
    twilio_number = "+17753735261"
    client = Client(account_sid, auth_token)

    try:
       
            # Initial SMS
        client.messages.create(
        body=message,
        from_= twilio_number,
        to=phone_number,
        )
        print(f"SMS sent to {vehicle_number}: {message}")
        increment_violations(vehicle_number)

        

    except Exception as e:
        print(f"Failed to send SMS: {e}")

def main():
    init_db()
    while True:
        print("\nChoose an option:")
        print("1. Add a vehicle")
        print("2. Send an SMS")
        print("3. View all vehicles")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            vehicle_number = input("Enter vehicle number: ")
            phone_number = input("Enter phone number: ")
            add_vehicle(vehicle_number, phone_number)

        elif choice == "2":
            vehicle_number = input("Enter vehicle number: ")
            message = input("Enter message to send: ")
            send_sms(vehicle_number, message)

        elif choice == "3":
            conn = sqlite3.connect("vehicles.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            for row in cursor.fetchall():
                print(row)
            conn.close()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
