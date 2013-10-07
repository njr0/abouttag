# -*- coding: utf-8 -*-

"""
    abouttag.books

    Standard about tags for books and authors.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unittest
import re
from abouttag import about
from abouttag.nacolike import normalize

DOT_LETTER_RE = re.compile(u'^.*\.[A-Z].*$')
LC_ARTICLES = (u'the', u'a')

def replacedots(author):
    return author.replace(u'.', u' ')


def book_author_about(author, move_surname=True):
    if move_surname:
        return replacedots(move_surname_to_end(author))
    else:
        return replacedots(author)


def normalize_work(prefix, preserveAlpha=False, move_surname=True):
    def f(title, *authors, **kwargs):
        doNormalize = kwargs['normalize'] if 'normalize' in kwargs else True
        if doNormalize:
            authors = u'; '.join(normalize(book_author_about(a, move_surname),
                                           preserveAlpha=preserveAlpha)
                                  for a in authors if a)
            return u'%s:%s (%s)' % (prefix,
                                    normalize(move_article(title),
                                              preserveAlpha=preserveAlpha),
                                    authors)
        else:
            authors = u'; '.join(a for a in authors if a)
            return u'%s:%s (%s)' % (prefix, title, authors)
    return f


normalize_book = normalize_work(u'book')
normalize_ubook = normalize_work(u'book', preserveAlpha=True)


def book(title, *authors, **kwargs):
    """This uses the book-u convention which is the same as book-1
except that accents are preserved.

Usage:
        from abouttag.books import ubook

        print book(u"Gödel, Escher, Bach: An Eternal Golden Braid",
                   u'Douglas R. Hofstader')
        book:gödel escher bach an eternal golden braid (douglas r hofstader)


        print book(u'The Feynman Lectures on Physics',
                   u'Richard P. Feynman', u'Robert B. Leighton',
                   u'Matthew Sands')
        book:the feynman lectures on physics (richard p feynman; robert b leighton; matthew sands)


        print book(u'The Oxford English Dictionary: second edition, volume 3',
                   u'John Simpson', u'Edmund Weiner')

        book:the oxford english dictionary second edition volume 3 (john simpson; edmund weiner)
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'book-u'

    return normalize_ubook(title, *authors, **kwargs)


ubook = book


def abook(title, *authors, **kwargs):
    """Usage:
        from abouttag.books import abook

        print abook(u"Gödel, Escher, Bach: An Eternal Golden Braid",
                   u'Douglas R. Hofstader')
        book:godel escher bach an eternal golden braid (douglas r hofstader)


        print abook(u'The Feynman Lectures on Physics',
                    u'Richard P. Feynman', u'Robert B. Leighton',
                    u'Matthew Sands')
        book:the feynman lectures on physics (richard p feynman; robert b leighton; matthew sands)


        print abook(u'The Oxford English Dictionary: second edition, volume 3',
                    u'John Simpson', u'Edmund Weiner')

        book:the oxford english dictionary second edition volume 3 (john simpson; edmund weiner)
    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'book-1'

    return normalize_book(title, *authors, **kwargs)


def is_all_upper(s):
    """Returns True if the whole of the string s is upper case."""
    return sum(c.isupper() for c in s) == len(s)


def dot_initial(s):
    if len(s) == 1 and s.isupper():
        return u'%s.' % s
    else:
        return s


def move_article(title):
    """Moves trailing article after comma to the start of a title.
       So

          Catcher in the Rye, The --> The Catcher in the Rye
          Catcher in the Rye,The  --> The Catcher in the Rye
          The Catcher in the Rye  --> The Catcher in the Rye
          Catcher in the Rye      --> Catcher in the Rye
          A Stitch in Time        --> A Stitch in Time
          Stitch in Time, A       --> A Stitch in Time
          Stitch in Time,A        --> A Stitch in Time
          Stitch in Time          --> Stitch in Time

       Currently only handles 'a' and 'the', but it just uses
       a word list, so it would be easy to add le/la etc.

       Case is unaffected.
        
    """
    L = title.lower()
    if not title:
        return u''
    for a in LC_ARTICLES:
        if L.endswith(u', ' + a):
            return u'%s %s' % (title[-len(a):], title[:-(len(a) + 2)])
        elif L.endswith(u',' + a):
            return u'%s %s' % (title[-len(a):], title[:-(len(a) + 1)])
    return title


def move_surname_to_end(author):
    """Given a name such as "Salinger, J.D.", this functions transforms
       the name into J. D. Salinger.

       Specifically, it takes anything after the comma (if present)
       and moves it to the front, adds full stops after single initials,
       and splits initials.   So all of

        J. D. Salinger
        J.D.Salinger
        J.D. Salinger
        JD Salinger
        Salinger,J.D.
        Salinger, J.D.
        Salinger, J. D.
        Salinger, JD

        will be turned into u'J. D. Salinger'.
        
    """
    if not author:
        return u''

    parts = [s.strip() for s in author.split(u',')]
    if len(parts) >= 2:
        parts = parts[1:] + [parts[0]]
        author = u' '.join(parts)

    parts = [s.strip() for s in author.split(u' ')]
    if len(parts) < 1 or is_all_upper(parts[-1]):
        return author           # Surname thing seems to be upper case;
                                # don't try to split initials.

    if len(parts[0]) == 1:       # First part is undotted initial
        return u' '.join([dot_initial(p) for p in parts[:-1]] + [parts[-1]])
    elif is_all_upper(parts[0]):    # First part looks like string of undotted
                                    # initials
        return u' '.join([u'%s.' % p for p in parts[0]] + parts[1:])
    elif re.match(DOT_LETTER_RE, parts[0]):
        parts[0] =  u'. '.join(s.strip() for s in parts[0].split(u'.')).strip()
        return u' '.join(parts)
    else:
        return author


def normalize_author(author, year, month, day, **kwargs):
    doNormalize = kwargs['normalize'] if 'normalize' in kwargs else True
    if year:
        if month:
            if day:
                date = u' (%04d-%02d-%02d)' % (year, month, day)
            else:
                date = u' (%04d-%02d)' % (year, month)
        else:
            date = u' (%04d)' % (year)
    else:
        date = u''
    if doNormalize:
        author = normalize(replacedots(author))
    return u'author:%s%s' % (author, date)


def author(name, year=None, month=None, day=None, **kwargs):
    """Usage:
        from abouttag.books import author

        print author(u'Douglas R. Hofstader', 1945, 2, 15)
        author:douglas r hofstader (1945-02-15)

        print author(u'Douglas R. Hofstader')
        author:douglas r hofstader

    """
    if 'convention' in kwargs:
        assert kwargs['convention'].lower() == u'author-1'

    return normalize_author(name, year, month, day, **kwargs)


class TestBooks(about.AboutTestCase):
    def testFluidDBBadConvention(self):
        self.assertRaises(AssertionError, book, u'hello', convention='unknown')

    def testFluidDBNormalize(self):
        expected = (
            ((u"Gödel, Escher, Bach: An Eternal Golden Braid",
              u'Douglas R. Hofstadter'),
             u'book:godel escher bach an eternal golden braid '
                 u'(douglas r hofstadter)'),

             ((u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'Robert B. Leighton',
               u'Matthew Sands'),
              u'book:the feynman lectures on physics '
                  u'(richard p feynman; robert b leighton; matthew sands)'),

             ((u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'', u'Robert B. Leighton', None,
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
            self.assertEqual((input, output),
                             (input, abook(title, *author)))
        self.assertEqual(abook(u'Kes', u'Ken Kesey', convention=u'book-1'),
                         u'book:kes (ken kesey)')
        self.assertEqual(abook(u'Kes', u'Ken Kesey', convention=u'book-1',
                               normalize=False),
                         u'book:Kes (Ken Kesey)')
        self.assertEqual(book(u'Kes', u'Ken Kesey', convention=u'book-u'),
                         u'book:kes (ken kesey)')
        self.assertRaises(AssertionError, book ,u'Kes', u'Ken Kesey',
                                   convention=u'book-1')

    def testFluidDBNormalizeU(self):
        expected = (
            ((u"Gödel, Escher, Bach: An Eternal Golden Braid",
              u'Douglas R. Hofstader'),
             u'book:gödel escher bach an eternal golden braid '
                 u'(douglas r hofstader)'),

             ((u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'Robert B. Leighton',
               u'Matthew Sands'),
              u'book:the feynman lectures on physics '
                  u'(richard p feynman; robert b leighton; matthew sands)'),

             ((u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'', u'Robert B. Leighton', None,
               u'Matthew Sands'),
              u'book:the feynman lectures on physics '
                  u'(richard p feynman; robert b leighton; matthew sands)'),

             ((u'The Oxford English Dictionary: second edition, volume 3',
               u'John Simpson', u'Edmund Weiner'),
              u'book:the oxford english dictionary second edition volume 3 '
                  '(john simpson; edmund weiner)'),

            ((u'The One Hundred Years of Solitude',
              u'Gabriel García Márquez'),
             u'book:the one hundred years of solitude '
             u'(gabriel garcía márquez)'),

            ((u"L'Histoire de Gil Blas de Santillane",
              u'Alain-René Lesage'), 
             u'book:lhistoire de gil blas de santillane (alain rené lesage)'),

           ((u'Cønsümàte Craziness',
             u'Imprøbable', u'CrÆzy', u'Øutlandisch'),
            u'book:cønsümàte craziness (imprøbable; cræzy; øutlandisch)'),
        )
        for (input, output) in expected:
            title, author = input[0], input[1:]
            self.assertEqual((input, output),
                             (input, book(title, *author)))
            self.assertEqual((input, output),
                             (input, ubook(title, *author)))

    def testNormalizeAuthor(self):
        expected = (
            ((u"Douglas R. Hofstadter", 1945, 2, 15),
             u'author:douglas r hofstadter (1945-02-15)'),
            ((u"Douglas R. Hofstadter", 1945, 2, None),
             u'author:douglas r hofstadter (1945-02)'),
            ((u"Douglas R. Hofstadter", 1945, None, None),
             u'author:douglas r hofstadter (1945)'),
            ((u"Douglas R. Hofstadter", None, None, None),
             u'author:douglas r hofstadter'),
            ((u'Gabriel García Márquez', 1927, 3, 6),
             u'author:gabriel garcia marquez (1927-03-06)'),
        )
        for (input, output) in expected:
            [name, y, m, d] = input
            self.assertEqual((input, output),
                             (input, author(name, y, m, d)))
        self.assertEqual(author('D. R. H.', 1, 2, 3, normalize=False,
                                convention=u'author-1'),
                         'author:D. R. H. (0001-02-03)')


    def testMoveSurname1(self):
        inputs = [
            u'J. D. Salinger',
            u'J.D.Salinger',
            u'J D Salinger',
            u'J.D. Salinger',
            u'JD Salinger',
            u'Salinger,J.D.',
            u'Salinger, J.D.',
            u'Salinger, J. D.',
            u'Salinger, JD',
        ]
        for input in inputs:
            self.assertEqual((input, move_surname_to_end(input)),
                             (input, u'J. D. Salinger'))


    def testMoveSurname2(self):
        inputs = [
            u'Anne Michaels',
            u'Michaels, Anne',
            u'Michaels,Anne',
        ]
        for input in inputs:
            self.assertEqual((input, move_surname_to_end(input)),
                             (input, u'Anne Michaels'))


    def testMoveSurname3(self):
        inputs = [
            u'Lynne Reid Banks',
            u'Banks, Lynne Reid',
            u'Banks,Lynne Reid',
            u'Reid Banks, Lynne',
            u'Reid Banks,Lynne',
        ]
        for input in inputs:
            self.assertEqual((input, move_surname_to_end(input)),
                             (input, u'Lynne Reid Banks'))

    def testMoveArticles(self):
        IO = ((u'Catcher in the Rye, The', u'The Catcher in the Rye'),
              (u'Catcher in the Rye,The', u'The Catcher in the Rye'),
              (u'The Catcher in the Rye', u'The Catcher in the Rye'),
              (u'Catcher in the Rye', u'Catcher in the Rye'),
              (u'A Stitch in Time', u'A Stitch in Time'),
              (u'Stitch in Time, A', u'A Stitch in Time'),
              (u'Stitch in Time,A', u'A Stitch in Time'),
              (u'Stitch in Time', u'Stitch in Time'))
        for (input, output) in IO:
            self.assertEqual((input, move_article(input)),
                             (input, output))


if __name__ == '__main__':
    unittest.main()
