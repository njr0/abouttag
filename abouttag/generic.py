# -*- coding: utf-8 -*-

"""
    abouttag.generic

    Provides generic abouttag function; object type specified by first
    parameter.

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

class AboutTagError(Exception):
    pass


def abouttag(*args):

    items = {
        'fi-user': FluidDB.user,
        'fi-namespace': FluidDB.namespace,
        'fi-ns': FluidDB.namespace,
        'fi-tag': FluidDB.tag,
        'uri': URI,
        'url': URI,
        'URI': URI,
        'URL': URI,
        'db-table': Database.table,
        'db-field': Database.field,
        'planet': planet,
        'element': element,
        'book': ubook,
        'author': author,
        'album': album,
        'track': track,
        'artist': artist,
        'isrc-recording': isrc_recording,
        'twitter-user': twitteruser,
    }
             
    if len(args) == 0:
        raise AboutTagError('No object type specified')
    object = args[0]
    if not object in items:
        raise AboutTagError('Object type %s not known.\n'
                            '  Supported object types are:\n    %s\n'
                            % (object, '\n    '.join(items.keys())))

    f = items[object]
    if object.startswith('fi'):
        db = FluidDB()
        return f(db, *args[1:])
    elif object.startswith('db'):
        db = Database()
        return f(db, *args[1:])
    elif object == 'author':
        if len(args) > 2:
            return f(args[1], *(int(a) for a in args[2:]))
        else:
            raise AboutTagError('No author specified')
    else:
        return f(*args[1:])



