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
import unittest
from abouttag import about

planet = about.simple(u'planet')
element = about.simple(u'element')

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

