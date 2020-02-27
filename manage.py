# 将存储数据到的session
from flask import session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db


# 传入的参数是development获取开发模式对应的app对象
# 传入的参数是production获取线上模式对应的app对象
app = create_app("developmengt")

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
