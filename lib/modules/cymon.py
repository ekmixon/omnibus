#!/usr/bin/env python
##
# omnibus - deadbits.
# cymon.io module
##
import cymon

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['cymon'] = None
        self.api_key = get_apikey('cymon')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')
        self.api = cymon.Cymon(self.api_key)


    def ip(self):
        try:
            self.artifact['data']['cymon'] = self.api.ip_lookup(self.artifact['name'])
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def fqdn(self):
        try:
            self.artifact['data']['cymon'] = self.api.domain_lookup(self.artifact['name'])
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.ip()
        elif self.artifact['subtype'] == 'fqdn':
            self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
