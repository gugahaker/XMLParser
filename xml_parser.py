#!/usr/bin/env python3

import sys
from lxml import etree
from html2text import html2text

if len(sys.argv) == 2:
    XML_FILE = sys.argv[1]
else:
    sys.exit("Usage: {0} <xml_file>".format(sys.argv[0]))

parsed = {}

class Revision:
    def __init__(self):
        self._id = -1
        self._timestamp = 0
        self._contributor = {"username":"", "id":-1}
        self._comment = ""
        self._model = ""
        self._format = ""
        self._text = ""
        self._sha1 = ""

    def set_id(self, ID):
        if type(ID) is int:
            self._id = ID
        else:
            raise ValueError("ID must be an integer.")
    def get_id(self):
        return self._id

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp
    def get_timestamp(self):
        return self._timestamp

    def set_contributor(self, username, ID):
        if type(username) is str:
            self._contributor["username"] = username
        else:
            raise ValueError("username must be a string.")
        if type(ID) is int:
            self._contributor["id"] = ID
        else:
            raise ValueError("ID must be an integer")
    def get_contributor(self):
        return self._contributor

    def set_comment(self, comment):
        self._comment = comment
    def get_comment(self):
        return self._comment

    def set_model(self, model):
        self._model = model
    def get_model(self):
        return self._model

    def set_format(self, f):
        self._format = f
    def get_format(self, f):
        return self._format

    def set_text(self, text):
        text = html2text(text) 
        self._text = text
    def get_text(self):
        return self._text
    
    def set_sha1(self, sha1):
        self._sha1 = sha1
    def get_sha1(self, sha1):
        return self._sha1

class Page:
    def __init__(self):
        self._title = ''
        self._ns = ''
        self._id = -1
        self._revision = Revision()
    
    def set_title(self, title):
        self._title = title
    def get_title(self):
        return self._title

    def set_ns(self, ns):
        self._ns = ns
    def get_ns(self):
        return self._ns

    def set_id(self, ID):
        if type(ID) is int:
            self._id = ID
        else:
            raise ValueError("ID must be an integer")
    def get_id(self):
        return self._id

    def set_revision(self, revision):
        if type(revision) is Revision:
            self._revision = revision
        else:
            raise ValueError("revision must be an instance of Revision class")
    def get_revision(self):
        return self._revision


def get_tag_name(tag):
    i = tag.rfind("}")
    if i != -1:
        return tag[i+1:]
    else:
        return None

inpage = False
inrevision = False
incontributor = False

p = Page()
r = Revision()

for event, elem in etree.iterparse(XML_FILE, events=['start', 'end']):
    if event == 'start':
        if get_tag_name(elem.tag) == "page":
            p = Page()
            inpage = True
        if get_tag_name(elem.tag) == "revision":
            inrevision = True
        if get_tag_name(elem.tag) == "contributor":
            username = ''
            uid = -1
            incontributor = True

    if event == 'end':
        if inpage and not inrevision:    
            if get_tag_name(elem.tag) == "title":
                p.set_title(elem.text)
            if get_tag_name(elem.tag) == "ns":
                p.set_ns(elem.text)
            if get_tag_name(elem.tag) == "id":
                p.set_id(int(elem.text))
            if get_tag_name(elem.tag) == "page":
                parsed[get_tag_name(elem.tag)] = p
                inpage = False
                print(p.get_revision().get_text())
        
        if inrevision:
            r = p.get_revision()
            if get_tag_name(elem.tag) == "id" and not incontributor:
                r.set_id(int(elem.text))
            if get_tag_name(elem.tag) == "timestamp":
                r.set_timestamp(elem.text)
            if get_tag_name(elem.tag) == "username":
                username = elem.text
            if get_tag_name(elem.tag) == "id" and incontributor:
                uid = int(elem.text)
            if get_tag_name(elem.tag) == "contributor":
                r.set_contributor(username, uid)
                incontributor = False
            if get_tag_name(elem.tag) == "comment":
                r.set_comment(elem.text)
            if get_tag_name(elem.tag) == "model":
                r.set_model(elem.text)
            if get_tag_name(elem.tag) == "format":
                r.set_format(elem.text)
            if get_tag_name(elem.tag) == "text":
                r.set_text(elem.text)
            if get_tag_name(elem.tag) == "sha1":
                r.set_sha1(elem.text)
            if get_tag_name(elem.tag) == "revision":
                p.set_revision(r)
                inrevision = False
