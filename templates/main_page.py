import models
#import time
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from sqlalchemy import func

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///run.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

#Главная страница
@app.route('/')
def one():
    return render_template('main.html')

#Участники
@app.route('/participants', methods=['get'])
def part():
    dont = request.args.get('d')
    print(dont)
    return render_template('participants.html')

#Организаторы
@app.route('/org', methods=['get'])
def org():
    #passw = password
    #print(passw)
    return render_template('org.html')

@app.route('/org_two', methods=['get'])
def org_two():
    my_id = 2
    passw = request.args.get('password')
    title = request.args.get('title')
    num = request.args.get('num')
    direction = request.args.get('direction')
    print(title, direction)
    #passw = password
    print(passw)
    x_were = db.session.query(models.Were.text_id).all()
    if passw == '666':
        return render_template('org_two.html', were = x_were)
    elif passw == None:
        text = models.Texts(
        text_id = num,
        direction=direction,
        title=title)
        #my_id += 1
        db.session.add(text)
        db.session.commit()
        return render_template('org_two.html', were = x_were)
    else:
        return render_template('participants.html')

@app.route('/org_three', methods=['get'])
def org_three():
    #title = request.args.get('title')
    #direction = request.args.get('direction')
    passw = '666'
    #print(title, direction)
    #if passw == '666':
    return render_template('org_two.html')
    #else:
        #return render_template('participants.html')


#Результат
@app.route('/results', methods=['get'])
def res():
    het = request.args.get('h')
    slash = request.args.get('s')
    fem = request.args.get('f')
    gen = request.args.get('g')
    if not request.args.get('direction_two') == None:
        direc = request.args.get('direction_two')
    elif request.args.get('direction_three') != None:
        direc = request.args.get('direction_three')
    numbers = request.args.get('numbers')
    print(direc)
    #s = request.args.get('student')
    dont = (het, slash, fem, gen)
    hayu = numbers.split(', ')
        #my_score = db.session.query(
        #func.avg(models.Answers.one)).one()
    if direc != 'any':
        random_row = db.session.query(models.Texts.text_id)\
                     .filter(models.Texts.direction == direc).all()
    else:
        random_row = db.session.query(models.Texts.text_id).all()
    print(random_row, hayu)
    if not random_row == []:
        dont = random.choice(random_row)
    print(type(hayu[0]), str(dont))
    while str(dont[0]) in hayu: #and random_row != []:
        random_row.remove(dont)
        if random_row == []:
            name = ''
            dont = ['Такие работы кончились']
        else:
            dont = random.choice(random_row)
            #dont = dont[0]
    if random_row == []:
        name = ''
        dont = ['Такие работы кончились']
    else:
        a = dont[0]
        name = db.session.query(models.Texts.title)\
               .filter(models.Texts.text_id == a).one()
        x = db.session.query(models.Texts.text_id).filter(models.Texts.text_id == a).delete()
        print('x', x, a)
        #x = db.session.query(models.We.text_id).filter(models.Texts.text_id == a).add()
        #db.session.query(models.Texts).filter(models.Texts.text_id == '3').delete(synchronize_session=False)
        #db.session.delete(x)
        were = models.Were(
        text_id = a)
        #direction=direction,
        #title=title)
        #my_id += 1
        db.session.add(were)
        db.session.commit()
        print(name)
        #db.session.delete(models.Texts.text_id).all()
    return render_template('results.html',
                           want = dont[0], my_name = name)


if __name__ == '__main__':
    app.run(debug=False)





