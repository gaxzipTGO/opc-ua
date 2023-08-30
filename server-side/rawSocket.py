from socket import socket, SOCK_RAW, AF_PACKET
from rawsocket.linklayer import Ethernet

class PFPacketSender:
    def __init__(self, interface):
        self.sock = socket(AF_PACKET, SOCK_RAW)
        self.sock.bind((interface, 0))

    def send(self, frame):
        self.sock.send(frame)

    def __str__(self):
        return "PF_PacketSender"


class Logger:
    ....
    ....

def parse_args():
    ....
    ....

def main():
    args = parse_args()
    log = Logger().get_logger("main")
    log.info("Starting....")
    src_mac = None
    with open("/sys/class/net/%s/address" % args.interface) as f:
        src_mac = f.read().strip()

    ether = Ethernet(log, PFPacketSender(args.interface), src_mac)
    ether.xmit("ARP", hex(123))


if __name__ == '__main__':
    main()