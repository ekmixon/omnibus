#!/usr/bin/env python
##
# omnibus - deadbits
# pgp search
##
import re

from BeautifulSoup import BeautifulSoup

from http import get

from common import re_email
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['pgp'] = None
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def fqdn(self):
        url = f"http://pgp.mit.edu/pks/lookup?op=index&search={self.artifact['name']}"

        try:
            status, response = get(url, headers=self.headers)

            if status and 'No results found' not in response.text:
                data = BeautifulSoup(response.text)
                items = data.fetch('a')
                for item in items:
                    matches = re.findall(re_email, item)
                    for m in matches:
                        if not isinstance(self.artifact['data']['pgp'], list):
                            self.artifact['data']['pgp'] = []
                        self.artifact['data']['pgp'].append(m)
                        self.artifact['children'].append({
                            'name': m,
                            'type': 'email',
                            'source': 'PGP',
                            'subtype': None})

        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def email(self):
        url = f"http://pgp.mit.edu/pks/lookup?op=index&search={self.artifact['name']}"

        try:
            status, response = get(url, headers=self.headers)

            if status and 'No results found' not in response.text:
                data = BeautifulSoup(response.text)
                hrefs = data.fetch('a')

                for href in hrefs:
                    content = href.contents

                    if self.artifact['name'] in content[0]:
                        try:
                            name = content[0].split('&lt;')[0]
                            if not isinstance(self.artifact['data']['pgp'], list):
                                self.artifact['data']['pgp'] = []
                            self.artifact['data']['pgp'].append(name)
                        except IndexError:
                            warning('Unable to parse returned PGP web data')

        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def run(self):
        if self.artifact['type'] == 'email':
            self.email()
        elif self.artifact['type'] == 'fqdn':
            self.fqdn()
        else:
            warning('PGP module only accepts artifact types email or fqdn')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
