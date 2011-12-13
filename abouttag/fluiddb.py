# -*- coding: utf-8 -*-

"""
    abouttag.fluiddb

    Standard about tags as used by FluidDB itself.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

from abouttag import about


class FluidDB:
    """Usage:
        from abouttag.fluiddb import FluidDB

        db = FluidDB()
        user = db.user(u'njr')
        ns = db.namespace(u'njr/ideas')
        tag = db.tag(u'njr/rating')
    """
    def __init__(self, convention=u'fluiddb-1'):
        assert convention.lower() in (u'fluiddb-1',)
        self.convention = convention.lower()

    def normalize(self, path, normalize=True, convention=u'fluiddb-1'):
        if normalize:
            if path.startswith(u'/'):
                path = path[1:]
            if path.endswith(u'/'):
                path = path[:-1]
            path = path.strip()
        return path

    def user(self, username, normalize=True):
        # There is no normalization to perform on a username
        return u'Object for the user named %s' % username

    def namespace(self, ns, normalize=True):
        return u'Object for the namespace %s' % self.normalize(ns, normalize)

    def tag(self, tag, normalize=True):
        return 'Object for the attribute %s' % self.normalize(tag, normalize)


class TestFluidDB(about.AboutTestCase):
    def testFluidDBBadConvention(self):
        self.assertRaises(AssertionError, FluidDB, u'unknown')

    def testFluidDBUser(self):
        db = FluidDB(u'fluiddb-1')
        self.assertEqual(db.user(u'njr'), u'Object for the user named njr')

    def testFluidDBNormalize(self):
        expected = (
            (u'njr', u'njr'),
            (u'/njr', u'njr'),
            (u'njr/', u'njr'),
            (u'/njr/', u'njr'),
            (u'one/two', u'one/two'),
        )
        db = FluidDB()
        self.normalizeTest(expected, db.normalize)

    def testFluidDBNamespace(self):
        expected = (
            (u'njr', u'Object for the namespace njr'),
            (u'one/two', u'Object for the namespace one/two')
        )
        db = FluidDB()
        self.getExpectedResults(expected, db.namespace)

    def testFluidDBTag(self):
        expected = (
            (u'njr/rating', u'Object for the attribute njr/rating'),
            (u'/njr/sub/rating', u'Object for the attribute njr/sub/rating'),
        )
        db = FluidDB()
        self.getExpectedResults(expected, db.tag)
