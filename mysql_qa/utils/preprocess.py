import jieba
from base.logger import setup_logging

logger = setup_logging(__name__)

def preprocess_text(text):
    # 预处理文本
    # logger.info("开始预处理文本")
    try:
        # 分词并转换为小写
        return jieba.lcut(text.lower())
    except AttributeError as e:
        # 记录预处理失败
        logger.error(f"文本{text}预处理失败: {e}")
        # 返回空列表
        return []