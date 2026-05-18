import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=KDB_M;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

cursor.execute("""
SELECT TOP 10
    Name,
    Mobile,
    Tel,
    Address
FROM tblCustomer
""")

for row in cursor.fetchall():
    print(row)

conn.close()
