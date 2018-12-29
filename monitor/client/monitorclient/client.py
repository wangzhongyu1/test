#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
from oslo_config import cfg
from oslo_config import types
import datetime
from prettytable import PrettyTable
cli_opts = [
    cfg.BoolOpt('verbose',
                short='v',
                default=False,
                help='Print more verbose output.'),
    cfg.BoolOpt('debug',
                short='d',
                default=False,
                help='Print debugging output.'),
    cfg.BoolOpt('test',
                short='t',
                default=False,
                help='Print test output.'),

    cfg.BoolOpt('nova-conf-change-list',
                default=False,
                help='Print nova conf change list output.'),

	   ]

def add_common_opts(conf):
        conf.register_cli_opts(cli_opts)

cf = cfg.CONF
add_common_opts(cf);
#cf(sys.argv[1:])
client = socket.socket()
client.connect(("10.154.4.141", 9999))
while True:
    #print(sys.argv[1:])
    args = str(sys.argv[1:])
    #print(args)
    client.send(args)
    #client.send(args.encode('utf-8'))
    data = client.recv(10240)
    #print(type(data))
    #print("received" + repr(data))
    #print(data)
    list1=eval(data)
    fields = list1[0]
    content=list(list1[1])
    table = PrettyTable(fields)
    table.align = 'l'	
    #print(table)
    #print(content)
    #print(list1[1:])
    for value in content:
    	#print(list(value))
	table.add_row(list(value))
    print(table)
    break
                               
