from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
# session拓展工具,　将flask中的session存储调整到redis
from flask_session import Session
# 将存储数据到的session
from flask import session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import pymysql

# python2和python３数据库相互转化使用
pymysql.install_as_MySQLdb()


# 0.创建项目配置
class Config(object):
    """自定义项目配置"""

    # 　开启项目调试模式
    DEBUG = True

    # 　mysql数据库配置
    # 连接mysql的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:python@127.0.0.1:3306/news"
    # 开启数据库跟踪修改操作
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis数据库的配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # 使用session需要设置加密字符串
    SECRET_KEY = "SNFKALFAGDASDFASDGHJ"

    # 将flask.session的存储从　服务器“内存”　调整到　“redis”数据库配置如下
    SESSION_TYPE = 'redis'  # 标明存储的数据库类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)  # 只需要redis对象
    SESSION_USE_SIGNER = True  # 对于session_id需要加密处理
    SESSION_PERMANENT = False  # redis中的session数据不需要永久存储
    PERMANENT_SESSION_LIFTTIME = 86400  # 设置redis中session过期时长


# 1.创建app对象
app = Flask(__name__)

# 2.将配置信息添加到app上
app.config.from_object(Config)

# 3.数据库对象(mysal/redis)
# mysql数据库对象
db = SQLAlchemy(app)

# redis数据库对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 4.给项目添加CSRF保护机制
# 4.1提取cooking中的csrf_token
# 4.2如果数据是通过表单发送：提取表单中的csrf_token,如果数据是通过ajax请求发送：提取请求头中的字段X-CSRFToken
# 4.3对比这两个值是否一致
CSRFProtect(app)

# 5.创建Flask_session工具对象：将flask.session的存储从　服务器“内存”　调整到　“redis”数据库
Session(app)

# 6.创建管理对象
manager = Manager(app)

# 7.创建迁移对象
Migrate(app, db)

# 8.创建迁移命令
manager.add_command('db', MigrateCommand)



@app.route('/')
def news():
    session['name'] = 'laowang'
    return "你好"


if __name__ == '__main__':
    # app.run()
    # 9.使用管理对象运行项目
    manager.run()
