#!/usr/bin/env python
##
# omnibus - deadbits.
# geolocation for hosts
##
from http import get

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['geoip'] = None
        self.api_key = get_apikey('ipstack')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = f"http://api.ipstack.com/{self.artifact['name']}?access_key={self.api_key}&hostname=1"


        try:
            status, response = get(url, headers=self.headers)

            if status:
                results = response.json()
                self.artifact['data']['geoip'] = results

                if 'hostname' in results.keys() and results['hostname'] not in [
                    self.artifact['name'],
                    '',
                ]:
                    self.artifact.children.append({
                        'name': results['hostname'],
                        'type': 'host',
                        'subtype': 'fqdn',
                        'source': 'ipstack'
                    })
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
