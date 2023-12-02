from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import os
import shutil
import searchk

app = FastAPI()

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    upload_directory = "uploaded_files"
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
text: str = Form(...,title="",description=""), 
):
    ret = searchk.query(text)
    return ret

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
