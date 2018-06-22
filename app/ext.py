from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate()


def init_ext(app: Flask):
    # 初始化数据库相关的配置
    init_db_config(app)
    # 初始化缓存配置
    init_cache_config(app)
    # 初始化用户管理模块
    init_login_config(app)


def init_db_config(app):
    # 主要配置 SECRET_KEY 主要用于加密
    app.config['SECRET_KEY'] = '13213132132131'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_ext?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    migrate.init_app(app, db)


cache = Cache()


# 缓存配置
def init_cache_config(app):
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    cache.init_app(app, config={
        # 默认的过期时间 单位秒
        'CACHE_DEFAULT_TIMEOUT': 60,
        # 缓存类型
        'CACHE_TYPE': 'redis',
        # IP地址
        'CACHE_REDIS_HOST': '127.0.0.1',
        # 端口
        'CACHE_REDIS_PORT': 6379,
        # 密码
        # 连接数据库的编号
        'CACHE_REDIS_DB': 1,
        # 缓存key的前缀
        'CACHE_KEY_PREFIX': 'view_'
    })


# 用户模块插件
login_manager = LoginManager()


def init_login_config(app):
    # 当用户点击某个需要登录才能访问的界面的时候,
    # 如果没有登录,就会自动跳转相应视图函数
    login_manager.login_view = 'user.login'
    login_manager.login_message = '必须要登录才能访问'
    login_manager.init_app(app)
