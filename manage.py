from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

import pymysql


# python2和python３数据库相互转化使用
pymysql.install_as_MySQLdb()


# 0.创建项目配置
class Config(object):
    """自定义项目配置"""

    #　开启项目调试模式
    DEBUG = True

    #　mysql数据库配置
    # 连接mysql的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:python@127.0.0.1:3306/news"
    # 开启数据库跟踪修改操作
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis数据库的配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379


# 1.创建app对象
app = Flask(__name__)

# 2.将配置信息添加到app上
app.config.from_object(Config)

# 3.数据库对象(mysal/redis)
# mysql数据库对象
db = SQLAlchemy(app)

# redis数据库对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,decode_responses=True)

# 4.创建管理对象

# 5.创建迁移对象

# 6.创建迁移命令

#　7.使用管理对象运行项目