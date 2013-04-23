import objc
from AppKit import *
from PyObjCTools.KeyValueCoding import *

class Storage:

    def __init__(self):
        self.defaults = NSUserDefaultsController.sharedUserDefaultsController().values()

    def save(self, key, body):
        self.defaults.setValue_forKey_(body, key)

    def load(self, key):
        body = getKey(self.defaults, key)
        #if body is None:
        #    body = '{"RequestType": "associate", "Key":"default", "Nonce": "default", "Verifier":"default"}';
        return body

    def save_file(self, body):
        file_handle = open('keyfile.txt', 'w')
        file_handle.write(body)
        file_handle.close()

    def load_file(self):
        return open('keyfile.txt').read()


