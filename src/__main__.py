import asyncio

from src.authentication import Authentication
from src.server.kademliaServer import KademliaServer
from src.menu import AuthenticationMenu, MainMenu
from src.utils import Logger, Validation

def post_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(user.post(answers['information']['message']), loop)
        return future.result()
    except Exception as e:
        print(e)

def follow_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(user.follow(answers['information']['username']), loop)
        return future.result()
    except Exception as e:
        print(e)

### This method should be called like this: coroutine_prototype(user.follow(answers['information']['username'])
def coroutine_prorotype(routine):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(routine, loop)
        return future.result()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    arguments = Validation.parse_arguments()
    Logger.log('Unknown', 'info', f'IP: {arguments.ip}')
    Logger.log('Unknown', 'info', f'Port: {arguments.port}')
    Logger.log('Unknown', 'info', f'Init Node: {arguments.initial}')

    if Validation.open_port(arguments.ip, arguments.port):
        Logger.log('Unknown', 'error', f'Port is occupied: {arguments.port}')
        exit(1)

    server = KademliaServer(arguments.ip, arguments.port, arguments.initial)

    authentication = Authentication()
    answers = AuthenticationMenu.menu()
    user = None

    if answers['method'] == 'register':
        user = authentication.register_coroutine(server, answers)
    elif answers['method'] == 'login':
        user = authentication.login_coroutine(server, answers)
        
    print(user)

    answers = MainMenu().menu()
    if answers['action'] == 'post':
        post_coroutine(server, answers, user)
    if answers['action'] == 'follow':
        follow_coroutine(server, answers, user)

    # msg_header = Header(host, user, sequence)
    # msg = Message(msg_header, "Send Message")
    # return msg
