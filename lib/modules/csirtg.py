from csirtgsdk.client import Client
from csirtgsdk.search import Search

from common import get_apikey
from common import warning


class Plugin(object):
    def __init__(self, artifact):
        self.artifact = artifact
        self.artifact['data']['csirtg'] = None
        self.api_key = get_apikey('csirtg')
        if self.api_key == '':
            raise TypeError('API keys cannot be left blank | set all keys in etc/apikeys.json')

    def run(self):
        try:
            client = Client(remote='https://csirtg.io/api', token=self.api_key)
            search = Search(client)

            data = search.search(self.artifact['name'])
            if len(data['feed']['indicators']) > 0:
                self.artifact['data']['csirtg'] = search.search(self.artifact['name'])

        except Exception as err:
            warning(f'Caught exception in module ({str(err)})')


def main(artifact):
    plugin = Plugin(artifact)
    plugin.run()
    return plugin.artifact
