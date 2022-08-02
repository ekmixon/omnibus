#!/usr/bin/env python
##
# omnibus - deadbits.
# HTTP requests library
##
import requests
import warnings

from requests.packages.urllib3 import exceptions


# class HTTP(object):
#    def __init__(self, proxy=None):
#        if proxy is not None:
#            self.proxy = {
#                'http': 'socks5://%s' % proxy,
#                'https': 'socks5://%s' % proxy
#            }
#        else:
#            self.proxy = proxy


def post(*args, **kwargs):
    kwargs['verify'] = False

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        # if isinstance(self.proxy, dict):
        #    kwargs['proxies'] = self.proxy

        try:
            req = requests.post(*args, **kwargs)
        except:
            return (False, None)

        return (True, req) if req.status_code == 200 else (False, req)


def get(*args, **kwargs):
    kwargs['verify'] = False

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        # if isinstance(self.proxy, dict):
        #    kwargs['proxies'] = self.proxy

        try:
            req = requests.get(*args, **kwargs)
        except:
            return (False, None)

        return (True, req) if req.status_code == 200 else (False, req)
