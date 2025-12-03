import mysql.connector
import socket

def debug(msg):
    print(f"[DEBUG] {msg}")

def get_db_connection():
    try:
        debug("STEP 1: Starting DB connection process...")

        # ---- RAW TCP CONNECT TEST ----
        debug("Testing raw TCP socket connection to 34.46.122.35:3306...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("34.46.122.35", 3306))
        debug("✓ Raw TCP connection successful (port 3306 reachable)")
        sock.close()

        # ---- MYSQL CONNECT ----
        debug("STEP 2: Calling mysql.connector.connect()…")
        conn = mysql.connector.connect(
            host="34.46.122.35",
            user="toyuser",
            password="ToyUser123!",
            database="toy_store_db",
            ssl_disabled=True,
            connection_timeout=5
        )

        debug("✓ mysql.connector.connect() returned successfully")
        return conn

    except mysql.connector.Error as err:
        debug(f"MYSQL CONNECTOR ERROR: {err}")
        return None

    except Exception as e:
        debug(f"GENERAL ERROR: {e}")
        return None

def insert_order(product_id, quantity, price):
    try:
        conn = get_db_connection()
        if not conn:
            return False, "DB connection failed"

        cursor = conn.cursor()

        total = price * quantity

        cursor.execute("""
            INSERT INTO orders (product_id, quantity, price, total)
            VALUES (%s, %s, %s, %s)
        """, (product_id, quantity, price, total))

        conn.commit()
        cursor.close()
        conn.close()

        return True, "Order stored successfully"

    except Exception as e:
        return False, str(e)
