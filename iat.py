# coding=utf-8

import commands

def get_text():
    (stat, output) = commands.getstatusoutput("./iat")
    if (stat == 0):
       return output
    else:
        print "Failed, output: %s" %output
