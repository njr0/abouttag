# -*- coding: utf-8 -*-

"""
    abouttag.books

    Standard about tags for books

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unittest
from abouttag import about
from abouttag.nacolike import normalize

def replacedots(author):
    return author.replace('.', ' ')
        
def normalize_book(title, *authors, **kwargs):
    doNormalize = kwargs['normalize'] if 'normalize' in kwargs else True
    if doNormalize:
        authors = u'; '.join (normalize (replacedots(a)) for a in authors)
        return u'book:%s (%s)' % (normalize (title), authors)
    else:
        authors = u'; '.join (a for a in authors)
        return u'book:%s (%s)' % (title, authors)

def book(title, *authors, **kwargs):
    """Usage:
        from abouttag.books import book

	print book(u"Gödel, Escher, Bach: An Eternal Golden Braid",
                   u'Douglas R. Hofstader')
	book:godel escher bach an eternal golden braid (douglas r hofstader)


	print book(u'The Feynman Lectures on Physics',
                   u'Richard P. Feynman', u'Robert B. Leighton', 
                   u'Matthew Sands')
        book:the feynman lectures on physics (richard p feynman; robert b leighton; matthew sands)


	print book(u'The Oxford English Dictionary: second edition, volume 3',
                   u'John Simpson', u'Edmund Weiner')

	book:the oxford english dictionary second edition volume 3 (john simpson; edmund weiner)
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'book-1'

    return normalize_book(title, *authors, **kwargs)

class TestBooks(about.AboutTestCase):
    def testFluidDBBadConvention(self):
        self.assertRaises(AssertionError, book, u'hello', convention='unknown')

    def testFluidDBNormalize(self):
        expected = (
            ((u"Gödel, Escher, Bach: An Eternal Golden Braid",
              u'Douglas R. Hofstader'),
             u'book:godel escher bach an eternal golden braid '
                 u'(douglas r hofstader)'),

	     ((u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'Robert B. Leighton', 
               u'Matthew Sands'),
	      u'book:the feynman lectures on physics '
                  u'(richard p feynman; robert b leighton; matthew sands)'),

             ((u'The Oxford English Dictionary: second edition, volume 3',
               u'John Simpson', u'Edmund Weiner'),
              u'book:the oxford english dictionary second edition volume 3 '
                  '(john simpson; edmund weiner)'),
        )
        for (input, output) in expected:
            title, author = input[0], input[1:]
            self.assertEqual ((input, output),
                              (input, book(title, *author)))



if __name__ == '__main__':
    unittest.main()

