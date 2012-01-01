# -*- coding: utf-8 -*-

"""
    abouttag.abouttag

    Helper test methods for the abouttag module.
    Generic entity function for simple about tags with simple normalization

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unittest


def generalentity(name, convention, conventions, normalize=True,
           prefix=u'', suffix=u'', case='title', doStrip=True):
    assert convention in conventions
    if normalize:
        if case == 'title':
            name = name.title()
        elif case == 'lower':
            name = name.lower()
        elif case == 'upper':
            name = name.upper()
        if doStrip:
            name = name.strip()
    return u'%s%s%s' % (prefix, name, suffix)


def simple(entity, cname=None):
    conventions = ('%s-1' % (cname if cname else entity),)

    def f(name, convention='%s-1' % entity, normalize=True):
        return generalentity(name, convention, conventions,
                             normalize=normalize, prefix=u'%s:' % entity)
    return f


class AboutTestCase(unittest.TestCase):
    def getExpectedResults(self, expected, f):
        for (input, output) in expected:
            self.assertEqual((input, f(input)), (input, output))
        self.assertEqual(f(u'/%s' % expected[0][0]) == output, False)

    def normalizeTest(self, expected, f, convention=None):
        if convention:
            for (input, normalized) in expected:
                self.assertEqual((input, f(input, convention=convention)),
                                 (input, normalized))
                self.assertEqual((input, f(input, True,
                                           convention=convention)),
                                 (input, normalized))
                self.assertEqual((input, f(input, False,
                                           convention=convention)),
                                 (input, input))
        else:
            for (input, normalized) in expected:
                self.assertEqual((input, f(input)), (input, normalized))
                self.assertEqual((input, f(input, True)), (input, normalized))
                self.assertEqual((input, f(input, False)), (input, input))

    def vectorTest(self, expected, f):
        for (args, normalized) in expected:
            self.assertEqual((args, f(*args)), (args, normalized))
