# -*- coding: utf-8 -*-

import socket
import datetime
import os
import urllib
from threading import Thread
from discription import STATUSES, CONTENT_TYPE, SIZE_PACKET, VERSION

def get_pars_headers_one(data):
        indexFirst = data.index(' ')
        indexLast = data.rindex(' ')
        return data[0:indexFirst], data[indexFirst + 1:indexLast], data[indexLast - 1:]  

def get_response(status, content_type, response_data, method):
        con_type = ''
        try:
                con_type = CONTENT_TYPE[content_type]
        except:
                con_type = CONTENT_TYPE['html']

        response  = VERSION + ' ' + str(status) + ' ' + STATUSES[status] + '\r\n'
        response += 'Date: ' + str(datetime.datetime.now()) + '\r\n'
        response += 'Content-Length: ' + str(len(response_data)) + '\r\n'       
        response += 'Content-Type: ' + con_type + '\r\n'
        response += 'Server: http_server\r\n'
        response += 'Connection: close\r\n'

        return response, response_data, method

def parse_request(data):
        try:
                request = list()

                for line in data.splitlines():
                        request.append(line)

                method, url, version = get_pars_headers_one(request[0])
                
                if 'GET' in method or 'HEAD' in method:

                        url = urllib.unquote(url).split('?')[0]

                        parse_url = url.split('.')
                        len_parse_url = len(parse_url)
                        path_req = parse_url[0]

                        if len_parse_url > 1: 
                                content_type_req = parse_url[len_parse_url - 1].lower()
                                
                        try:
                                path = os.path.abspath(os.path.dirname(__file__)) + url
                                path_check = os.path.abspath(os.path.dirname(__file__)) + os.path.abspath(os.path.relpath(url))
                                if path_check in path and os.path.exists(path):
                                        if os.path.isdir(path):
                                                if os.path.exists(path + 'index.html'):
                                                        with open(path + 'index.html') as file:
                                                                data_response = file.read()
                                                                return get_response(200, 'html', data_response, method)  
                                                else: 
                                                        return get_response(403, 'html', '___403___', method)
                                        else:
                                                with open(path) as file:
                                                        data_response = file.read()
                                                        return get_response(200, content_type_req, data_response, method)
                                else:
                                        return get_response(404, 'html', '___404___', method)
                        except:
                                return get_response(403, 'html', '___403___', method)                            
                else:   
                        return get_response(405, 'html', '___405___', 'GET')         
        except:
                return get_response(404, 'html', '___404___', 'GET')

def thread_fun(client_socket):
        request = client_socket.recv(SIZE_PACKET)
        response_headers, response_data, method = parse_request(request)
        client_socket.send(response_headers)
        client_socket.send('\r\n')
        if 'GET' in method:
                client_socket.send(response_data)
        client_socket.close()
        print('closed client socket')       
                
def start_new_thread(client_socket):
        print('start thread')
        thread = Thread(target=thread_fun, args=(client_socket,))
        thread.start()
   
def httpServerStart():
        hostname = 'localhost'
        port = 8080
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((hostname, port))
        server_socket.listen(10)

        while True:
                client_socket, client_data = server_socket.accept()
                start_new_thread(client_socket)
           
httpServerStart()
