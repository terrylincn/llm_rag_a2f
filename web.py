from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import searchk
import tts
import a2f

app = FastAPI()
UPLOAD_PATH = os.path.dirname(__file__)

# 设置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，或者你可以指定来源 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

upload_directory = os.path.join(UPLOAD_PATH, "uploaded_files")

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    os.makedirs(upload_directory, exist_ok=True)

    for file in files:
        file_path = os.path.join(upload_directory, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    return {"message": f"Successfully uploaded {len(files)} files."}

# 可选的: 提供一个简单的HTML界面来测试上传
@app.get("/")
async def main():
    content = """
<body>
<form action="/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.post("/search")
async def search(
message: str = Form(...,title="",description=""), 
):
    ret = searchk.query(message)
    text = ret['response']
    
    import re
    import settings
    if settings.language == 'en':
        delimiters = "\.|\n"
    else:
        delimiters = "，|。|\:"  # 分隔符可以是逗号、句号、冒号或空格

    # 使用正则表达式分割字符串
    result = re.split(delimiters, text)

    for text in result:
        print(text)
        if len(text.strip())<=1:
            continue
        #text = text.replace(".","").replace(" ","")
        haswav,wav = tts.tts_request(text=text)
        if haswav:
            a2f.audio2face(wav)

    return ret

@app.post("/build")
async def build(
):
    searchk.rebuild()
    return {"ret": True}

@app.get("/files")
async def list_files():
    files = []
    for filename in os.listdir(upload_directory):
        file_path = os.path.join(upload_directory, filename)
        if os.path.isfile(file_path):
            files.append(filename)
    return files

@app.delete("/files/{file_name}")
async def delete_file(file_name: str):
    file_path = os.path.join(upload_directory, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File '{file_name}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found.")
    
@app.post("/streamingsearch")
async def streamingsearch(
message: str = Form(...,title="",description=""), 
):
    import streamsearchk
    ret = streamsearchk.streamquery(message, streaming_tts)
    return ret

import queue
import threading
import time
tts_q = queue.Queue()

def tts_thread():
    while True:
        if not tts_q.empty():
            text = tts_q.get()
            haswav,wav = tts.tts_request(text=text)
            if haswav:
                a2f.audio2face(wav)
        else:
            time.sleep(0.1)

t1 = threading.Thread(target=tts_thread, args=())
t1.start()
def streaming_tts(text):
    tts_q.put(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
