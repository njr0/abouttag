# -*- coding: utf-8 -*-

"""
    abouttag.music

    Standard about tags for tracks, albums and artists.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unittest
from abouttag import about
from abouttag.nacolike import normalize
from abouttag.books import normalize_work

normalize_track = normalize_work(u'track', preserveAlpha=True,
                                           move_surname=False)
normalize_album = normalize_work(u'album', preserveAlpha=True,
                                           move_surname=False)


def track(title, artist, **kwargs):
    """Usage:
        from abouttag.music import track

        print track(u"Solilaï", u'Pierre Bensusan')

        print track(u'Bamboulé', u'Bensusan and Malherbe')

        print track(u'''Archie Campbell/Marjorie Campbell/Miss Lyall's '''
                    u'''Strathspey/Miss Lyall's Reel/The St Kilda Wedding''',
                    u'The Cast')

        track:solilaï (pierre bensusan)
        track:bamboulé (bensusan and malherbe)
        track:archie campbell marjorie campbell miss lyalls strathspey miss lyalls reel the st kilda wedding (the cast)
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'track-u'

    return normalize_track(title, artist, **kwargs)


def album(title, artist, **kwargs):
    """Usage:
        from abouttag.music import album

        print album(u"Solilaï", u'Pierre Bensusan')
        album:solilaï (pierre bensusan)


        print album(u'Bamboulé', u'Bensusan and Malherbe')
        album:bamboulé (bensusan and malherbe)

        print album(u'''Archie Campbell/Marjorie Campbell/Miss Lyall's '''
                    u'''Strathspey/Miss Lyall's Reel/The St Kilda Wedding',
                    u'The Cast')

        album:archie campbell marjorie campbell miss lyalls strathspey miss lyalls reel the st kilda wedding (the cast)
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'album-u'

    return normalize_album(title, artist, **kwargs)


def isrc_recording(isrc, **kwargs):
    """Usage:
        from aboutag.music import isrc_recording

        print isrc_recording(u'US-PR3-73-00012')
        isrc:US-PR3-73-00012

    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'isrc-1'

    isrc_stripped = isrc.replace(u'-', u'').upper()
    assert len(isrc_stripped) == 12
    return u'isrc:%s' % isrc_stripped


def artist(name, **kwargs):
    """Usage:
        from aboutag.music import artist

        print artist((u"John Renbourn")
        artist:john renbourn

        print artist(u"Crosby, Stills, Nash & Young")
        artist:crosby stills nash & young'

        print artist(u"Motörhead")
        artist:motörhead'
    """

    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'artist-u'

    return 'artist:%s' % normalize(name, preserveAlpha=True)


class TestMusic(about.AboutTestCase):
    def testFluidDBNormalizeTrack(self):
        expected = (
            ((u"Solilaï", u'Pierre Bensusan'),
              u'track:solilaï (pierre bensusan)'),
            ((u"Down by the River", u'Crosby, Stills, Nash  &  Young'),
              u'track:down by the river (crosby stills nash & young)'),
            ((u'Bamboulé', u'Bensusan and Malherbe'),
             u'''track:bamboulé (bensusan and malherbe)'''),
            ((u'''Archie Campbell/Marjorie Campbell/Miss Lyall's '''
               '''Strathspey/Miss Lyall's Reel/The St Kilda Wedding''',
               u'The Cast'),
             u'''track:archie campbell marjorie campbell miss lyalls str'''
              '''athspey miss lyalls reel the st kilda wedding (the cast)''')
        )
        for (input, output) in expected:
            title, artists = input[0], input[1:]
            self.assertEqual((input, output),
                             (input, track(title, *artists)))

    def testFluidDBNormalizeAlbum(self):
        expected = (
            ((u"Solilaï", u'Pierre Bensusan'),
              u'album:solilaï (pierre bensusan)'),
            ((u"Déjà Vu", u'Crosby, Stills, Nash & Young'),
              u'album:déjà vu (crosby stills nash & young)'),
            ((u"Down by the River", u'Crosby, Stills, Nash  &  Young'),
              u'album:down by the river (crosby stills nash & young)'),
            ((u'Bamboulé', u'Bensusan and Malherbe'),
             u'''album:bamboulé (bensusan and malherbe)'''),
            ((u'''Archie Campbell/Marjorie Campbell/Miss Lyall's '''
               '''Strathspey/Miss Lyall's Reel/The St Kilda Wedding''',
               u'The Cast'),
             u'''album:archie campbell marjorie campbell miss lyalls str'''
              '''athspey miss lyalls reel the st kilda wedding (the cast)''')
        )
        for (input, output) in expected:
            title, artists = input[0], input[1:]
            self.assertEqual((input, output),
                             (input, album(title, *artists)))

    def testFluidDBNormalizeISRC(self):
        expected = (
            (u"US-PR3-73-00012", u'isrc:USPR37300012'),
            (u"USPR37300012", u'isrc:USPR37300012'),
            (u"us-pr3-73-00012", u'isrc:USPR37300012'),
            (u"uspr37300012", u'isrc:USPR37300012')
        )
        for (input, output) in expected:
            self.assertEqual((input, output),
                             (input, isrc_recording(input)))

    def testFluidDBNormalizeArtist(self):
        expected = (
            (u"John Renbourn", u'artist:john renbourn'),
            (u"The  Pentangle", u'artist:the pentangle'),
            (u"Pentangle, The", u'artist:pentangle the'),
            (u"Crosby, Stills, Nash & Young",
             u'artist:crosby stills nash & young'),
            (u"Crosby, Stills, Nash and Young",
             u'artist:crosby stills nash and young'),
            (u"Motörhead", u'artist:motörhead'),
        )
        for (input, output) in expected:
            self.assertEqual((input, output),
                             (input, artist(input)))


if __name__ == '__main__':
    unittest.main()
