import psycopg2
import datetime
import os
import re

# DB
sqluser = os.environ["POSTGRE_USER"]
sqlpass = os.environ["POSTGRE_PASS"]
db = psycopg2.connect(
    dbname = "ParadiseCoffee",
    user = sqluser,
    password = sqlpass,
    host = "localhost",
    port = "5432"
)
# Query - SELECT
def getrecords(query, val):
    cursor = db.cursor()
    cursor.execute(query, val)
    records = cursor.fetchall()
    cursor.close()
    return records
# Query - UPDATE/INSERT/DELETE
def changerecords(query, val):
    cursor = db.cursor()
    cursor.execute(query, val)
    db.commit()
    cursor.close()
# Query - No variables
def fixrecords(query):
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    cursor.close()
# Current date in YYYY-MM-DD format
rawdate = datetime.datetime.now()
currentdate = rawdate.strftime('%Y-%m-%d')
def inputvalues(insert):
    strcash = input("Enter the cash total for today: ")
    cash = float(strcash)
    strelectronic = input("Enter the eftpos total for today: ")
    electronic = float(strelectronic)
    if insert: 
        query = "INSERT INTO daily (cash, eftpos, day) VALUES (%s, %s, %s)"
        val = (cash, electronic, currentdate)
        changerecords(query, val)
    else:
        query = "UPDATE daily SET cash = %s, eftpos = %s WHERE day = %s"
        val = (cash, electronic, currentdate)
        changerecords(query, val)

# Check if daily have already been added
query = "SELECT * FROM daily WHERE day = %s"
val = (currentdate,)
records = getrecords(query, val)
insert = True

# Run
if len(records) > 0:
    print("You have already added today's totals, this will change them.")
    insert = False
    inputvalues(insert)
else: 
    inputvalues(insert)

print("Daily totals have been updated.")
db.close()

