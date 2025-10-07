#import library
import sqlite3
print('import')

#add path to chinook.db to connect to it
connection = sqlite3.connect("chinook.db")
print('connection: ', connection)

#cursor object that executes SQL commands
cur_obj = connection.cursor()
print('init cursor: ', cur_obj)

#function definitions

#main method

#always close connections when exiting
cur_obj.close()
connection.close()
print('connection closed')