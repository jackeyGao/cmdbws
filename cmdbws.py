# -*- coding: utf-8 -*-
'''
File Name: cmdbws.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 四  5/14 15:05:17 2015
'''
# -*- coding: utf-8 -*-

from os.path import join
import json
import functools
import requests

version_info = (0, 5, 1)
VERSION = __version__ = '.'.join( map(str, version_info) )


"""
Usage:
cmdb = Cmdbws(username, password)
c = cmdb.get_class("host_ccms_user")
c.list()
c.create(data)
c.update(cid, data)
c.delete(cid)
c.status(cid)
"""


CMDB_HOST = "http://cmdbuild.example.com/services/rest/v1"


class CmdbwsException(Exception):
    def __init__(self, url, status_code, content):
        message = "\nurl:%s\nstatus_code:%s\nMessage:%s" % (url,
                status_code, content)
        Exception.__init__(self, message)


def requests_error_handler(func):
    @functools.wraps(func)
    def deco(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            req = e.args[0]
            content = req.content 
            if 401 == req.status_code:
                content += b" No authentication or authentication failure"
            elif 404 == req.status_code:
                content += b" Page or class name not found, confirm class name"
            elif 500 == req.status_code:
                content += b" An error occurred, Please contact junqi.gao."
            else:
                content += b" An error occurred, It's a unknown error."

            raise CmdbwsException(
                    req.url, req.status_code, content
                )
    return deco

class Cmdbws(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        # Authentication to cmdbuild
        login = self._login()
        self.token = login["data"]["_id"] 
        self.role = login["data"]["role"]
        self.availableRoles = login["data"]["availableRoles"]

    def get_class(self, class_name):
        return CmdbClass(self, class_name)

    def _login(self, **kwargs):
        try:
            url = "%s/sessions/" % CMDB_HOST

            data = json.dumps({"username": self.username, "password": self.password})
            login = self.request('POST', url, data=data) 
            return login
        except Exception as e:
            raise CmdbwsException(url, 500, "authentication failure")

    def build_requests_headers(self):
        token = getattr(self, 'token', None)
        headers = {
            'Content-Type': 'application/json'
        }
        if token is not None:
            headers["CMDBuild-Authorization"] = token
        return headers

    @requests_error_handler
    def request(self, method, url, **kwargs):
        res = requests.request(method, url, headers=self.build_requests_headers(), **kwargs)
        assert res.status_code == 200 or res.status_code == 204, res
        return res.json() if res.text else ''

    def request_real(self, method, url, **kwargs):
        result = self.request(method, url, **kwargs)
        if result is not None:
            return result["data"]
        return result

    def list_class(self):
        """列出所有的class"""
        return self.request_real("GET", join(CMDB_HOST, 'classes'))

    def get_lookup_types(self):
        return self.request_real("GET", join(CMDB_HOST, 'lookup_types'))

    def get_lookup_values(self, lookup_name):
        return self.request_real("GET", join(CMDB_HOST, 'lookup_types', 
            lookup_name, 'values'))


class CmdbClass(object):
    def __init__(self, cmdb, class_name):
        self.cmdb = cmdb
        self.class_name = class_name
        self.url = "%s/classes/%s" % (CMDB_HOST, self.class_name)

        self.info = self.get_info()
        self.attributes = self.get_attributes()

        self.lookups = [ (o["description"],o["lookupType"]) \
                for o in self.attributes if o["lookupType"] is not None ]

    def convert(self, data):
        for card, lookup in self.lookups:
            if card not in data:
                continue

            lookup_values = self.cmdb.get_lookup_values(lookup)
            description = data[card]
            card_id = [ i['_id'] for i in lookup_values \
                    if description == i['description']]

            if card_id is None:
                continue

            data[card] = card_id[0]

        return data

    def get_attributes(self):
        return self.cmdb.request_real("GET", join(self.url, 'attributes'))

    def get_info(self):
        return self.cmdb.request_real("GET", self.url)

    def create(self, data, convert=True):
        data = json.dumps(self.convert(data) if convert else data)
        return self.cmdb.request_real("POST", join(self.url, 'cards'), 
                data=data)

    def status(self, cid):
        return self.cmdb.request_real("GET", join(self.url, 'cards', cid))

    def delete(self, cid):
        return self.cmdb.request_real("DELETE", join(self.url, 'cards', cid))

    def update(self, cid, data, convert=True):
        data = json.dumps(self.convert(data) if convert else data)
        return self.cmdb.request_real("PUT", join(self.url, 'cards', cid), 
                data=data)

    def list(self):
        return self.cmdb.request_real("GET", join(self.url, 'cards'))

def printj(data):
    print(json.dumps(data, indent=2))

