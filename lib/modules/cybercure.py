#!/usr/bin/env python
##
# Developed by Alex (https://github.com/grispan56)
# Module to implement indicators search functionality in cybercure.ai api
#
##
from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['cybercure'] = None


    def run(self):
        url = f"http://api.cybercure.ai/feed/search?value={self.artifact['name']}"
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)
            if status:
                results = response.json()
                self.artifact['data']['cybercure'] = results
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact

