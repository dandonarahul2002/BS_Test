from tail import Tail
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os
import asyncio

app = FastAPI()
PATH = 'logfile.log'
logs = Tail(PATH)

@app.get("/")
async def get():
    return HTMLResponse(content=open('templates/client.html').read())

@app.websocket("/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(logs.getLines())
    await websocket.send_text(logs.getLines())
    
    last_read_position = os.path.getsize(logs.file_path)
    print(last_read_position)
    while True and os.path.exists(PATH):
        # if os.path.getsize(PATH) == last_read_position:
        #     continue
        try:
            with open(logs.file_path,'rb') as f:
                f.seek(last_read_position)
                new_data = f.read()
                if new_data:
                    # print(new_data)
                    await websocket.send_text(new_data.decode('utf-8'))
                last_read_position = f.tell()
        except Exception as e:
            pass
        await asyncio.sleep(1)




