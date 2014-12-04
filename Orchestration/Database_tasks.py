import sqlite3 as sql
import os
import random


def generate_db(database_name):
    db_name = database_name
    db = sql.connect(db_name)
    db.row_factory = sql.Row #use to access column by name (otherwise, column must be accessed by index)


    #CREATE TABLE
    cursor = db.cursor()

    sql_stm = 'DROP TABLE IF EXISTS TRAVEL_COST'
    cursor.execute(sql_stm)
    sql_stm = 'CREATE TABLE TRAVEL_COST(start_node INTEGER, end_node INTEGER, cost REAL)'
    cursor.execute(sql_stm)

    sql_stm = 'DROP TABLE IF EXISTS TIME'
    cursor.execute(sql_stm)
    sql_stm = 'CREATE TABLE TIME(node INTEGER, early_time INTEGER, late_time INTEGER)'
    cursor.execute(sql_stm)

    sql_stm = 'DROP TABLE IF EXISTS RUNS'
    cursor.execute(sql_stm)
    sql_stm = 'CREATE TABLE RUNS(method_id INTEGER, run_id INTEGER PRIMARY KEY, solution REAL, run_time REAL, start_time REAL, stop_time REAL)'
    cursor.execute(sql_stm)

    db.commit()


    #INSERT VALUES TO TABLE
    n = 10 #number of nodes
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            start_node = i
            end_node = j
            cost = random.randint(1,10)
            cursor.execute('''INSERT INTO TRAVEL_COST(start_node,end_node,cost)
                          VALUES(?,?,?)''', (start_node,end_node,cost))

    for i in range(1,n+1):
        node = i
        early_time = random.randint(0,0)
        late_time = random.randint(30,100)
        cursor.execute('''INSERT INTO TIME(node,early_time,late_time)
                      VALUES(?,?,?)''', (node,early_time,late_time))

    for i in range(1,n+1):
        method_id = random.randint(1,4)
        run_id = i
        solution = random.uniform(50,300)
        start_time = random.uniform(1,20)
        stop_time = random.uniform(80,130)
        run_time = stop_time - start_time
        cursor.execute('''INSERT INTO RUNS(method_id,run_id,solution,run_time,start_time,stop_time)
                      VALUES(?,?,?,?,?,?)''', (method_id,run_id,solution,run_time,start_time,stop_time))

    db.commit()
    return db_name

def refresh_db(database_name_B,n):
    db_name = database_name_B
    db = sql.connect(db_name)
    db.row_factory = sql.Row #use to access column by name (otherwise, column must be accessed by index)


    #CREATE TABLE
    cursor = db.cursor()

    sql_stm = 'DROP TABLE IF EXISTS TRAVEL_COST'
    cursor.execute(sql_stm)
    sql_stm = 'CREATE TABLE TRAVEL_COST(start_node INTEGER, end_node INTEGER, cost REAL)'
    cursor.execute(sql_stm)

    sql_stm = 'DROP TABLE IF EXISTS TIME'
    cursor.execute(sql_stm)
    sql_stm = 'CREATE TABLE TIME(node INTEGER, early_time INTEGER, late_time INTEGER)'
    cursor.execute(sql_stm)

    db.commit()



    #INSERT VALUES TO TABLE
##    n = 10 #number of nodes
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            start_node = i
            end_node = j
            cost = random.randint(1,10)
            cursor.execute('''INSERT INTO TRAVEL_COST(start_node,end_node,cost)
                          VALUES(?,?,?)''', (start_node,end_node,cost))

    for i in range(1,n+1):
        node = i
        early_time = random.randint(0,0)
        late_time = random.randint(30,100)
        cursor.execute('''INSERT INTO TIME(node,early_time,late_time)
                      VALUES(?,?,?)''', (node,early_time,late_time))

    db.commit()
    return db_name

def read_db(database_name_B,n):
    """READ DATA AND RUN OPTIMIZE"""
##    n=10
    c={}
    e={}
    l={}

    db_name = database_name_B
    db = sql.connect(db_name)
    db.row_factory = sql.Row #use to access column by name (otherwise, column must be accessed by index)
    cursor = db.cursor()

    sql_stm = 'SELECT * FROM TRAVEL_COST'
    cursor.execute(sql_stm)
    rows = map(lambda t: t, cursor.fetchall())
    i = 0
    j = 0
    c[n,n] = 0
    for row in rows:
        i = row['start_node']
        j = row['end_node']
        c[i,i] = 0
        c[i,j] = float(row['cost'])
        c[j,i] = c[i,j]


    sql_stm = 'SELECT * FROM TIME'
    cursor.execute(sql_stm)
    rows = map(lambda t: t, cursor.fetchall())
    i = 0
    for row in rows:
        i +=1
        e[i] = float(row['early_time'])
        l[i] = float(row['late_time'])

    return n,c,e,l

def update_db(database_name,method_id,solution,run_time,start_time,stop_time,new_table):
    db_name = database_name
    db = sql.connect(db_name)
    db.row_factory = sql.Row #use to access column by name (otherwise, column must be accessed by index)
    cursor = db.cursor()

    if(new_table == True):
        sql_stm = 'DROP TABLE IF EXISTS RUNS'
        cursor.execute(sql_stm)
        sql_stm = 'CREATE TABLE RUNS(method_id INTEGER, run_id INTEGER PRIMARY KEY, solution REAL, run_time REAL, start_time REAL, stop_time REAL)'
        cursor.execute(sql_stm)

    #INSERT VALUES TO TABLE
    n = 10 #number of nodes

    sql_stm = 'SELECT COUNT(*) FROM RUNS'
    cursor.execute(sql_stm)
##    rows = map(lambda t: t, cursor.fetchall())
    result=cursor.fetchone()
    number_of_rows=result[0]
    run_id = number_of_rows + 1

    cursor.execute('''INSERT INTO RUNS(method_id,run_id,solution,run_time,start_time,stop_time)
                  VALUES(?,?,?,?,?,?)''', (method_id,run_id,solution,run_time,start_time,stop_time))


    db.commit()