import requests
import json
from settings import language

def tts_request(text):
    url = "http://13902254981.tpddns.cn:8888/generate2"#"http://localhost:11434/api/generate"

    payload = {
        "content": text,
        "language": language
    }

    try:
        # Send the POST request
        response = requests.post(url, data=payload)

        # Check the response
        if response.status_code == 200:
            output = response.content
            print(len(output))
            return True, output
        else:
            print(response.status_code)
    except Exception as e:
        print(e)
    return False, None