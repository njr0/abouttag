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
from abouttag.objects import planet, element, twitteruser
from abouttag.location import GEOnet
from abouttag.books import book, ubook, author
from abouttag.music import album, track, artist, isrc_recording
from abouttag.film import film, movie


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

print '\nBOOKS (book-1 and book-u conventions):\n'

print book(u"Gödel, Escher, Bach: An Eternal Golden Braid",
           u'Douglas R. Hofstader')
print
print book(u"One Hundred Years of Solitude", u'Gabriel García Márquez')
print book(u'The Feynman Lectures on Physics',
           u'Richard P. Feynman', u'Robert B. Leighton',
           u'Matthew Sands')
print
print book(u'The Oxford English Dictionary: second edition, volume 3',
           u'John Simpson', u'Edmund Weiner')
print

print '\nAUTHORS:'

print author(u'Gabriel García Márquez', 1927, 3, 6)
print author(u"Douglas R. Hofstadter", 1945, 2, 15)

print '\nMUSIC (album-u, track-u, artist-u and isrc-1 conventions):\n'
print track(u'Bamboulé', u'Bensusan and Malherbe')
print album(u"Solilaï", u'Pierre Bensusan')
print artist(u"Crosby, Stills, Nash & Young")
print isrc_recording(u'US-PR3-73-00012')

print '\nFILM (film-u convention):\n'
print film(u"Citizen Kane", u'1941')
print movie(u"L'Âge d'Or", u'1930')
print

print '\nTWITTER users:\n'
print twitteruser(u"terrycojones")

print
