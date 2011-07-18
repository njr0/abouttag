# -*- coding: utf-8 -*-

"""
    abouttag.film

    Standard about tags for films (movies)

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unittest
from abouttag import about
from abouttag.nacolike import normalize
from abouttag.books import normalize_work

normalize_film = normalize_work(u'film', preserveAlpha=True,
                                move_surname=False)


def film(title, year, **kwargs):
    """Usage:
        from abouttag.film import film

        print film(u"Citizen Kane", u'1941')
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'track-u'
    if type(year) == int:
        year = str(year)
    assert len(year) == 4
    assert all('0' <= y <= '9' for y in year)

    return normalize_film(title, year, **kwargs)

movie = film


class TestFilm(about.AboutTestCase):
    def testFluidDBNormalizeFilm(self):
        expected = (
            ((u"Citizen Kane", u'1941'), u'film:citizen kane (1941)'),
            ((u"The Last Seduction", 1994), u'film:the last seduction (1994)'),
            ((u"Él", 1953), u'film:él (1953)'),
            ((u"L'Âge d'Or", u'1930'), u'film:lâge dor (1930)'),
        )
        bads = ((u"Citizen Kane", u''),
                (u"Citizen Kane", u'1941-42'),
                (u"Citizen Kane", u'41')
        )
        for (input, output) in expected:
            title, year = input[0], input[1]
            self.assertEqual((input, output), (input, film(title, year)))
            self.assertEqual((input, output), (input, movie(title, year)))
        for input in bads:
            title, year = input[0], input[1]
            self.assertRaises(AssertionError, film, title, year)


                             

if __name__ == '__main__':
    unittest.main()
