import sqlite3
import csv

con = sqlite3.connect("CurrentVoltage.db")
cur = con.cursor()
cur.execute("CREATE TABLE DataTable (DeviceTimeStamp, VL1, VL2,	VL3, IL1 ,IL2 ,IL3 ,VL12 ,VL23 ,VL31 , INUT);") ##If not table is create use this code

with open('CurrentVoltage.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['DeviceTimeStamp'], i['VL1'], i['VL2'], i['VL3'], i['IL1'], i['IL2'], i['IL3'], i['VL12'], i['VL23'], i['VL31'], i['INUT']) for i in dr]

cur.executemany("INSERT INTO DataTable (DeviceTimeStamp, VL1, VL2,	VL3, IL1 ,IL2 ,IL3 ,VL12 ,VL23 ,VL31 , INUT) VALUES(?,?,?,?,?,?,?,?,?,?,?);", to_db)
con.commit()
con.close()

