from flask import Flask,url_for

# 实例化app
app = Flask(__name__)

# 注册路由
# @app.route('/')
# 动态URL
@app.route('/user/<name>')
def index(name):
    print(url_for('index',name="hahaha"))
    return "<h1>Hello %s </h1>"%name
