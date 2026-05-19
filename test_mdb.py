import pyodbc

path = r"D:\2.Security & hack & Tools\database-telegram\irancell\936-2.mdb"

conn = pyodbc.connect(
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={path};"
)

cursor = conn.cursor()

for row in cursor.tables(tableType="TABLE"):
    print(row.table_name)

conn.close()
