from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict
from flask_wtf.csrf import CSRFProtect
# session拓展工具,　将flask中的session存储调整到redis
from flask_session import Session
from logging.handlers import RotatingFileHandler

import pymysql
import logging

# python2和python３数据库相互转化使用
pymysql.install_as_MySQLdb()

# 全局变量，申明为空类型数据
redis_store = None

# 当app不存的时候，只有进行申明，并没有真正创建数据库对象db
db = SQLAlchemy()


def write_log(config_class):
    # 设置日志的记录等级
    # DevelopmentConfig.LOG_LEVEL == logging.DEBUG
    # ProductionConfig.LOG_LEVEL == logging.ERORR
    # logging.basicConfig(level=logging.DEBUG)  # 调试DEBUG级
    logging.basicConfig(level=config_class.LOG_LEVEL)  # 调试DEBUG级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上线
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)

    # 创建日志记录的格式、日志等级　输入日志信息的文件名　行数　日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s: %(lineno)d %(message)s')

    # 为创建的日志记录器设置日志日志记录格式
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象,(flask app使用的)添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """
    工厂方法:development --->DevelopmentConfig/ production --->ProductionConfig
    """
    # 1.创建app对象
    app = Flask(__name__)

    # 2.将配置信息添加到app上
    config_class = config_dict[config_name]

    # 日志记录
    write_log(config_class)

    # DevelopmentConfig --->赋予app属性：开发模式app
    # ProductionConfig --->赋予app属性：线上模式app
    app.config.from_object(config_class)

    # 3.数据库对象(mysal/redis)
    # mysql数据库对象
    # db = SQLAlchemy(app)
    # 延迟加载数据库,当app有值的时候我才真正进行数据库初始化工作
    db.init_app(app)

    # redis数据库对象
    global redis_store
    redis_store = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)

    # 4.给项目添加CSRF保护机制
    # 4.1提取cooking中的csrf_token
    # 4.2如果数据是通过表单发送：提取表单中的csrf_token,如果数据是通过ajax请求发送：提取请求头中的字段X-CSRFToken
    # 4.3对比这两个值是否一致
    CSRFProtect(app)

    # 5.创建Flask_session工具对象：将flask.session的存储从　服务器“内存”　调整到　“redis”数据库
    Session(app)

    # 返回app对象
    return app
