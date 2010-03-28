# -*- coding: utf-8 -*-

"""
    abouttag.nacolike

    NACO-like normalization.

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

import unicodedata, re

TO_SPACES_RE = re.compile(r'[\!\(\)\{\}\<\>\-\;\:\.\?\,\/\\\@\*\%\=\$\^\_\~]')
DELETIONS_RE = re.compile(r'\[\]\|')
MULTISPACE_RE = re.compile(r'\s+')
TRANSLATE = {
        u'Æ' : u'AE',
        u'æ' : u'ae',
        u'Œ' : u'OE',
        u'œ' : u'oe',
        u'Ð' : u'D',
        u'đ' : u'd',
        u'ð' : u'd',
        u'ı' : u'i',
        u'Ł' : u'l',
        u'ł' : u'l',
        u'ℓ' : u'l',
        u'Ø' : u'o',
        u'ø' : u'o',
        u'Ơ' : u'o',
        u'ơ' : u'o',
        u'Þ' : u'th',
        u'þ' : u'th',
        u'Ư' : u'u',
        u'ư' : u'u',
        u'α' : u'a',
        u'β' : u'b',
        u'γ' : u'y',
        u'♭' : u'b', 
        u'♯' : u'#', # careful: sharp not hash on left!     
        u'–' : u'-', # en-dash
        u'—' : u'-', # em-dash
        u"'" : u'', # apostrophe
}

def remove_accents(u):
    return ''.join(c for c in unicodedata.normalize('NFD', u)
                            if unicodedata.category(c) != 'Mn')

def normalize_part(u):
    u =  ''.join(TRANSLATE[s] if s in TRANSLATE else s for s in u)
    u = remove_accents(u)
    u = re.sub(TO_SPACES_RE, u' ', u)
    u = re.sub(DELETIONS_RE, u'', u)
    u = ''.join(c if 0x1F < ord(c) < 0x7E else u' ' for c in u)
    u = re.sub(MULTISPACE_RE, u' ', u)
    return u

def normalize(u, preserveFirstComma=False):
    """Normalize a string using NACO normalization rules.
       Input is (must be) unicode string.

       Rules taken from NACO Normalization
       http://lcweb.loc.gov/catdir/pcc/naco/normrule.html
       Except that accents are mapped to nearest equivalent ASCII characters
       or character sequences, and "subfield delimiters" are ignored.
    """
    if preserveFirstComma and u',' in u:
        cPos = u.find(u',')
        U = u'%s,%s' % (normalize_part(u[:cPos]), normalize_part(u[:cPos]))
    else:
        U = normalize_part(u)
    return U.lower().strip()

        


