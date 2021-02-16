import sqlite3

conn = sqlite3.connect('run.db')
cur = conn.cursor()

#Создаёт пустые таблицы для базы данных

cur.execute("""
CREATE TABLE IF NOT EXISTS my_texts 
(text_id int PRIMARY KEY, direction text, title text, link text)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS were_texts 
(text_id int PRIMARY KEY)
""")
conn.commit()



