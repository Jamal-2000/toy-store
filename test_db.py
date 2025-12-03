from db import get_db_connection, debug

debug("TEST FILE STARTED")
debug("Calling get_db_connection()...")

conn = get_db_connection()

if conn:
    debug("SUCCESS: Connected to database!")
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    debug(f"DB TIME: {result}")
    conn.close()
else:
    debug("FINAL RESULT: FAILED to connect to database.")
