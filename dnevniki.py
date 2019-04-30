from AddNews import AddNewsForm
from data_init import DB
from flask import Flask, redirect, render_template, session
from LoginForm import LoginForm
from NewsModel import NewsModel
from UsersModel import UsersModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#инициализируем таблицу
db = DB('asav')
NewsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()


# http://127.0.0.1:8080/login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/index')


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        usname = None
    else:
        usname=session['username']
    
    news = NewsModel(db.get_connection()).get_all()
    return render_template('index.html', username=usname, news=news)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')