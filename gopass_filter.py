#!/usr/bin/env python

import os
import sys
import logging
import subprocess
import json
import re

logging.basicConfig(filename='/tmp/gopassalfred.log', level=logging.DEBUG)
query = sys.argv[1] if len(sys.argv) > 1 else ""
logging.debug('Debug log started, called with {}'.format(query))

my_env = os.environ.copy()
my_env['PATH'] = '/usr/local/bin:{}'.format(my_env['PATH'])

gopass = subprocess.Popen(['/usr/local/bin/gopass', 'list', '-f'], stdout=subprocess.PIPE, env=my_env)
fzy = subprocess.Popen(['/usr/local/bin/fzy', '-e', query], stdin=gopass.stdout, stdout=subprocess.PIPE, env=my_env)

gopass.stdout.close()
stdout, stderr = fzy.communicate()

outlist = [
    {
        "uid": result,
        "title": result.split('/')[-1],
        "subtitle": '/'.join(result.split('/')[:-1]),
        "arg": result,
        "match": " ".join(set(re.split('[. /\-]', result))) + ' ' + result,
        "autocomplete": result
    } for result in stdout.decode('ascii').splitlines()
]

logging.debug('Matched {} items for: {}'.format(len(outlist), query))

print(json.dumps({'items': outlist}))
