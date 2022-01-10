import asyncio

from .message import MessageType, MessageInterface

class SendPostType(MessageInterface):
    def __init__(self, user, sender):
        super().__init__(user, sender)

    def build(self, follower_user):
        username = self.user.username
        follower_info = self.user.get_user(follower_user)
        timeline = self.user.get_own_timeline()
        signature = self.user.sign(timeline)

        msg = {
            'header': {
                'user': username,
                'signature': signature,
                'type': MessageType.SEND_POSTS.value,
            },
            'content': timeline
        }
        
        return (follower_info, msg)
    
    def send(self, follower_info, msg):
        try:
            asyncio.run(self.sender.publish_one(follower_info, msg))
        except Exception as e:
            print(e)