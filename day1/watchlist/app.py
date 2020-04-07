from flask import Flask,url_for,render_template

# 实例化app
app = Flask(__name__)

# 注册路由
@app.route('/')
# 动态URL
# @app.route('/user/<name>')
# def index(name):
#     print(url_for('index',name="hahaha"))
#     return "<h1>Hello %s </h1>"%name


def index():
    name = "ZY"
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
    return render_template('index.html',name=name,movies=movies)