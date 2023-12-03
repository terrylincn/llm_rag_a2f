
from audio2face_client import push_audio_track_stream
from settings import *
import threading
import soundfile
import io
import queue
import time

audio_q = queue.Queue()

def audio2face_thread():
    while True:
        if not audio_q.empty():
            wav = audio_q.get()
            audio_file = io.BytesIO(wav)
            data, samplerate = soundfile.read(audio_file, dtype="float32")
            push_audio_track_stream(a2f_url, data, samplerate, instance_name)
        else:
            time.sleep(0.1)

t1 = threading.Thread(target=audio2face_thread, args=())
t1.start()

def audio2face(wav):
    audio_q.put(wav)