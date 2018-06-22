"""
1> 登录  注销功能
2> 限制用户的权限
3> 记住密码功能
4> 对session进行保护
"""
from flask import Blueprint, request, render_template, redirect, abort, url_for
from flask_login import login_user, logout_user, login_required

from app.ext import login_manager, db
from app.user.models import User

from werkzeug.security import generate_password_hash, check_password_hash

"""
1>创建模型
2>配置登录


"""

"""
LoginManager
"""
user_blue = Blueprint('user', __name__, template_folder='templates')


@login_manager.user_loader
def init_user(uid):
    user = User.query.get(uid)
    # passwd = generate_password_hash('123456')
    # check_password_hash(passwd, '123456')

    return user


@user_blue.route('/login/', methods=['POST', 'GET'])
def login():
    msg = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.values.get('uname')
        password = request.values.get('pwd')
        if username and password:
            try:
                user = User.query.filter(User.username == username).first()
                if user:
                    if user.password == password:
                        # 必须调用第三方的插件的login_user 表示用户登录成功
                        login_user(user)
                        return redirect('/index/')
                    else:
                        msg = '密码错误'
                else:
                    msg = '账号不存在'
            except Exception  as e:
                print(e)
                # abort(500)
                msg = '网络异常!!!请检查网络!!'
    else:
        msg = '不支持的请求方式'
    return render_template('login.html', msg)


@user_blue.route('/logout/', methods=['POST', 'GET'])
def login_out():
    logout_user()
    return redirect(url_for('login'))


@user_blue.route('/test/')
@login_required
def test():
    return render_template('index.html')
