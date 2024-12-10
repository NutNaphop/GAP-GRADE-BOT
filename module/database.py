import sqlite3


def connect():
    connect = sqlite3.connect("db/Students.db")
    return connect

def findDup(userID , userName) :
    try :
      con = connect() 
      cur = con.cursor() 
      data = cur.execute(f''' 
                         select LineID , NontriID from Students 
                         where LineID = '{userID}' and NontriID = '{userName}'
                         ''')
      data = data.fetchall()
      
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return False
    finally:
        if data:
            print('found')
            return True
        else :
          return False
def insertData(LineID , userName , passWord):
    try:
        con = connect()
        cur = con.cursor()
        data = (LineID, userName, passWord)
        cur.execute("INSERT INTO Students VALUES(?, ?, ?)", data)
        con.commit()  # Remember to commit the transaction after executing INSERT.
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return False
    finally:
        if con:
            con.close()
            return True
        
def findID(LineID):
    try:
        con = connect()
        cur = con.cursor()
        cur.execute(f'''
            Select * from Students 
            Where LineID = '{LineID}'
                    ''')
        rows = cur.fetchone()
        print(rows)
    except sqlite3.Error as e:
        print("An error occurred:", e)
        return False
    finally:
        if rows == None:
            return -1
        elif con:
            print(rows)
            con.close()
            return rows
        
    