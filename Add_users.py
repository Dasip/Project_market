from AddNews import AddNewsForm
from data_init import DB
from LoginForm import LoginForm
from NewsModel import NewsModel
from UsersModel import UsersModel

#инициализируем таблицу
db = DB('asav')
UsersModel(db.get_connection()).init_table()
user_ = UsersModel(db.get_connection())
#добавляем пользователя (по одному!!!!!)
user_.insert('Admin','pass')
user_.insert('Dasip', 'BeakEasy_cool')
user_.insert('cTPoIJTeJIb', 'asdqwezxcfghrtyvbn')
user_.insert('Fred', '#@#@fff!11')
