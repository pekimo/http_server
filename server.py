# -*- coding: utf-8 -*-

import socket
import datetime
import os
import urllib
import time
import multiprocessing as mp
from threading import Thread
from discription import STATUSES, CONTENT_TYPE, SIZE_PACKET, VERSION

def get_pars_headers_one(data):
    indexFirst = data.index(' ')
    indexLast = data.rindex(' ')
    return data[0:indexFirst], data[indexFirst + 1:indexLast], data[indexLast - 1:]  

def get_headers(status, content_type, size):
    con_type = ''
    try:
        con_type = CONTENT_TYPE[content_type]
    except:
        con_type = CONTENT_TYPE['html']

    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())
    response  = VERSION + ' ' + str(status) + ' ' + STATUSES[status] + '\r\n'
    response += 'Date: ' + str(date) + '\r\n'
    response += 'Content-Length: ' + str(size) + '\r\n'       
    response += 'Content-Type: ' + con_type + '\r\n'
    response += 'Server: http_server\r\n'
    response += 'Connection: close\r\n'

    return response

def parse_request(data, client_socket):
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
                                size = os.path.getsize(path + 'index.html')
                                response_headers = get_headers(200, 'html', size)
                                client_socket.send(response_headers)
                                client_socket.send('\r\n')
                                if 'GET' in method:
                                    while 1:
                                        line = file.read(2048)
                                        if not line:
                                            break
                                        client_socket.send(line)
                                return                               
                        else: 
                            response_headers = get_headers(403, 'html', 0)
                            client_socket.send(response_headers)
                            return
                    else:
                        with open(path) as file:
                            size = os.path.getsize(path)
                            response_headers = get_headers(200, content_type_req, size)
                            client_socket.send(response_headers)
                            client_socket.send('\r\n')
                            if 'GET' in method:
                                while 1:
                                    line = file.read(2048)
                                    if not line:
                                        break
                                    client_socket.send(line)
                            return
                else:
                    response_headers = get_headers(404, 'html', 0)
                    client_socket.send(response_headers)
                    return
            except:
                response_headers = get_headers(403, 'html', 0)
                client_socket.send(response_headers)
                return                     
        else:   
            response_headers = get_headers(405, 'html', 0)
            client_socket.send(response_headers)
            return
    except:
        response_headers = get_headers(404, 'html', 0)
        client_socket.send(response_headers)
        return


def thread_fun(client_socket):
    request = client_socket.recv(SIZE_PACKET)
    parse_request(request, client_socket)
    client_socket.close()

   
def worker(socket):
    while True:
        client_socket, client_data = socket.accept()
        thread = Thread(target=thread_fun, args=(client_socket,))
        thread.start()


if __name__ == '__main__':
      
    num_workers = mp.cpu_count()

    print('Cpu_Count: ' + str(num_workers))

    hostname = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((hostname, port))
    server_socket.listen(100)
 
    for i in range(num_workers):
        process = mp.Process(target=worker, args=(server_socket,) )
        process.start()

