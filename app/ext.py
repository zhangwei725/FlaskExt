from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class

db = SQLAlchemy()

migrate = Migrate()


def init_ext(app: Flask):
    # 初始化数据库相关的配置
    init_db_config(app)
    # 初始化缓存配置
    init_cache_config(app)
    # 初始化用户管理模块
    init_login_config(app)
    # 初始化文件上传配置
    init_upload_config(app)


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


""" 文件上传相关配置"""
"""
参数说明
name : 保存文件的子目录 默认是files 
extensions  设置允许上传的文件的类型 默认类型
default_dest 设置文件上传的根路径
"""
images = UploadSet(name='images', extensions=IMAGES, default_dest=None)
# files = UploadSet( extensions=IMAGES, default_dest=None)
import os

"""配置信息"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT_PATH = os.path.join(BASE_DIR, 'static/upload')


# 1> 配饰上传的文件的根目录
def init_upload_config(app):
    # 配置上传根目录
    app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_ROOT_PATH
    # 生成文件的访问的url地址
    app.config['UPLOADS_DEFAULT_URL'] = '/static/upload/'
    """
    app  Flask对象
    uploads_sets 文件上传核心类 UploadSet对象
    """
    configure_uploads(app=app, upload_sets=images)
    #     限制文件上传的大小
    patch_request_class(app=app, size=32 * 1024 * 1024)
