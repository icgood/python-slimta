
from pprint import pprint
import shelve
from slimta.edge.smtp import SmtpEdge
from slimta.queue import Queue
from slimta.queue.dict import DictStorage
from slimta.relay import RelayError

class FakeRelay(object):

    def attempt(self, envelope):
        print '------------------------'
        print 'sender: ', envelope.sender
        print 'rcpts:  ', envelope.recipients
        print 'message:', envelope.message
        print
        raise RelayError()

def backoff(envelope, attempts):
    if attempts <= 5:
        return 5.0 * attempts

env_db = shelve.open('envelope.db')
meta_db = shelve.open('meta.db')
queue_storage = DictStorage(env_db, meta_db)
queue = Queue(queue_storage, FakeRelay(), backoff)

edge = SmtpEdge(('127.0.0.1', 1337), queue)
edge.start()
queue.start()
try:
    edge.get()
except KeyboardInterrupt:
    print
finally:
    for key in env_db.keys():
        print 'env', key
    for key in meta_db.keys():
        print 'meta', key
    env_db.close()
    meta_db.close()

# vim:et:fdm=marker:sts=4:sw=4:ts=4
