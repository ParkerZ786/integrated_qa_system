import pymysql
import pandas as pd
from base.config import Config
from base.logger import setup_logging
logger = setup_logging(__name__)


class MySQLClient:
    def __init__(self):
        self.logger = logger
        try:
            self.connection = pymysql.connect(host=Config().MYSQL_HOST,
                                        user=Config().MYSQL_USER,
                                        password=Config().MYSQL_PASSWORD,
                                        db=Config().MYSQL_DATABASE,)
            self.cursor = self.connection.cursor()
            logger.info("数据库连接成功")
        except pymysql.Error as e:
            logger.error("数据库连接失败：{}".format(e))
            raise

    def fetch_questions(self):
        # 获取所有问题
        try:
            # 执行查询
            self.cursor.execute("SELECT question FROM jpkb")
            # 获取结果
            results = self.cursor.fetchall()
            # 记录获取成功
            self.logger.info("成功获取所有问题")
            # 返回结果
            return results
        except pymysql.MySQLError as e:
            # 记录查询失败
            self.logger.error(f"获取所有问题失败: {e}")
            # 返回空列表
            return []

    def create_table(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS jpkb (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(20),
            question VARCHAR(1000),
            answer VARCHAR(1000))
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info("表jpkd创建成功")
        except pymysql.Error as e:
            logger.error("表jpkd创建失败，{}".format(e))
            raise

    def insert_data(self, csv_file):
        data = pd.read_csv(csv_file)
        try:
            for index, row in data.iterrows():
                insert_query = '''
                INSERT INTO jpkb (subject_name, question, answer)
                VALUES (%s, %s, %s)
                '''
                values = (row['学科名称'], row['问题'], row['答案'])
                self.cursor.execute(insert_query, values)
                self.connection.commit()
                logger.info("数据插入成功")
        except pymysql.Error as e:
            logger.error("数据插入失败，{}".format(e))

    def fetch_answer(self, question):
        try:
            query = '''
            SELECT answer FROM jpkb WHERE question = %s
            '''
            values = (question)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                self.logger.info(f"question:{question[:20]}, result: {result[0][:50]}")
                return result[0]
            else:
                self.logger.info(f"question:{question}, result: NONE")
                return None
        except pymysql.Error as e:
            self.logger.error("查询失败，{}".format(e))
            return None

    def close(self):
        # 关闭数据库连接
        try:
            # 关闭连接
            self.connection.close()
            # 记录关闭成功
            self.logger.info("MySQL 连接已关闭")
        except pymysql.MySQLError as e:
            # 记录关闭失败
            self.logger.error(f"关闭连接失败: {e}")



if __name__ == '__main__':
    mysql_client = MySQLClient()
    # mysql_client.create_table()
    # mysql_client.insert_data(Config().csv_file)
    # result = mysql_client.fetch_answer('ch系数模型评估')
    print(mysql_client.fetch_questions())
    mysql_client.close()