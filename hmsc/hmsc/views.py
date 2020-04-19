from hmsc import app 
   # from models import User, Post, ROLE_USER, ROLE_ADMIN   
@app.route('/') 
def index(): 
    return 'hello flask' 