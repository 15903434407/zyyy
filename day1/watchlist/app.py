import os,sys

from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

import click
# 判断系统是不是以win开头的
WIN = sys.platform.startswith('win')

if WIN:
    prifix = "sqlite:///"  #windows
else:
    prifix = "sqlite:////"   #Mac,linux

# 实例化app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = prifix + os.path.join(app.root_path,'data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化app
db = SQLAlchemy(app)

# model数据层
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 注册路由
@app.route('/')
# 动态URL
# @app.route('/user/<name>')
# def index(name):
#     print(url_for('index',name="hahaha"))
#     return "<h1>Hello %s </h1>"%name


def index():
    # name = "ZY"
    # movies = [
    #     {'title':"a","year":"1"},
    #     {'title':"b","year":"2"},
    #     {'title':"c","year":"3"},
    #     {'title':"d","year":"4"},
    #     {'title':"e","year":"5"},
    #     {'title':"f","year":"6"},
    #     {'title':"g","year":"7"},
    #     {'title':"h","year":"8"},
    #     {'title':"i","year":"9"},
    # ]
    user = User.query.first()  #查询用户记录
    movies = Movie.query.all()

    return render_template('index.html',user=user,movies=movies)





#自定义命令

@app.cli.command()  #注册为命令
@click.option('--drop',is_flag=True,help="先删除再创建")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("chushihua")

@app.cli.command()
def forge():
    name = "zy"
    movies = [
        {'title':"a","year":"1"},
        {'title':"b","year":"2"},
        {'title':"c","year":"3"},
        {'title':"d","year":"4"},
        {'title':"e","year":"5"},
        {'title':"f","year":"6"},
        {'title':"g","year":"7"},
        {'title':"h","year":"8"},
        {'title':"i","year":"9"},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("导入数据完成")


@app.errorhandler(404)
def page_not_found(a):
    user = User.query.first()
    return render_template('404.html',user=user)







