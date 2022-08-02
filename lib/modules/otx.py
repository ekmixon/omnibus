#!/usr/bin/env python
##
# omnibus - deadbits.
# alienvault otx module
##
from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['otx'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def ip(self):
        url = f"https://otx.alienvault.com:443/api/v1/indicators/IPv4/{self.artifact['name']}/"


        try:
            status, response = get(url)

            if status:
                self.artifact['data']['otx'] = response.json()
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def host(self):
        url = f"https://otx.alienvault.com:443/api/v1/indicators/domain/{self.artifact['name']}/"


        try:
            status, response = get(url)

            if status:
                self.artifact['data']['otx'] = response.json()
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def hash(self):
        url = f"https://otx.alienvault.com:443/api/v1/indicators/file/{self.artifact['name']}/"


        try:
            status, response = get(url)

            if status:
                self.artifact['data']['otx'] = response.json()
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def run(self):
        if self.artifact['type'] == 'host':
            if self.artifact['subtype'] == 'ipv4':
                self.ip()
            elif self.artifact['subtype'] == 'fqdn':
                self.host()
        elif self.artifact['type'] == 'hash':
            self.hash()
        else:
            warning('OTX module accepts artifact types host or hash')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
