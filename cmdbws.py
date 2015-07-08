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

version_info = (0, 6, 1)
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
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

        assert self.url, u'URL为空,请指定正确的URL.'
        
        # Authentication to cmdbuild
        login = self._login()
        self.token = login["data"]["_id"] 
        self.role = login["data"]["role"]
        self.availableRoles = login["data"]["availableRoles"]

    def get_class(self, class_name):
        return CmdbClass(self, class_name)

    def _login(self, **kwargs):
        try:
            url = "%s/sessions/" % self.url

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
        if result:
            return result["data"]
        return result

    def list_class(self):
        """列出所有的class"""
        return self.request_real("GET", join(self.url, 'classes'))

    def get_lookup_types(self):
        return self.request_real("GET", join(self.url, 'lookup_types'))

    def get_lookup_values(self, lookup_name):
        return self.request_real("GET", join(self.url, 'lookup_types', 
            lookup_name, 'values'))

    def get_reference_values(self, class_name):
        cls = self.get_class(class_name)
        return cls.list()


class CmdbClass(object):
    def __init__(self, cmdb, class_name):
        self.cmdb = cmdb
        self.class_name = class_name
        self.url = "%s/classes/%s" % (self.cmdb.url, self.class_name)

        self.info = self.get_info()
        self.attributes = self.get_attributes()

        self.lookups = self.get_lookups()
        self.references = self.get_references()

    def get_lookups(self):
        lookups = [ (o["lookupType"], o["description"]) \
                for o in self.attributes if o["type"] == "lookup" ]
        values = {}
        for lookup, key in lookups:
            values[key] = self.cmdb.get_lookup_values(lookup)
        return values

    def get_references(self):
        references = [ (o["targetClass"], o["description"]) \
                for o in self.attributes if o["type"] == "reference" ]
        values = {}
        for reference, key in references:
            values[key] = self.cmdb.get_reference_values(reference)
        return values

    def convert_value(self, key, value):
        attribute = [ a for a in self.attributes if a["description"] == key ][0]
        if 'lookup' == attribute["type"]:
            value = [ o["_id"] for o in self.lookups[key]\
                    if o["description"] == value ][0]
        elif 'reference' == attribute["type"]:
            value = [ o["_id"] for o in self.references[key]\
                    if o["Description"] == value ][0]

        return value

    def convert(self, data):
        ob = {}
        for key, value in data.items():
            ob[key] = self.convert_value(key, value)
        return ob 

    def get_attributes(self):
        return self.cmdb.request_real("GET", join(self.url, 'attributes'))

    def get_info(self):
        return self.cmdb.request_real("GET", self.url)

    def create(self, data, convert=True):
        data = json.dumps(self.convert(data) if convert else data)
        return self.cmdb.request_real("POST", join(self.url, 'cards'), 
                data=data)

    def status(self, cid):
        return self.cmdb.request_real("GET", join(self.url, 'cards', str(cid)))

    def delete(self, cid):
        return self.cmdb.request_real("DELETE", join(self.url, 'cards', str(cid)))

    def update(self, cid, data, convert=True):
        data = json.dumps(self.convert(data) if convert else data)
        return self.cmdb.request_real("PUT", join(self.url, 'cards', str(cid)), 
                data=data)

    def list(self):
        return self.cmdb.request_real("GET", join(self.url, 'cards'))

def printj(data):
    print(json.dumps(data, indent=2))

