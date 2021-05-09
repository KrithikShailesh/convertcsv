from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
import random
import csv
# Create your views here.

def home(request):
    return render(request, "home.html")

def convert(request):
    if request.method == 'GET':
        return render(request, "home.html")
    name=request.POST['filename']
    fileName="csvFile"

    #Open the cs file
    with open(name) as csv_file:
        csvfile=csv.reader(csv_file,delimiter=',')
        header=[]
        row1=[]

        #read a header
        for row in csvfile:
            header=row
            break

        #read the first record for evaluation
        i=0
        for row in csvfile:
            if i==1:
                row1=row
                break
            i=i+1
    datatyperow=[]
    datatype_spec=[]

    #checking the datatypes
    for col in row1:
        if col.isdigit():
            val=" INT(11),"
            spec="%s,"
        elif type(col)==str:
            val=" VARCHAR(100),"
            spec="%s,"
        datatyperow.append(val)
        datatype_spec.append(spec)
    res = [i + j for i , j in zip(header, datatyperow)]
    create_state=""
    create_state=create_state.join(res)
    create_state=create_state[3:-1]
    insert_state=""
    insert_state=insert_state.join(datatype_spec)
    insert_state=insert_state[:-1]

    #declaring header which will be used to insert values into table
    header_str=","
    header_str=header_str.join(header)
    header_str=header_str[3:]
    with open(name) as csv_file:
        csvfile=csv.reader(csv_file,delimiter=',')
        all_values=[]
        header=[]
        row1=[]

        #storing all the records as Collections
        i=0
        for row in csvfile:
            if i==0:
                i=1
                continue
            tuple_row=tuple(row)
            all_values.append(tuple_row)

    #connecting to mysql
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass"
    )

    #initial cursor
    mycursor = db.cursor()

    #creating database statement
    mycursor.execute("CREATE DATABASE csvFile")

    #creating table statement
    mycursor.execute("CREATE TABLE "+filename+" ("+res+")")

    #inserting the values
    sql = "INSERT INTO "+filename+" ("+header_str+") VALUES ("+insert_state+")"

    #insert records into database
    mycursor.executemany(sql,all_values)
    db.commit()
    print(mycursor.rowcount, "was inserted.")




