import asyncio
import websockets
import numpy as np
import json
import cv2
import base64
import time

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print('quit')
    quit()
ret, frame = capture.read()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]


# 向服务器端实时发送视频截图
async def send_video(websocket):
    global ret, frame
    # global cam
    while True:
        if not ret:
            continue
        time.sleep(0.1)

        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        img = data.tobytes()
        # base64编码传输
        img = base64.b64encode(img).decode()

        send_data = {"data_type": "video", "message": "data:image/jpg;base64," + img}

        await websocket.send(json.dumps(send_data))
        ret, frame = capture.read()


async def main_logic():
    while True:
        try:
            async with websockets.connect('ws://127.0.0.1:8000/live/ws/3/') as websocket:
                await send_video(websocket)
        except Exception as e:
            print("111", e)
            async with websockets.connect('ws://127.0.0.1:8000/live/ws/3/') as websocket:
                await send_video(websocket)


asyncio.run(main_logic())
