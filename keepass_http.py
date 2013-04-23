# -*- coding: utf-8 -*-

import time
import getpass
import os.path
import sys
import base64
import json
import socket
from kptool.keepassdb import keepassdb
import keepass_crypt
from storage import Storage

class KeePassHttpServer:
    def __init__(self, db_path, password):
        self.id = 'KeePassHttpX'
        self.host = 'localhost'
        self.port = 19455
        self.db_path = db_path
        self.password = password
        self.storage = Storage()

    def activate(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))

        while True:
            #print '-- begin while ------'
            server_sock.listen(3)

            #print 'Waiting for connections...'
            client_sock, client_address = server_sock.accept()
            receive_message = client_sock.recv(4096)

            if receive_message.rstrip() == "":
                sys.exit()

            response = self.handle_request(receive_message)

            client_sock.sendall(response)
            client_sock.close()

        server_sock.close()

    def create_response(self, body):
        data = []
        data.append('HTTP/1.1 200 OK')
        data.append('Date: ' + time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
        data.append('Server: python-keypass-http')
        data.append('Connection: close')
        data.append('Content-Type: application/json; charset=utf-8')
        data.append('')
        data.append(body)
        data.append('')

        response = "\n".join(data)

        return response

    def handle_request(self, request):

        #print '-- start handle_request ------'
        #print request
        #print '-- close handle_request ------'

        header, body = request.split('\r\n\r\n')
        response = json.loads(body)

        if response['RequestType'] == 'associate':
            response['Id'] = 'KeePassHttpX'
            response['Success'] = False

            key = base64.b64decode(response['Key'])
            iv  = base64.b64decode(response['Nonce'])
            verifier = base64.b64decode(response['Verifier'])

            kpc = keepass_crypt.KeePassCrypt(key, iv)

            if base64.b64encode(iv) == kpc.decrypt(verifier):
                response['Success'] = True

                self.storage.save('body', body);

        elif response['RequestType'] == 'test-associate':
            response = self.test_associate(response)

        elif response['RequestType'] == 'get-logins':
            response = self.get_logins(response)

        else:
            print '-- start unknown request type response ------'
            print response

        http_response = self.create_response(json.dumps(response))
        return http_response

    def test_associate(self, response):
        response['Id'] = self.id
        response['Success'] = False

        storage_data = self.storage.load('body')
        if storage_data is None:
            return response

        keyfile = json.loads(storage_data)

        key = base64.b64decode(keyfile['Key']);
        iv  = base64.b64decode(keyfile['Nonce'])
        verifier = base64.b64decode(keyfile['Verifier'])

        kpc = keepass_crypt.KeePassCrypt(key, iv)

        if base64.b64encode(iv) == kpc.decrypt(verifier):
            response['Success'] = True

        return response

    def get_logins(self, response):
        response['Id'] = self.id
        response['Success'] = True

        keyfile = json.loads(self.storage.load('body'))
        key = base64.b64decode(keyfile['Key']);
        iv = base64.b64decode(response['Nonce'])

        kpc = keepass_crypt.KeePassCrypt(key, iv)
        url = kpc.decrypt(base64.b64decode(response['Url']))

        k = keepassdb.KeepassDBv1(self.db_path, self.password)
        response['Entries'] = []
        for e in k.find_entries(url):
            entry = {}
            entry['Name']     = base64.b64encode(kpc.encrypt(e['title']))
            entry['Login']    = base64.b64encode(kpc.encrypt(e['username']))
            entry['Uuid']     = base64.b64encode(kpc.encrypt(e['id']))
            entry['Password'] = base64.b64encode(kpc.encrypt(e['password']))
            response['Entries'].append(entry)

        return response

if __name__ == "__main__":

    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print "Usage: keepass_http.py KeePassDBPath"
        sys.exit()

    db_path = sys.argv[1]
    print "KeePass DB v1 path:" + db_path

    password = getpass.getpass("Enter Password: ")

    server = KeePassHttpServer(db_path, password)
    server.activate()

