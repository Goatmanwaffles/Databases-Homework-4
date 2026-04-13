import pymysql
#change this variable for you own variables with the user information
#dblocal = pymysql.connect(host="localhost",user= "root",password= "",database= "kent") #for local connection


#CS Server database


#local database
dbserver = pymysql.connect(host="localhost",user= "root",password= "",database= "ksu") #for connecting to the CS server
#server
#dbserver = pymysql.connect(host="dbdev.cs.kent.edu",user= "username",password= "",database= "username") #for connecting to the CS server