import asyncio
import zmq
import zmq.asyncio
import json
import threading

from src.connection.message import MessageType
from src.utils.logger import Logger
"""
def subs(url, channel):
    import asyncio

    import zmq
    import zmq.asyncio

    ctx = zmq.asyncio.Context.instance()

    async def task():
        sock = ctx.socket(zmq.SUB)
        sock.connect(url)
        sock.setsockopt(zmq.SUBSCRIBE, channel.encode())

        try:
            while True:
                msg = await sock.recv_multipart()
                print(' | '.join(m.decode() for m in msg))
        finally:
            sock.setsockopt(zmq.LINGER, 0)
            sock.close()

    asyncio.run(task())
"""
class MessageReceiver:
    def __init__(self, user, listening_ip : str, listening_port : int) -> None:
        self.user = user

        self.listener_action_list = {
            MessageType.TIMELINE_MESSAGE.value: self.user.receive_timeline_message,
            MessageType.REQUEST_TIMELINE.value: self.user.send_timeline,
            MessageType.SEND_TIMELINE.value: self.user.receive_timeline,
        }  

        self.ctx = zmq.asyncio.Context.instance()
        self.socket = self.ctx.socket(zmq.PULL)
        self.socket.bind(f'tcp://{listening_ip}:{listening_port}')

        #self.loop = asyncio.new_event_loop()
        #self.loop.run_until_complete(self.task)
        threading.Thread(target=self.listening_thread, daemon=True).start()
        

    def listening_thread(self):
        asyncio.run(self.task())
    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def listener_action(self, action : int, message) -> None:
        if self.user.verify_signature(message['content'], message['header']['user'], message['header']['signature']):
            self.listener_action_list[action](message)

    # --------------------------
    # -- Listener Loop 
    # --------------------------
    async def task(self):
        print("Aqui")
        try:
            while True:
                msg = await self.socket.recv_multipart()
                print(' | '.join(m.decode() for m in msg))
        finally:
            print("Fecha")
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()

    def recv_msg_loop(self) -> None:
        while True:
            message = self.socket.recv_string()
            msg = json.loads(message)
            Logger.log("MessageReceiver", "info", f"RECV {msg}")

            self.listener_action(msg['header']['type'], msg)
