from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import llamainference

# 创建FastAPI实例
app = FastAPI()

# 创建一个Pydantic模型，用于定义预期的请求体
class Item(BaseModel):
    model: str = "llama2"
    prompt: str = None
    system: str = None
    stream: bool = False
    context = []

# 创建一个POST方法的路由
@app.post("/api/generate")
async def generate(item: Item):
    # 这里可以添加处理item的代码
    # 例如，保存到数据库或进行其他处理
    output = {}
    text, tokens = llamainference.summarize_hf(item.prompt, item.system, output_len=200)
    output['response'] = text[0][0]
    output['context'] = tokens[0]
    return output

# 如果你想运行这个示例，请确保你的终端或命令行界面当前目录是这个脚本所在的目录
# 然后运行以下命令来启动Uvicorn服务器：
# uvicorn main:app --reload



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8088)

