
open omniverse audio2face, and open the file data/claire.usd

pip install -r requirements.txt

how to start LLM service?
if you are using ollama, just install ollama, and launch it with: ollama serve
if you are using native llama, following these commands:
cd backend
python3 llamaapi.py

how to start TTS service?
cd backend
python ttsapi.py

in case you launch all the services in another machine, change the url in the settings.py

how to start the web ui?
launch python web.py

use your favorite browsewr to open static/chatbox.html