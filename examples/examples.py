# -*- coding: utf-8 -*-

"""
    abouttag.examples

    abouttag: Example usage.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

from abouttag.fluiddb import FluidDB
from abouttag.uri import URI
from abouttag.database import Database
from abouttag.objects import planet, element
from abouttag.location import GEOnet



db = FluidDB()
print db.user(u'njr')
print db.namespace(u'njr/misc')
print db.tag(u'terrycojones/private/rating')


print URI(u'FluidDB.fluidinfo.com')
print URI(u'FluidDB.fluidinfo.com/one/two/')
print URI(u'https://FluidDB.fluidinfo.com/one/two/')
print URI(u'http://fluiddb.fluidinfo.com/one/two/')
print URI(u'http://test.com/one/two/?referrer=http://a.b/c')

db = Database()
print db.table(u'elements')
print db.field(u'Name', u'elements')

print planet(u'Mars')

print element(u'Helium')

print GEOnet(-2601490, -3577649)


