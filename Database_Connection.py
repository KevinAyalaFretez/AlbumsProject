import pyodbc
 
SERVER = 'DESKTOP-FI30JF2'
DATABASE = 'Albums'
USERNAME = 'DESKTOP-FI30JF2/kevin'
DRIVER = "ODBC Driver 18 for SQL Server"

def get_db_connection():
    """Establish a connection to SQL Server using ODBC."""
    try:
        conn = pyodbc.connect(
           f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            "Trusted_Connection=yes;"
            f'Encrypt=yes;'
            f'TrustServerCertificate=yes;'
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None
 
# def test_connection():
#     conn = get_db_connection()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             sqlquery = "SELECT * FROM Tasks"
#             cursor.execute(sqlquery)
#             results = cursor.fetchall()
#             if results:
#                 for row in results:
#                     print(row)  # Prints each row as a tuple
#             else:
#                 print("No records found in Tasks table.")
#         except Exception as e:
#             print(f"Error during query execution: {e}")
#         finally:
#             conn.close()
#     else:
#         print("Failed to establish a connection.")
 
 
# # Call the test function
# test_connection()