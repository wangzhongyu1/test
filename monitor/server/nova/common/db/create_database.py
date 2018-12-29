#!/bin/env python
# -*- encoding=utf-8 -*-
import MySQLdb

# Database info
host = '10.154.4.141'
#port = 3306
user = 'root'
passwd = 'root'
db = 'test'
table_name1  = 'change_value'
table_name2  = 'current_value'

# connect the database
conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

# get the cursor
cursor = conn.cursor()

# Create Database
#cursor.execute("create database %s" % database_name)

# Use database
cursor.execute("use %s" % db)

# Create tables
cmd1 = "create table  %s(date timestamp, hostname  VARCHAR(40) NOT NULL, ip  VARCHAR(40) NOT NULL, conf_name  VARCHAR(100) NOT NULL, last_value  VARCHAR(1000) NOT NULL,new_value  VARCHAR(1000) NOT NULL);"
cursor.execute(cmd1 % table_name1)

cmd2 = "create table  %s(date timestamp, hostname  VARCHAR(40) NOT NULL, ip  VARCHAR(40) NOT NULL, conf_name  VARCHAR(100) NOT NULL, current_value  VARCHAR(1000) NOT NULL);"
cursor.execute(cmd2 % table_name2)



# close database
cursor.close()
conn.commit()
conn.close()
