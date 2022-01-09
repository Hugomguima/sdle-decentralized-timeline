import threading

from src.cli import AuthMenu, MainMenu
from src.api import Authentication, User
from src.server import KademliaNode

class Core:
    def __init__(self, ip, port, initial):
        if initial: 
            self.node = KademliaNode(ip, port)
        else: 
            self.node = KademliaNode(ip, port, ("127.0.0.1", 8000))

        self.user = None
        self.loop = self.node.run()
        self._run_kademlia_loop()
        
    def _run_kademlia_loop(self):
        """
        Start running kademlia loop
        """
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def cli(self):
        self.authentication = Authentication(self.node)
        # print(self.authentication.actions)
        answers = AuthMenu.menu()
        self.user = User(*self.authentication.action(answers['method'], answers['information']))

        # print(self.user.actions)
        while True:
            answers = MainMenu().menu()
            self.user.action(answers['action'], answers['information'])