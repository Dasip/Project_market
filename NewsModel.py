import sqlite3

class NewsModel():
    
    def __init__(self, conn):
        self.conn = conn 
        
    def init_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             picture VARCHAR(1000),
                             user_id INTEGER,
                             time DATETIME
                             )''')
        cursor.close()
        self.conn.commit()
        
    def insert(self, title, pict_name, content, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE title = ?''', (title,))   
        row = cursor.fetchone()
        a = [False, 'Проект с таким именем уже существует']
        if not row:
            cursor.execute('''INSERT INTO news 
                              (title, content, picture, user_id, time) 
                              VALUES (?,?,?, DATETIME())''', (title, content, pict_name,
                                                              str(user_id)))
            a = [True, '']
        cursor.close()
        self.conn.commit()
        return a
    
    def get(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row
     
    def get_all(self, user_id = None):
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows
    
    def delete(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.conn.commit()
        
    def stats(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(title), user_id, FROM news GROUP BY user_id')
        st = cursor.fetchall()
        return st