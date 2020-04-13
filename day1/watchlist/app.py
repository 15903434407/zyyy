import os,sys

from flask import Flask,url_for,render_template,request,flash,redirect
# from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
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

app.config['SECRET_KEY'] = '1903_dev'


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


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':

        # 获取表单的数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入错误')
            return redirect(url_for('index'))
        # 将数据保存到数据库
        movie = Movie(title=title,year=year) # 创建记录
        db.session.add(movie)
        db.session.commit()
        flash('创建成功')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html',movies=movies)


# 更新/movie/edit
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST']) 
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year)>4 or len(title)>60:
            flash('输入有误')
            return redirect(url_for('edit'),movie_id = movie_id)
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('电影更新完成')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)



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

# 处理错误函数
@app.errorhandler(404)
def page_not_found(a):
    return render_template('404.html')

# 模板上下文处理函数
@app.context_processor
def common_user():
    user = User.query.first()
    return dict(user = user)




