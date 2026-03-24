# EduRAG (Integrated QA System)

这是一个基于检索增强生成（RAG）架构的教育领域智能问答系统。它封装了从文档处理、特征向量提取、混合检索到最终调用LLM生成回答的完整流水线。系统支持对不同学科（如 AI、Java、测试、运维、大数据）的专业问题进行高精准度的解答。

## 🌟 核心特性

- **文档智能切分**：采用父子块（Parent-Child Chunking）切分策略，保障检索精度的同时保留丰富的父文档上下文内容。
- **高精度混合检索**：融合了 BGE-M3 的稠密向量（Dense Vector）和稀疏向量（Sparse Vector），在 Milvus 中执行混合搜索。
- **多阶段重排序 (Reranking)**：引入 BGE-Reranker 交叉编码器，对召回的候选文档块进行二次打分重排，提高 Top-K 的准确率。
- **自适应高级检索策略**：
  - **意图识别分发**：集成的 BERT 分类器 (Query Classifier)，将通用闲聊与特定领域知识隔离，提升系统响应速度与稳定性。
  - **假设问题检索 (HyDE)**：通过大模型生成假设性答案，再以假设答案搜寻相关文档，解决语义不匹配问题。
  - **子查询拆解 (Sub-queries)**：将复杂问题拆分为多个子问题并发检索，提高长片段复杂查询的召回覆盖率。
  - **多轮对话回溯 (Backtracking)**：结合对话历史重新构建查询问题。
- **多数据源隔离**：支持基于 `source_filter` 进行特定学科类别的过滤检索，防止跨学科知识干扰。

## 🛠️ 技术栈

- **编程语言**：Python 3
- **核心框架**：LangChain, FastAPI
- **向量数据库**：Milvus (PyMilvus)
- **嵌入模型 (Embedding)**：BGE-M3 (支持 Dense/Sparse/ColBERT)
- **重排模型 (Reranker)**：BGE-Reranker-large (基于 Sentence-Transformers)
- **大语言模型 (LLM)**：通过 OpenAI 兼容接口对接 Kimi 开放平台 (DashScope 等)
- **其他组件**：MySQL (关系数据), Redis (缓存), PyTorch

## 🚀 快速开始

### 1. 配置环境
运行前请确保安装了 `requirements.txt` 中的所有依赖：
```bash
pip install -r requirements.txt
```

### 2. 参数配置
在 `config.ini` 文件中配置您的数据库连接（MySQL, Redis, Milvus）以及大模型 API Key（`dashscope_api_key` 等）。

### 3. 数据处理模式 (向量化入库)
执行以下命令，将 `data/` 目录下的源文档根据学科类别提取并向量化存入 Milvus 数据库：
```bash
python main.py --data-processing --data-dir ./data
```

### 4. 交互式查询模式
执行以下命令启动 CLI 终端问答：
```bash
python main.py
```
在提示下输入您想要查询的问题，系统将自动分类意图、检索引擎、重排并流式输出生成的最终答案。

## 📁 项目结构
- `main.py`：系统主入口，包含文档处理和交互查询两种运行模式。
- `config.ini`：系统的核心配置文件。
- `base/`：包含日志记录、配置读取等基础服务组件。
- `rag_qa/core/`：核心 RAG 逻辑目录。
  - `document_processor.py`：文档清洗与切分逻辑。
  - `vector_store.py`：使用 BGE-M3 创建 Embedding 并和 Milvus 进行交互、重排过滤。
  - `rag_system.py`：基于多种检索策略获取上下文并调用 LLM 生成答案。
  - `query_classifier.py` / `strategy_selector.py`：Query 处理、意图分类与策略路由。
- `mysql_qa/`：关系型数据库 MySQL 的问答或存储逻辑。
