# -*- coding: utf-8 -*-

"""
    abouttag.location

    Standard about tags for URIs and URLs

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

from abouttag import about


def GEOnet(fli, fni, normalize=False, convention=u'geonet-1'):
    """Usage:
        from abouttag.uri import GEOnet

        normalURL = URI(-2601490, -3577649)
    """
    assert convention.lower() == u'geonet-1'
    return u'GEOnet%d_%d' % (fli, fni)


class TestGEOnet(about.AboutTestCase):
    def testFluidDBBadConvention(self):
        self.assertRaises(AssertionError, GEOnet, 1, 2, convention='unknown')

    def testFluidDBNormalize(self):
        expected = (
            ((1, 2), u'GEOnet1_2'),
            ((-99999, -77777), u'GEOnet-99999_-77777')
        )
        self.vectorTest(expected, GEOnet)
