#!/usr/bin/env python

import sys

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task
from twisted.python import log

class Sonar(DatagramProtocol):
    def __init__(self, group, port):
        self.group = group
        self.port = port
        self.pingers = set()
        self.pongers = set()

    def startProtocol(self):
        self.transport.joinGroup(self.group)
        task.LoopingCall(self.ping).start(10)

    def ping(self):
        log.msg('pinging')
        self.transport.write('PING!', (self.group, self.port))

    def datagramReceived(self, datagram, address):
        log.msg('received: %r from %r' % (datagram, address))

        if datagram == 'PING!':
            self.transport.write('PONG!', address)
            self.pingers.add(address[0])
            log.msg('pingers: ' + ', '.join(self.pingers))

        if datagram == 'PONG!':
            self.pongers.add(address[0])
            log.msg('pongers: ' + ', '.join(self.pongers))
            

if __name__ == '__main__':
    group = '239.255.0.1'
    port = 1111

    log.startLogging(sys.stderr)

    reactor.listenMulticast(port, Sonar(group, port), listenMultiple=True)
    reactor.run()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
