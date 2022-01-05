import argparse
import logging
import asyncio

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address of existing node", type=str, default=None)
    parser.add_argument("-p", "--port", help="port number of existing node", type=int, default=None)
    parser.add_argument("-b", "--bootstrap", help="Bootstrap on or off", type=bool, default=False)

    return parser.parse_args()


def connect_to_bootstrap_node(args):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(interface=args.ip, port=args.port))
    
    bootstrap_node = (args.ip, 8001)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def create_bootstrap_node(args):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    
    loop.run_until_complete(server.listen(interface=args.ip, port=args.port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


# def create_node(ip,port):
#     loop = asyncio.get_event_loop()
#     loop.set_debug(True)
#     loop.run_until_complete(server.listen(interface="127.0.0.1", port=port))

#     bootstrap_node = (ip, port)
#     loop.run_until_complete(server.bootstrap([bootstrap_node]))

#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         server.stop()
#         loop.close()


def main():
    args = parse_arguments()

    if(args.bootstrap):
        create_bootstrap_node(args)
    else:
        connect_to_bootstrap_node(args)


    # create_node(args.ip,args.port)



    # if args.ip and args.port:
    #     connect_to_bootstrap_node(args)
    # else:
    #     create_bootstrap_node()


if __name__ == "__main__":
    main()