import json

from channels.generic.websocket import JsonWebsocketConsumer
from django.shortcuts import render

# Create your views here.

class EchoConsumer(JsonWebsocketConsumer):

    def websocket_connect(self, event):
        self.accept()

    def websocket_receive(self, event):
        self.send(json.dumps({
            "type": "websocket.send supcon",
            "text": event["text"],
        }))


    def websocket_message(self, event):
        self.send(json.dumps({
            "type": "websocket.send jackie",
            "text": event["text"],
        }))

    def websocket_disconnect(self, event):
        self.send(json.dumps({
            "type": "websocket.send",
            "text": event["text"],
        }))