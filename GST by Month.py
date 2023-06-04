import psycopg2
import datetime
import os
from decimal import Decimal

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

year = datetime.datetime.now().year
month = input('Enter the month: ')

query = "SELECT cash, eftpos FROM daily WHERE EXTRACT(YEAR FROM day) = %s AND EXTRACT(MONTH FROM day) = %s"
val = (year, month)
records = getrecords(query, val)
totalcash = 0
totaleftpos = 0
for record in records:
    totalcash = totalcash + record[0]
    totaleftpos = totaleftpos + record[1]
rawgst = (totalcash + totaleftpos) * Decimal(0.15)
gst = round(rawgst, 2)
print("Cash total: ", totalcash)
print("Eftpos total: ", totaleftpos)
print("GST total: ", gst)