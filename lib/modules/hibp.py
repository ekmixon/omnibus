#!/usr/bin/env python
##
# omnibus - deadbits
# haveibeenpwned
##
from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['hibp'] = {'breaches': None, 'pastes': None}
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def breaches(self):
        url = f"https://haveibeenpwned.com/api/v2/breachedaccount/{self.artifact['name']}"


        try:
            status, response = get(url, headers=self.headers)
            if status:
                self.artifact['data']['hibp']['breaches'] = response.json()
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def pastes(self):
        url = f"https://haveibeenpwned.com/api/v2/pasteaccount/{self.artifact['name']}"

        try:
            status, response = get(url, headers=self.headers)
            if status:
                self.artifact['data']['hibp']['pastes'] = response.json()
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def run(self):
        self.breaches()
        self.pastes()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
