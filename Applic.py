from AddNews import AddNewsForm
from data_init import DB
from flask import Flask, redirect, render_template, session
from LoginForm import LoginForm
from NewsModel import NewsModel
from UsersModel import UsersModel
from AddUser import RegistrationForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB('asav')
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()


# http://127.0.0.1:8080/login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(username, password)
        if (exists[0]):
            session['username'] = username
            session['user_id'] = exists[1]
            return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    news = NewsModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'], news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news(comment=''):
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    
    path = os.getcwd()
    
    if form.validate_on_submit():
        
        title = form.title.data
        content = form.content.data
        picture = form.picture.data
        nm = NewsModel(db.get_connection())
        print(picture)
        a = nm.insert(title, content, picture.filename, session['username'])
        if a[0]:
            
            if not os.path.exists('static/users/{}'.format(session['username'])):
                os.chdir('static/users')
                os.mkdir(session['username'])
                os.chdir(session['username'])
                os.mkdir(title) 
                file.save(picture)
                
            else:
                os.chdir('static/users/{}'.format(session['username']))
                os.mkdir(title)
                file.save(picture)
                
            os.chdir('../../..')
            return redirect("/index")
        else:
            return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'], comment=a[1])
    
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'], comment='')


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_name = form.username.data
        pass_word = form.password.data
        um = UsersModel(db.get_connection())
        a = um.insert(user_name, pass_word)
        if a[0]:
            return redirect('/index')
        else:
            return render_template('register.html', title='Регистрация', form=form, comment=a[1])
        
    return render_template('register.html', title='Lol', form=form, comment='')


@app.route('/scatman')
def scatman():
    um = UsersModel(db.get_connection())
    user_list = um.get_all()
    nm = NewsModel(db.get_connection())
    news_list = nm.get_all()
    stats_list = []
    for i in user_list:
        hobosti = list(filter(lambda x: x == i[0],
                              map(lambda x: x[3], news_list)))
        stats_list.append([i[0], i[1], len(hobosti)])
    return render_template('stats.html', stats_list=stats_list)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')