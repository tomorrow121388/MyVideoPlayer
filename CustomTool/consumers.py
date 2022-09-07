import json

from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """ 有客户端来向后端发送websocket连接请求时，自动触发"""
        self.accept()  # 服务端允许和客户端创建连接。

        # 获取群号，获取路由匹配中的值
        self.group = self.scope['url_route']['kwargs']["room_id"]
        # print(group)
        async_to_sync(self.channel_layer.group_add)(self.group, self.channel_name)
        # print(self.channel_name)

    def websocket_receive(self, message):
        """浏览器基于websocket向后端发送数据，自动触发接收消息"""
        # text = message['text']
        # print("message->", text)
        # print("---------------", message)

        # 通知组内所有的客户端，执行 xx_oo的方法，在此方法中自己去定义任意的功能
        async_to_sync(self.channel_layer.group_send)(self.group, {
            "type": "ws_send_data",
            "message": message
        })

    def ws_send_data(self, message):
        text = message['message']['text']
        # print(text)
        try:
            self.send(json.dumps(eval(text)))
        except Exception as e:
            print("ws,error", e)

    def websocket_disconnect(self, message):
        """客户端与服务端断开连接时，自动触发"""
        print("0000000000", message, "00000000")
        async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)
        raise StopConsumer()
