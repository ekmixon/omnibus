#!/usr/bin/env python
##
# omnibus - deadbits
# hurricane eletric
##
import re

from BeautifulSoup import BeautifulSoup

from http import get

from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['he'] = None


    def ip(self):
        url = f"http://bgp.he.net/ip/{self.artifact['name']}#_dns"
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)

            if status:
                data = BeautifulSoup(response.text)

                result = [
                    item.text.strip()
                    for item in data.findAll(
                        attrs={'id': 'dns', 'class': 'tabdata hidden'}
                    )
                ]

        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def fqdn(self):
        url = f"http://bgp.he.net/dns/{self.artifact['name']}#_whois"
        headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}

        try:
            status, response = get(url, headers=headers)

            if status:
                pattern = re.compile('\/dns\/.+\".title\=\".+\"\>(.+)<\/a\>', re.IGNORECASE)
                hosts = re.findall(pattern, response.text)
                result = [h.strip() for h in hosts]
        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


    def run(self):
        if self.artifact['subtype'] == 'ipv4':
            self.artifact['data']['he'] = self.ip()

        elif self.artifact['subtype'] == 'fqdn':
            self.artifact['data']['he'] = self.fqdn()


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
