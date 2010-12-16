# -*- coding: utf-8 -*-

"""
    abouttag.database

    Standard about tags for database tables / datasets

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

from abouttag import about


class Database:
    """Usage:
        from abouttag.database import Database

        db = Database()
        table = db.table(u'elements')
        field = db.field(u'Name', u'elements')
    """
    def __init__(self, convention=u'database-1'):
        assert convention.lower() in (u'database-1',)
        self.convention = convention.lower()

    def normalize(self, word, normalize=True):
        return word.strip()

    def table(self, tablename, normalize=True):
        return u'table:%s' % self.normalize(tablename)

    def field(self, fieldname, tablename, normalize=True):
        return u'field:%s in table:%s' % (self.normalize(fieldname),
                                          self.normalize(tablename))


class TestDatabase(about.AboutTestCase):
    def testDatabseBadConvention(self):
        self.assertRaises(AssertionError, Database, u'unknown')

    def testTable(self):
        db = Database()
        self.assertEqual(db.table(u'elements'), u'table:elements')

    def testFluidDBNamespace(self):
        db = Database()
        self.assertEqual(db.field(u'Name', u'elements'),
                         u'field:Name in table:elements')
