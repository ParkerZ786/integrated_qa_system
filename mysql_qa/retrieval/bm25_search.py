from rank_bm25 import BM25Okapi
import numpy as np
from mysql_qa.utils.preprocess import preprocess_text
from base.logger import setup_logging
logger = setup_logging(__name__)

class BM25Search:
    def __init__(self, mysql_client, redis_client):
        self.logger = logger
        self.mysql_client = mysql_client
        self.redis_client = redis_client
        self.bm25 = None
        self.questions = None
        self.original_questions = None
        self._load_data()

    def _load_data(self):
        self.logger.info("加载数据并初始化BM25模型...")
        # redis字段名称
        original_key = "qa_original_questions"          # 原始问题
        tokenized_key = "qa_tokenized_questions"        # 分词处理过的问题
        # 尝试从redis加载数据
        self.original_questions = self.redis_client.get_data(original_key)
        tokenized_questions = self.redis_client.get_data(tokenized_key)
        # 如果没有数据，则从 MySQL 加载数据
        if not self.original_questions or not tokenized_questions:
            self.original_questions = self.mysql_client.fetch_questions()
            if not self.original_questions:
                self.logger.warning("未加载到问题")
                return
            # 分词问题并存到 Redis
            tokenized_questions = [preprocess_text(q[0]) for q in self.original_questions]
            self.redis_client.set_data(original_key, [(q[0]) for q in self.original_questions])
            self.redis_client.set_data(tokenized_key, tokenized_questions)
        # 初始化 BM25 模型
        self.questions = tokenized_questions
        self.bm25 = BM25Okapi(self.questions)
        self.logger.info("BM25模型初始化完成")

    def _softmax(self, scores):
        # 计算 Softmax 分数
        exp_scores = np.exp(scores - np.max(scores))
        # 返回归一化分数
        return exp_scores / exp_scores.sum()

    def search(self, query, threshold=0.85):
        if not query or not isinstance(query, str):
            self.logger.error("无效的查询")
            return []

        try:
            query_tokens = preprocess_text(query)
            scores = self.bm25.get_scores(query_tokens)
            softmax_scores = self._softmax(scores)
            best_idx = np.argmax(softmax_scores)
            best_score = softmax_scores[best_idx]
            if best_score >= threshold:
                original_question = self.original_questions[best_idx]
                answer = self.mysql_client.fetch_answer(original_question)
                if answer:
                    # 缓存答案
                    # self.redis_client.set_data(f"answer:{query}", answer)
                    # 记录搜索成功
                    self.logger.info(f"搜索成功，最相似问题：{original_question}，Softmax 相似度: {best_score:.3f}，answer：{answer}")
                    return answer, False
            self.logger.info(f"搜索失败，最相似问题：{self.original_questions[best_idx]}，Softmax 相似度: {best_score:.3f}")
            return None, True
        except Exception as e:
            self.logger.error(f"搜索失败: {e}")
            return None, True

if __name__ == '__main__':
    from mysql_qa.cache.redis_client import RedisClient
    from mysql_qa.db.mysql_client import MySQLClient
    redis_client = RedisClient()
    mysql_client = MySQLClient()
    bm25_search = BM25Search(mysql_client, redis_client)
    # print(bm25_search.original_questions)
    query = 'ch系数模型评估'
    query2 = '你吃早餐了吗？'
    answer, is_get = bm25_search.search(query2)
    # print(answer)