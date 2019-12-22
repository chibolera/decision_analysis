from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer

class AgentConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            text_data_json
        )

    # Receive message from room group
    def send_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message
        }))

def send_to_ws(serializer, group_name, from_government=True, buy=False, seller=None):
    print("AAAAAAAAAAAAAAAAAAAAAAAA++++++++++++++++++++++++")
    channel_layer = get_channel_layer()
    data = serializer.data
    if not from_government:
        data = {
            'from_government': from_government,
            'others': serializer.data,
        }
    else:
        data['buy'] = buy
    if seller:
        data['quantity'] = seller.quantity,
        async_to_sync(channel_layer.group_send)(
            seller,
            {
                'type': "send_message",
                'message': data
            }
        )
    if 'quantity' in data:
        del data['quantity']
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': "send_message",
            'message': data
        }
    )

def send_to_front(log_serializer):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "front",
        {
            'type': "send_message",
            'message': log_serializer.data
        }
    )