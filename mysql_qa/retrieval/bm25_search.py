import jieba
from rank_bm25 import BM25L
import logging

# 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BM25Search:
    def __init__(self, docs):
        self.docs = docs
        # 将文档分词
        self.tokenized_docs = [jieba.lcut(doc) for doc in docs]
        # 创建BM25模型
        self.bm25 = BM25L(self.tokenized_docs)
        logger.info("BM25模型创建成功")

    def search(self, query):
        token_query = jieba.lcut(query)
        try:
            scores = self.bm25.get_scores(token_query)
            best_idx = scores.argmax()
            best_score = scores[best_idx]
            best_doc = self.docs[best_idx]
            logger.info(f"查询：{query}，最佳匹配{best_doc}，得分{best_score}")
            return best_doc, best_score

        except Exception as e:
            logger.error(f"查询错误: {e}")
            return None, 0

