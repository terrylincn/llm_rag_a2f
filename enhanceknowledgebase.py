from sentence_transformers import SentenceTransformer
import os

# 假设函数，用于模拟 matt_solomatov_toolkit 的文本处理
def process_text_with_matt_solomatov_toolkit(text):
    from mattsollamatools import chunker
    # 这里简单地将文本分割为句子作为示例
    #return text.split('. ')
    chunks = chunker(text)
    return chunks

class EnhancedKnowledgeBase:
    def __init__(self, directory, model_name='./models/sentence-transformers_all-MiniLM-L6-v2'):
        self.directory = directory
        self.model = SentenceTransformer(model_name)
        self.knowledge_base = {}
        self.vectorized_knowledge = []

    def build_knowledge_base(self):
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path) and file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    chunks = process_text_with_matt_solomatov_toolkit(content)
                    self.knowledge_base[filename] = chunks

    def vectorize_knowledge_base(self):
        for filename, chunks in self.knowledge_base.items():
            article={}
            article['embeddings'] = []
            article['url'] = filename
            embeddings = self.model.encode(chunks)
            for (chunk, embedding) in zip(chunks, embeddings):
                item = {}
                item['source'] = chunk
                item['embedding'] = embedding.tolist()  # Convert NumPy array to list
                item['sourcelength'] = len(chunk)
                article['embeddings'].append(item)
            self.vectorized_knowledge.append(article)

    def get_vectorized_content(self, filename):
        ret = None
        index = 0
        for vec in self.vectorized_knowledge:
            if vec['url'] == filename:
                ret = vec
                break
        return ret

    def list_files(self):
        return list(self.knowledge_base.keys())

if __name__  == "__main__":
    # 使用方法
    directory_path = "data"
    enhanced_kb = EnhancedKnowledgeBase(directory_path)
    enhanced_kb.build_knowledge_base()
    enhanced_kb.vectorize_knowledge_base()

    # 获取特定文件的向量化内容
    print(enhanced_kb.get_vectorized_content("example.txt"))

    # 列出知识库中的所有文件
    print(enhanced_kb.list_files())
