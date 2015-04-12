Freeswitch EventSocket
======================

This is a work in progress abstraction class to handle freeswitch's
eventsocket command lines.

Currently only inbound server is implemented.


Installation
============

..code-block:: bash

    pip install freeswitch-eventsocket



Implementation under Tornado's IOLoop
-------------------------------------

Here is a simple server implementation under `Tornado
<http://www.tornadoweb.org/>`_

.. code-block:: python

    import eventsocket

    from tornado.tcpserver import TCPServer
    import tornado.ioloop
    from tornado.gen import coroutine, Return


    class TestServer(eventsocket.BaseEventSocket, TCPServer):

        @coroutine
        def handle_stream(self, stream, address):
            self.stream = stream
            self.on_connect()

        @coroutine
        def send_and_receive(self, chunk):
            yield self.stream.write(chunk)
            _ = yield self.stream.read_until_regex(b'\n\n')
            raise Return(self._parse_event(_))

        @coroutine
        def on_connect(self):
            print 'connected!'
            data = yield self.connect()
            print data
            yield self.my_events()
            yield self.answer()
            yield self.playback(
                '{loops=10}tone_stream://path=${base_dir}/conf/tetris.ttml',
                lock=True
            )


    if __name__ == '__main__':
        server = TestServer()
        server.listen(8888, '0.0.0.0')
        tornado.ioloop.IOLoop.instance().start()



Implementation under Twisted's Reactor
--------------------------------------

Here is a simple server implementation under `Twisted
<https://twistedmatrix.com/>`_

.. code-block:: python

    import eventsocket

    from twisted.internet import defer, protocol
    from twisted.protocols import basic

    from cStringIO import StringIO


    class TestServer(eventsocket.BaseEventSocket, basic.LineReceiver):

        delimiter = '\n'

        def __init__(self, *args, **kwargs):
            self.stream = None
            self._io = StringIO()
            self._queue = []
            super(TestServer, self).__init__(*args, **kwargs)

        def lineReceived(self, line):
            if len(line) > 0:
                self._io.write('%s\n' % line)
            else:
                self.dispatch_event()

        def dispatch_event(self):
            try:
                deferred = self._queue.pop(0)
            except IndexError:
                pass
            else:
                self._io.reset()
                _ = self._parse_event(self._io.read())
                deferred.callback(_)
                self._io.reset()
                self._io.truncate()

        def send_and_receive(self, chunk):
            deferred = defer.Deferred()
            self._queue.append(deferred)
            self.transport.write(chunk)
            return deferred

        @defer.inlineCallbacks
        def connectionMade(self):
            print 'connected!'
            data = yield self.connect()
            print data
            yield self.my_events()
            yield self.answer()
            yield self.playback(
                '{loops=10}tone_stream://path=${base_dir}/conf/tetris.ttml',
                lock=True
            )


    class PubFactory(protocol.Factory):

        def buildProtocol(self, addr):
            return TestServer()


    if __name__ == '__main__':
        from twisted.internet import reactor

        reactor.listenTCP(8888, PubFactory())
        reactor.run()


Freeswitch EventSocket is available under
the `Apache License, Version 2.0
<http://www.apache.org/licenses/LICENSE-2.0.html>`_.
