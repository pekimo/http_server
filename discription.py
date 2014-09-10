# -*- coding: utf-8 -*-


SIZE_PACKET = 267037
VERSION     = 'HTTP/1.1'
METHOD      = 'GET'

STATUSES = {
	200: 'OK',
	400: 'Bad Request',
	403: 'Forbidden',
	404: 'Not Found',
	405: 'Method not Allowed'
}

CONTENT_TYPE = {
	'html': 'text/html',
	'css' : 'text/css',
	'js'  : 'text/javascript',
	'jpg' : 'image/jpeg',
	'jpeg': 'image/jpeg',
	'png' : 'image/png',
	'gif' : 'image/gif',
	'swf' : 'application/x-shockwave-flash'
}