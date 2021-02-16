from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Texts(db.Model):

    __tablename__ = "my_texts"
    text_id = db.Column('text_id', db.Integer, primary_key=True)
    direction = db.Column('direction', db.Text)  # направленность
    title = db.Column('title', db.Text)  # заголовок
    link = db.Column('link', db.Text)  # ссылка


class Were(db.Model):

    __tablename__ = "were_texts"
    text_id = db.Column('text_id', db.Integer, primary_key=True)
