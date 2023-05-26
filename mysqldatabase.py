import os
import configparser
import mysql.connector
from datetime import datetime


class User:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(BASE_DIR ,'config.ini'))
        conn = mysql.connector.connect(
            host=config.get('mysql', 'host'),  
            user=config.get('mysql', 'user'),  
            password=config.get('mysql', 'passwd'),
            database=config.get('mysql', 'database'),
        port=3306)  
        self.conn = conn
        self.cursor = conn.cursor()
        self.create_user_table()
        self.create_story_table()
        self.create_story_options_table()

    def create_user_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                userid INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARBINARY(128) NOT NULL,
                email VARCHAR(255) NOT NULL,
                sex CHAR(3) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_dt DATE AS (DATE(created_at))
            ) ENGINE=InnoDB;
        ''')
        self.conn.commit()
    def create_story_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stories (
                story_id INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                story_generate_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
                story_over_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                story_style VARCHAR(50) NOT NULL,
                story_name VARCHAR(100) NOT NULL,
                story TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(userid)
            ) ENGINE=InnoDB;
        ''')
        self.conn.commit()
    def create_story_options_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS story_score (
                id INT AUTO_INCREMENT UNIQUE NOT NULL,
                story_id INT NOT NULL,
                user_id INT NOT NULL,
                score INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(userid),
                FOREIGN KEY(story_id) REFERENCES stories(story_id)
            ) ENGINE=InnoDB;
        ''')
        self.conn.commit()


    def insert_user(self, username, password,email,sex):
        query = 'INSERT INTO users (username, password, email, sex) VALUES (%s, %s, %s, %s)'
        value = (username, password, email, sex)
        self.cursor.execute(query, value)
        self.conn.commit()
    def insert_story(self, user_id,story_generate_time,story_over_time,story_style,story_name,story):
        query = 'INSERT INTO users (user_id,story_generate_time,story_over_time,story_style,story_name,story) VALUES (%s, %s, %s,%s, %s, %s)'
        value = (user_id,story_generate_time,story_over_time,story_style,story_name,story)
        self.cursor.execute(query, value)
        self.conn.commit()
    def insert_score(self, story_id, user_id,score):
        query = 'INSERT INTO users (story_id, user_id,score) VALUES (%s, %s, %s)'
        value = (story_id, user_id,score)
        self.cursor.execute(query, value)
        self.conn.commit()
    def get_user_id(self, username):
        query = 'SELECT userid FROM users WHERE username = %s'
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result is None:
            return None 
        return result[0]
    def get_story_id(self, user_id, story_name):
        query = 'SELECT story_id FROM stories WHERE user_id = %s AND story_name = %s'
        self.cursor.execute(query, (user_id, story_name,))
        result = self.cursor.fetchone()
        if result is None:
            return None 
        return result[0]
    def get_password(self, username):
        query = 'SELECT password FROM users WHERE username = %s'
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result is None:
            return None 
        password_hash_binary = bytes(result[0]) 
        print(password_hash_binary)
        return password_hash_binary
    def get_users_list(self):
        query = 'SELECT username FROM users'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    def logout(self):
        self.conn.close()




if __name__ == "__main__":
    user = User()
    user_list = user.get_users_list()
    print(user_list[0][0])
    print(type(user_list[0]))
    password = user.get_password('admin1')
    if password is None:
        print("User not found")
    else:
        print("The password is:", password)
    user.logout()

