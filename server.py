# -*- coding: utf-8 -*-

import socket
import datetime
import os
import urllib
from threading import Thread
from discription import STATUSES, CONTENT_TYPE, SIZE_PACKET, METHOD, VERSION


def get_response(status, content_type, response_data):
        response  = VERSION + ' ' + str(status) + ' ' + STATUSES[status] + '\r\n'

        response += 'Date: ' + str(datetime.datetime.now()) + '\r\n'
        
        response += 'Content-Length: ' + str(len(response_data)) + '\r\n'

        response += 'Content-type: ' + CONTENT_TYPE[content_type] + '\r\n'

        response += 'Connection: close\r\n'
        

        return response.encode(), response_data


def parse_request(data):
        '''try:'''
        request = list()
                
        for line in data.splitlines():
                request.append(line)

        method, url, version = request[0].split(' ')
        print(url)
        if METHOD in method:

                url = url.split('?')[0]
                parse_url = url.split('.')

                len_parse_url = len(parse_url)

                path_req = parse_url[0]
                content_type_req = 'html'
                if len_parse_url == 2: 
                        content_type_req = parse_url[1]
                        
                '''try:'''
                path = os.path.dirname(__file__) + '' + url
                f = open(path, 'rb')
                data_response = f.read()
                print(type(data_response))
                return get_response(200, content_type_req, data_response.decode("utf-8"))
                '''except:
                                return get_response(403, 'html', '___403___')'''
                                                
        else:
                return get_response(405, 'html', '___405___')
                                                                
                                
        '''except:
                return get_response(404, 'html', '___404___')'''


def thread_fun(client_socket):
        request = client_socket.recv(SIZE_PACKET)
        response_headers, response_data = parse_request(request.decode('utf-8'))
        client_socket.send(response_headers)
        client_socket.send(response_data)
        client_socket.close()
        print('closed client socket')       
                
def start_new_thread(client_socket):
        print('start thread')
        thread = Thread(target=thread_fun, args=(client_socket,))
        thread.start()
        
def httpServerStart():
        hostname = 'localhost'
        port = 80
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((hostname, port))
        server_socket.listen(10)

        while 1:
                client_socket, client_data = server_socket.accept()
                start_new_thread(client_socket)

                
httpServerStart()
