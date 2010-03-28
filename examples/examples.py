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
from abouttag.books import book



db = FluidDB()
print '\nFluidDB OBJECTS:'
print db.user(u'njr')
print db.namespace(u'njr/misc')
print db.tag(u'terrycojones/private/rating')

print '\nURIs:'
print URI(u'FluidDB.fluidinfo.com')
print URI(u'FluidDB.fluidinfo.com/one/two/')
print URI(u'https://FluidDB.fluidinfo.com/one/two/')
print URI(u'http://fluiddb.fluidinfo.com/one/two/')
print URI(u'http://test.com/one/two/?referrer=http://a.b/c')

db = Database()
print '\nDATABASE ITEMS:'
print db.table(u'elements')
print db.field(u'Name', u'elements')

print '\nPLANETS, ELEMENTS:'
print planet(u'Mars')
print element(u'Helium')

print'\nLOCATIONS:'
print GEOnet(-2601490, -3577649)

print '\nBOOKS:'
print book(u"Gödel, Escher, Bach: An Eternal Golden Braid",
                   u'Douglas R. Hofstader')


print book(u'The Feynman Lectures on Physics',
           u'Richard P. Feynman', u'Robert B. Leighton', 
           u'Matthew Sands')

print book(u'The Oxford English Dictionary: second edition, volume 3',
           u'John Simpson', u'Edmund Weiner')
