from base.logger import logger
from base.config import Config
import redis



class RedisClient(object):
    """
    Redis数据库操作类
    """
    def __init__(self):
        self.logger = logger
        try:
            self.client = redis.StrictRedis(
                host=Config().REDIS_HOST,
                port=Config().REDIS_PORT,
                db=Config().REDIS_DB,
                password=Config().REDIS_PASSWORD,
                decode_responses=True           # 默认返回字节，这里改为字符串
                )
            self.logger.info('Redis连接成功')
        except Exception as e:
            self.logger.error('Redis连接失败：{}'.format(e))
            raise

def main():
    """
    测试
    """
    rc = RedisClient()
    # rc.client.set('test', 'test')
    # print(rc.client.get('test'))

if __name__ == '__main__':
    main()