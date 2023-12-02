from sentence_transformers import SentenceTransformer
import requests
import json
import time
from search import knn_search
from enhanceknowledgebase import EnhancedKnowledgeBase

directory_path = "uploaded_files"
enhanced_kb = EnhancedKnowledgeBase(directory_path)
enhanced_kb.build_knowledge_base()
enhanced_kb.vectorize_knowledge_base()
model_name='./models/sentence-transformers_all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

def rebuild():
    enhanced_kb.build_knowledge_base()
    enhanced_kb.vectorize_knowledge_base()

def query(question):
    context = []
    # Embed the user's question
    t1 = time.time()
    question_embedding = model.encode([question])
    t2 = time.time()
    print(f'encode:{t2-t1}')

    # Perform KNN search to find the best matches (indices and source text)
    best_matches = knn_search(question_embedding, enhanced_kb.vectorized_knowledge, k=5)
    t3 = time.time()
    print(f'knn_search:{t3-t2}')


    sourcetext=""
    for i, (index, source_text) in enumerate(best_matches, start=1):
        sourcetext += f"{i}. Index: {index}, Source Text: {source_text}"

    systemPrompt = f"Only use the following information to answer the question. Do not use anything else: {sourcetext}"
    print(f'systemPrompt:{systemPrompt}')
    print(f'systemPrompt len:{len(systemPrompt)}')

    url = "http://13902254981.tpddns.cn:9888/api/generate"#"http://localhost:11434/api/generate"

    payload = {
    "model": "llama2",#"mistral-openorca",
    "prompt": question, 
    "system": systemPrompt,
    "stream": False, 
    "context": context
    }

    # Convert the payload to a JSON string
    payload_json = json.dumps(payload)

    # Set the headers to specify JSON content
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, data=payload_json, headers=headers)

    # Check the response
    if response.status_code == 200:
        output = json.loads(response.text)
        context = output['context']
        print(output['response'])
        

    else:
        print(f"Request failed with status code {response.status_code}")
    t4 = time.time()
    print(f'inference:{t4-t3}')
    return output

    