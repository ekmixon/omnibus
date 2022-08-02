#!/usr/bin/env python
import os
import re
import sys
import json
import string
import datetime
import ConfigParser

from pygments import lexers
from pygments import highlight
from pygments import formatters


jsondate = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None

# regex patterns courtesy of https://github.com/yolothreat/utilitybelt
re_ipv4 = re.compile('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', re.I | re.S | re.M)
re_ipv6 = re.compile('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', re.I | re.S | re.M)
re_email = re.compile("\\b[A-Za-z0-9_.]+@[0-9a-z.-]+\\b", re.I | re.S | re.M)
re_fqdn = re.compile('(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', re.I | re.S | re.M)
re_cve = re.compile("(CVE-(19|20)\\d{2}-\\d{4,7})", re.I | re.S | re.M)
re_url = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.I | re.S | re.M)
re_md5 = re.compile("\\b[a-f0-9]{32}\\b", re.I | re.S | re.M)
re_sha1 = re.compile("\\b[a-f0-9]{40}\\b", re.I | re.S | re.M)
re_sha256 = re.compile("\\b[a-f0-9]{64}\\b", re.I | re.S | re.M)
re_sha512 = re.compile("\\b[a-f0-9]{128}\\b", re.I | re.S | re.M)
re_btc = re.compile('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')

BOLD = "\033[1m"
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
PURPLE = '\033[95m'
DARKBLUE = '\033[38;5;24m'
END_COLOR = '\033[0m'

API_CONF = f'{os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))}/etc/apikeys.json'


def bold_msg(msg):
    """Bold a message"""
    print(f'{BOLD}{msg}{END_COLOR}')


def info(msg):
    """ Informational message """
    print(f'{BOLD}{DARKBLUE}[*]{END_COLOR} {msg}')


def running(msg):
    """ Background task message """
    print(f'{BOLD}{PURPLE}[*]{END_COLOR} {msg}')


def success(msg):
    """ Successful completion message"""
    print(f'{BOLD}{GREEN}[~]{END_COLOR} {msg}')


def warning(msg):
    """ Non-fatal error message """
    print(f'{BOLD}{YELLOW}[!]{END_COLOR} {msg}')


def error(msg):
    """ Error that stops proper task completion message """
    print(f'{BOLD}{RED}[!]{END_COLOR} {msg}')


def pp_json(data):
    if data is None:
        warning('No data returned from module.')
    else:
        print(highlight(unicode(json.dumps(data, indent=4, default=jsondate), 'UTF-8'),
            lexers.JsonLexer(), formatters.TerminalFormatter()))


def get_option(section, name, conf):
    config = ConfigParser.ConfigParser()
    if not os.path.exists(conf):
        error(f'configuration file {conf} does not exist!')
        return None
    config.read(conf)
    answer = None
    try:
        answer = config.get(section, name)
    except:
        pass
    return answer


def get_apikey(service):
    """ Read API key config file and return API key by service name """
    if os.path.exists(API_CONF):
        api_keys = load_json(API_CONF)
        if service in api_keys.keys():
            return api_keys[service]
    else:
        error(f'cannot find API keys file: {API_CONF}')


def timestamp():
    """ Return UTC timestamp as a string """
    return datetime.datetime.isoformat(datetime.datetime.utcnow())


def required_opt(argument):
    """ Helper for CLI app to ensure all required arguments are there """
    error(f'argument {argument} is required!')
    sys.exit(1)


def list_dir(directory):
    """ Get all files in a given directory """
    files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        files = [f for f in files if f[0] != '.']
        files.extend(os.path.join(root, _file) for _file in files)
    return files


def write_file(file_path, data):
    """ Write data to a specified file path by appending """
    try:
        with open(file_path, 'a+') as fp:
            fp.write(data)
        return True
    except Exception as err:
        raise err


def is_valid(file_path):
    """ Check if a given path is a valid file with data in it """
    return bool(
        os.path.exists(file_path)
        and os.path.isfile(file_path)
        and os.path.getsize(file_path) > 0
    )


def read_file(file_path, lines=False):
    """ Read a given file and optionally return content lines or raw data """
    if is_valid(file_path):
        return (
            (open(file_path, 'rb').read()).split('\n')
            if lines
            else open(file_path, 'rb').read()
        )

    return False


def load_json(file_name):
    """ Load arbitrary JSON files by file name """
    return json.load(open(file_name, 'rb')) if is_valid(file_name) else None


def mkdir(path):
    """ Make a directory if it doesnt already exist """
    if os.path.isdir(path):
        return True
    else:
        try:
            os.mkdir(path)
            os.chmod(path, 0777)
            return True
        except:
            return False


def lookup_key(session, artifact):
    """ Attempt to see if artifact has a valid session key and return if True """
    value = None
    valid_key = False

    if session is None:
        return (valid_key, value)

    try:
        artifact = int(artifact)
        value = session.get(artifact)
        valid_key = True
    except:
        pass

    return (valid_key, value)


def utf_decode(data):
    """ Decode UTF-8 string """
    if isinstance(data, str):
        return data

    try:
        return str(data.decode('utf-8'))
    except ValueError:
        return data


def utf_encode(data):
    """ Encode string as UTF-8 """
    if isinstance(data, bytes):
        return data

    try:
        return data.encode('utf-8')
    except ValueError:
        return data


def is_ipv4(ipv4address):
    """ Check if string is IPv4 address """
    return bool(re.match(re_ipv4, ipv4address))


def is_ipv6(ipv6address):
    """ Check if string is IPv6 address """
    return bool(re.match(re_ipv6, ipv6address))


def is_fqdn(address):
    """ Check if string is a valid domain name """
    return bool(re.match(re_fqdn, address))


def is_url(url):
    """ Check if string is a valid URL """
    return bool(re.match(re_url, url))


def is_email(address):
    """ Check if string is a valid email address """
    return bool(re.match(re_email, address))


def is_hash(string):
    """ Check if string is a valid hash and if so what kind """
    if re.match(re_md5, string):
        return 'md5'
    elif re.match(re_sha1, string):
        return 'sha1'
    elif re.match(re_sha256, string):
        return 'sha256'
    elif re.match(re_sha512, string):
        return 'sha512'
    else:
        return False


def is_btc_addr(string):
    """Check if string is matches as a Bitcoin address.

    @note: This does not verify that the string is a VALID BTC address,
    only that it matches the regex pattern of BTC addresses.
    """
    return 'btc' if re.match(re_btc, string) else False



def detect_type(artifact):
    """ Determine type of given argument """
    if is_ipv4(artifact):
        return 'host'
    elif is_fqdn(artifact):
        return 'host'
    elif is_email(artifact):
        return 'email'
    elif is_hash(artifact):
        return 'hash'
    elif is_btc_addr(artifact):
        return 'btc'
    else:
        try:
            accepted = set(string.ascii_letters + string.digits + '_' + '-')
            if set(artifact) <= accepted:
                return 'user'
        except:
            return None
