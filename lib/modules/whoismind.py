#!/usr/bin/env python
##
# omnibus - deadbits.
# Whois Mind lookup module
##
import BeautifulSoup

from http import get
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['whoismind'] = []
        self.headers = {'User-Agent': 'OSINT Omnibus (https://github.com/InQuest/Omnibus)'}


    def run(self):
        url = f"http://www.whoismind.com/emails/{self.artifact['name']}.html"

        try:
            status, response = get(url, headers=self.headers)

            if status:
                content = BeautifulSoup(response.content, 'lxml')
                a_tag = content.findAll('a')

                for tag in a_tag:
                    if tag.text in tag['href'] and tag.text not in self.artifact['data']['whoismind']:
                        self.artifact['data']['whoismind'].append(tag.text)

        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
