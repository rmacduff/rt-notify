#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pynotify
import sys
import os
import subprocess
import re
import time

if __name__ == '__main__':
    if not pynotify.init("Urgency"):
        sys.exit(1)

    rt_cmd = ['rt ls "Owner=\'Nobody\' AND ( Status=\'new\' OR Status=\'open\') AND ( Queue!=\'spambin\' AND Queue!=\'maildrop\' AND Queue!=\'learnspam\' )"']
    rt_img = "file://" + os.path.abspath(os.path.curdir) + "/rt_img.png"

    while True:
        output = subprocess.Popen(rt_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        # Nothing if it returns "No matching results."
        pat = "^No matching results."
        match = re.match(pat, output)

        if not match:
            n = pynotify.Notification("RT Notice", output, rt_img)
            n.set_urgency(pynotify.URGENCY_LOW)

            if not n.show():
                print "Failed to send notification"
                sys.exit(1)
            
        time.sleep(300)
