
from audio2face_client import push_audio_track_stream
from settings import *
import threading
import soundfile
import io

def audio2face(wav):
    audio_file = io.BytesIO(wav)
    data, samplerate = soundfile.read(audio_file, dtype="float32")
    t1 = threading.Thread(target=push_audio_track_stream, args=(a2f_url, data, samplerate, instance_name,))
    t1.start()