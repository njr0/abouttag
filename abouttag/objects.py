# -*- coding: utf-8 -*-

"""
    abouttag.objects

    Objects with very simple conventions, mostly
        "entity:Name"
    with normalization consisting only stripping leading
    and trailing spaces and (perhaps) normalizing it.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""
from abouttag import about

planet = about.simple(u'planet')
element = about.simple(u'element')
twitteruser1 = about.simple(u'twitter.com:uid', 'twitteruser')

def twitteruser(name, normalize=True, convention=u'twitteruser-2'):
    assert convention in (u'twitteruser-1', u'twitteruser-2')
    if convention == u'twitteruser-1':
        return twitteruser1(name, convention, normalize)
    else:
        n = name.lower().strip() if normalize else name
        return n if n.startswith(u'@') else u'@%s' % n


class TestObjects(about.AboutTestCase):
    # Just tests planet, becaues if planet's OK there's really
    # not much to go wrong with other simple about tags.
    def testConvention(self):
        self.assertRaises(AssertionError, planet, u'foo', u'unknown')

    def testPlanet(self):
        self.assertEqual(planet(u'Mars'), u'planet:Mars')
        self.assertEqual(planet(u' saturn '), u'planet:Saturn')

        # No normalization:
        self.assertEqual(planet(u' saturn ', normalize=False),
                         u'planet: saturn ')

    def testElement(self):
        self.assertEqual(element(u'Hydrogen'), u'element:Hydrogen')
        self.assertEqual(element(u' copper '), u'element:Copper')

        # No normalization:
        self.assertEqual(element(u' copper ', normalize=False),
                         u'element: copper ')

    def testTwitterUser(self):
        self.assertEqual(twitteruser(u'17895882', convention='twitteruser-1'),
                         u'twitter.com:uid:17895882')
        self.assertEqual(twitteruser(u' 17895882 ',
                                     convention='twitteruser-1'),
                         u'twitter.com:uid:17895882')

        self.assertEqual(twitteruser(u'terrycojones'), u'@terrycojones')
        self.assertEqual(twitteruser(u' @TERRYCOJONES '), u'@terrycojones')
                         

        # No normalization:
        self.assertEqual(twitteruser(u' @TERRYCOJONES ', False,
                                     'twitteruser-2'),
                         u'@ @TERRYCOJONES ')
