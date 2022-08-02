#!/usr/bin/env python
##
# omnibus - deadbits.
# query SANS ISC API
##
import dshield

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['sans'] = None


    def run(self):
        try:
            data = dshield.ip(self.artifact['name'])
            if isinstance(data, dict) and 'ip' in data.keys():
                self.artifact['data']['sans'] = data['ip']
                if data['ip']['hostname'] != '':
                    self.artifact['children'].append({
                        'name': data['ip']['hostname'],
                        'type': 'host',
                        'source': 'SANS ISC',
                        'subtype': 'fqdn'
                    })
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
