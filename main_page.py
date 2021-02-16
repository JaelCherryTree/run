import models
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
    return render_template('org.html')

@app.route('/org_two', methods=['get'])
def org_two():
    my_id = 2
    passw = request.args.get('password') #проверяем пароль
    title = request.args.get('title')
    num = request.args.get('num')
    direction = request.args.get('direction') #получаем данные из вопросов
    x_were = db.session.query(models.Were.text_id).all() #использованные номера
    if passw == '666': #если организатор
        return render_template('org_two.html', were = x_were)
    elif passw == None: #если организатор
        text = models.Texts(
        text_id = num,
        direction=direction,
        title=title) #это ввод текста
        db.session.add(text) #добавляем в базу
        db.session.commit()
        return render_template('org_two.html', were = x_were)
    else:#если участник
        return render_template('participants.html')

@app.route('/org_three', methods=['get'])
def org_three():
    passw = '666'
    return render_template('org_two.html')

#Результат
@app.route('/results', methods=['get'])
def res():
    het = request.args.get('h')
    slash = request.args.get('s')
    fem = request.args.get('f')
    gen = request.args.get('g') #это из анкеты участников, пока не работает
    direc = request.args.get('direction_two') #это направленность из выпадающего списка
    numbers = request.args.get('numbers') #это номера
    hayu = numbers.split(', ') #это делим номера в список
    if direc != 'any': #есди направленность любая
        random_row = db.session.query(models.Texts.text_id)\
                     .filter(models.Texts.direction == direc).all()
    else: #если есть пожелания по направленности
        random_row = db.session.query(models.Texts.text_id).all()
    if not random_row == []: #если есть подходящие тексты
        dont = random.choice(random_row)
    while str(dont[0]) in hayu: #если этот номер уже прочитан
        random_row.remove(dont)
        if random_row == []:
            dont = ['Такие работы кончиились']
        else:
            dont = random.choice(random_row)
    if random_row == []:
        dont = ['Такие работы кончиились']
    else:
        a = dont[0]
        name = db.session.query(models.Texts.title)\
               .filter(models.Texts.text_id == a).one() #получаем заголовок по номеру
        #удаляем текст из непрочитанных:
        x = db.session.query(models.Texts.text_id).filter(models.Texts.text_id == a).delete()
        print('x', x, a)
        #добавляем номер в прочитанные
        were = models.Were(
        text_id = a)
        db.session.add(were)
        db.session.commit()
    return render_template('results.html',
                           want = dont[0], read = '1', my_name = name[0])

#поехали!
if __name__ == '__main__':
    app.run(debug=False)





