import os
import asyncio

from .message import MessageType, MessageInterface

class RequestPostType(MessageInterface):
    def __init__(self, user, sender):
        super().__init__(user, sender)

    def build(self, followed_user):
        username = self.user.username
        followed_info = self.user.get_user(followed_user)
        random_check = str(os.urandom(32))
        signature = self.user.sign(random_check)

        msg = {
            'header': {
                'user': username,
                'signature': signature,
                'followed': followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
            'content': random_check,
        }

        return (followed_info, msg)

    def send(self, followed_info, msg):
        try:
            asyncio.run(self.sender.publish_one(followed_info, msg))
        except Exception as e:
            print(e)