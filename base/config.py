import os


class Config():
    def __init__(self):
        # redis
        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = 6379
        self.REDIS_DB = 0
        self.REDIS_PASSWORD = 1234

        # mysql
        self.mysql_host = '127.0.0.1'
        self.mysql_port = 3306
        self.mysql_user = 'root'
        self.mysql_password = 'root'
        self.mysql_db = 'mysql_qa'
        self.mysql_charset = 'utf8mb4'
        self.mysql_cursorclass = 'pymysql.cursors.DictCursor'
        self.mysql_pool_size = 10
        self.mysql_pool_recycle = 3600

        # logging
        self.LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log', 'app.log')