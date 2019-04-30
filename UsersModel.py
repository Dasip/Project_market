import sqlite3

class UsersModel():
    
    def __init__(self, conn):
        self.conn = conn  
        
    def init_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          username VARCHAR(64),
                          password_hash VARCHAR(128)
                          )''')
        cursor.close()
        self.conn.commit()  
        
    def exists(self, username, password_hash=None):
        cursor = self.conn.cursor()
        if password_hash:
            cursor.execute('''SELECT * FROM users WHERE username = ?
                              AND password_hash = ?''',
                           (username, password_hash))
        else:
            cursor.execute('''SELECT * FROM users WHERE username = ?''',
                           (username))     
            
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)    
    
    def get(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row
 
    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows
    
    def insert(self, username, password_hash):
        curs = self.conn.cursor()
        
        curs.execute('''SELECT * FROM users WHERE username = ?''', (username,))     
        row = curs.fetchone()
        a = [False, 'Этот логин уже занят.']
        if not row:
            curs.execute('''INSERT INTO users 
            (username, password_hash) 
            VALUES (?,?)''', (username, password_hash))
            a = [True, '']
        
        curs.close()
        self.conn.commit()    
        return a
            