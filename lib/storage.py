#!/usr/bin/env python
##
# omnibus - deadbits.
# output storage management
##
import os
import json

from common import timestamp

from common import error
from common import success
from common import warning


class JSON(object):
    def __init__(self, data, file_path=None, file_name='report.json', create=True):
        self.data = data
        self.file_path = None

        if file_name == 'report.json':
            self.file_name = f"{data['name']}_{timestamp}.json"
        else:
            self.file_name = file_name

        if file_path:
            self.set_filepath(file_path, file_name, create)


    def set_filepath(self, file_path, file_name, create=True):
        if os.path.isdir(file_path):
            self.file_path = os.path.join(file_path, file_name)
            if not os.path.exists(self.file_path):
                self.save()
                success(f'saved report to {self.file_path}')
        else:
            error(f'unable to find directory {file_path} - cannot save report')

        return False


    def save(self):
        if self.file_path:
            with open(self.file_path, 'wb') as fp:
                json.dump(self.data, fp)
        else:
            warning('file path not correctly set - cannot save report')
