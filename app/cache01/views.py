from flask import Blueprint

from app.ext import cache
from flask import render_template

cache_blue = Blueprint('cache', __name__, template_folder='templates')

"""
timeout 过期时间
key_prefix 缓存key的前缀
unless: 回调函数 当返回True 缓存不起作用  None 使用缓存
"""


@cache_blue.route('/1/')
@cache.cached(timeout=60, key_prefix='')
def test():
    print('天台见')
    return '111'


"""
make_name 是一个函数 返回string类型 默认情况下会函数名称作为key缓存起来
"""


@cache_blue.route('/2/<name>/')
@cache.memoize(timeout=60 * 60)
def test2(name):
    print(name)
    return '2222'


@cache_blue.route('/3/')
def test3():
    return render_template('cache1.html', msg='111')
