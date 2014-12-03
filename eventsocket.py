import types
import re


class BaseEventSocket(object):

    def __init__(self, *args, **kwargs):
        self.stream = None
        super(BaseEventSocket, self).__init__(*args, **kwargs)

    def _parse_event(self, res):
        lines = res.rstrip().split('\n')
        _ = {}
        for line in lines:
            k, v = line.rstrip().split(': ', 1)
            _.update({
                re.sub('-', '_', k.lower()): v
            })
        return _

    def on_connect(self):
        raise NotImplementedError()

    def send_and_receive(self, chunk):
        raise NotImplementedError()

    def _raw_send(self, chunk):
        if isinstance(chunk, types.UnicodeType):
            chunk = chunk.encode('utf-8')
        return self.send_and_receive(chunk)

    def send(self, chunk):
        return self._raw_send(chunk + '\n\n')

    def send_msg(self, name, arg=None, uuid='', lock=False):
        if isinstance(name, types.UnicodeType):
            name = name.encode('utf-8')
        if isinstance(arg, types.UnicodeType):
            arg = arg.encode('utf-8')

        _res = [
            'sendmsg %s' % uuid,
            'call-command: execute',
            'execute-app-name: %s' % name
        ]
        if arg is not None:
            _res.append('execute-app-arg: %s\n' % arg)
        if lock is True:
            _res.append('event-lock: true\n')
        return self.send('\n'.join(_res))

    def connect(self):
        return self.send('connect')

    def my_events(self):
        return self.send('myevents')

    def set(self, args):
        return self.send_msg('set', args, lock=True)

    def set_global(self, args):
        return self.send_msg('set_global', args, lock=True)

    def unset(self, args):
        return self.send_msg('unset', args, lock=True)

    def playback(self, filename, terminators=None, lock=True):
        self.set('playback_terminators=%s' % terminators or 'none')
        return self.send_msg('playback', filename, lock=lock)

    def answer(self):
        return self.send_msg('answer', lock=True)

    def bridge(self, args):
        return self.send('bridge %s' % args, lock=True)

    def hangup(self, reason=''):
        return self.send_msg('bridge', reason, lock=True)

    def sleep(self, ms):
        return self.send_msg('sleep', ms, lock=True)

    def transfer(self, args):
        return self.send_msg('transfer', args, lock=True)
