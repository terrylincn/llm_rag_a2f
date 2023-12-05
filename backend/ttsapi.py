from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, StreamingResponse
import os
import io
import time
from typing import Optional
import numpy as np
import struct
import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts_cn = TTS("tts_models/zh-CN/baker/tacotron2-DDC-GST").to(device)
tts_en = TTS("tts_models/en/ljspeech/tacotron2-DDC").to(device)
#tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1").to(device)

app = FastAPI()


@app.post("/api/generate")
async def generate(content: str = Form(...), language: Optional[str] = Form(default='zh-CN')):
    if language == 'zh-CN':
        wav = tts_cn.tts(text = content)
    elif language == 'en':
        wav = tts_en.tts(text = content) 
    print(len(wav))

    #speech = np.asarray(wav) * 32768
    #data16 = speech.astype(np.int16)

    import soundfile as sf
    import io

    sample_rate = 22050 

    # Create a BytesIO object to hold the audio data in memory
    memory_file = io.BytesIO()

    # Write the audio data to the in-memory file
    sf.write(memory_file, wav, sample_rate, format='WAV')

    # To use the audio data, you can seek back to the beginning of the in-memory file
    memory_file.seek(0)
    # 创建 StreamingResponse，返回二进制内容
    return StreamingResponse(memory_file, media_type="audio/x-wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8087)

