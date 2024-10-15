

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import logging
from channels.layers import get_channel_layer

logger = logging.getLogger("websocket_notification")

class UIWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        context = f"UIWebsocketConsumer.connect"
        logger.info(f"{context},establishing new socket connection...")
        logger.info(f"{context},scope:{self.scope}")
        self.user_id = self.scope.get('user_id')
        async_to_sync(self.channel_layer.group_add)(
            self.user_id,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        context = "UIWebsocketConsumer.disconnect"
        logger.info(f"{context},closing socket connection...")
        logger.info(f"{context},scope:{self.scope}")
        async_to_sync(self.channel_layer.group_discard)(
            self.user_id,
            self.channel_name
        )
    
    def send_message(self,event):
        context = "UIWebsocketConsumer.send_message"
        message = event['message']
        logger.info(f"{context},sending message:{message}")
        self.send(text_data=message)

    def send_websocket_notification_to_user(self,user_id,message):
        context = "UIWebsocketConsumer.send_notification_to_user"
        logger.info(f"{context},sending websocket notification to user,user_id:{user_id},message:{message}")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_id,
            {
                'type': 'send_message',
                'message': message
            }
        )
    
    def receive(self, text_data):
        context = "UIWebsocketConsumer.receive"
        logger.info(f"{context},received message from client,scope:{self.scope},text_data:{text_data}")

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print([1]*30)
#         print(self.scope)
#         print([2]*30)
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         print(self.scope['headers'],type(self.scope['headers']))
#         self.room_group_name = f'chat_{self.room_name}'
#         print([3]*30)
#         print(self.channel_layer)
#         print([4]*30)
#         print(self.room_group_name)
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         print([4]*30)
#         print(self.channel_layer)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': text_data
#             }
#         )

#     def chat_message(self, event):
#         print(['#']*30)
#         message = event['message']
#         self.send(text_data=message)



def func(user_id,message):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        user_id,
        {
            'type': 'send_message',
            'message': message
        }
    )