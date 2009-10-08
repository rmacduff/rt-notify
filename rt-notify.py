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

QUERY = "\"Owner=\'Nobody\' AND ( Status=\'new\' OR Status=\'open\' ) AND ( Queue!=\'spambin\' AND Queue!=\'maildrop\' AND Queue!=\'learnspam\' )\""
TIME = 300 # in seconds
KEEP_STATE = True
RT_CLI = "/usr/bin/rt-3.6"


seen_queue = []
out_queue = []

if __name__ == '__main__':
    if not pynotify.init("Urgency"):
        sys.exit(1)

    rt_cmd = [RT_CLI + " ls " + QUERY]
    rt_img = "file://" + os.path.abspath(os.path.curdir) + "/rt_img.png"

    while True:
        output = subprocess.Popen(rt_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        # Do nothing if it returns "No matching results."
        pat = "^No matching results."
        match = re.match(pat, output)

        if not match:
            for line in output.split('\n'):
                if len(line.strip()) == 0:
                    pass

                ticket_id = line.split(':')[0]

                if KEEP_STATE:
                    if ticket_id not in seen_queue:
                        seen_queue.append(ticket_id)
                        out_queue.append(line)
                        # keep the seen queue from growing too large (improve this)   
                        if len(seen_queue) > 50:
                            seen_queue.pop(0)
                    else:
                        pass
                else:
                    out_queue.append(line)

                #done for loop

            if len(out_queue) != 0:
                n = pynotify.Notification("RT Notice", '\n'.join(out_queue), rt_img)
                n.set_urgency(pynotify.URGENCY_LOW)
            
                if not n.show():
                    print "Failed to send notification"
                    sys.exit(1)

                out_queue = []
            
        time.sleep(TIME)
