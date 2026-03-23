import os
import configparser
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config():
    def __init__(self, config_file=os.path.join(project_root, 'config.ini')):
        # 创建配置对象并读取配置文件
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # redis
        self.REDIS_HOST = self.config.get('redis', 'host', fallback='localhost')
        self.REDIS_PORT = self.config.getint('redis', 'port', fallback=6379)
        self.REDIS_PASSWORD = self.config.get('redis', 'password', fallback='1234')
        self.REDIS_DB = self.config.getint('redis', 'db', fallback=0)

        # mysql
        # fallback作用：如果没有找到对应的键值对，则返回fallback指定的值
        self.MYSQL_HOST = self.config.get('mysql', 'host', fallback='localhost1')
        self.MYSQL_USER = self.config.get('mysql', 'user', fallback='root')
        self.MYSQL_PASSWORD = self.config.get('mysql', 'password', fallback='root')
        self.MYSQL_DATABASE = self.config.get('mysql', 'database', fallback='subjects_kg')


        # logging
        self.LOG_FILE = os.path.join(project_root, self.config.get('logger', 'log_file', fallback='logs/app.log'))

        # JP学科知识问答.csv位置
        self.csv_file = os.path.join(project_root, self.config.get('file', 'csv_file', fallback='mysql_qa/JP学科知识问答.csv'))

if __name__ == '__main__':
    config = Config()
    # print(config.MYSQL_HOST)
    print(config.LOG_FILE)