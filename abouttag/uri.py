# -*- coding: utf-8 -*-

"""
    abouttag.uri

    Standard about tags for URIs and URLs

    Copyright 2010 AUTHORS (see AUTHORS file)
    License: MIT, see LICENSE for more information
"""

from abouttag import about
import urlnorm


def normalize_uri_1(uri, normalize=True):
    if normalize:
        if not u'://' in uri:
            uri = u'http://%s' % uri
        if uri.endswith(u'/'):
            uri = uri[:-1]
        parts = uri.split(u'://')
        prefix, path = parts[0].lower(), u'://'.join(parts[1:])
        parts = path.split(u'/')
        domain, rest = parts[0].lower(), u'/'.join(parts[1:])
        if rest:
            uri = u'%s://%s/%s' % (prefix, domain, rest)
        else:
            uri = u'%s://%s' % (prefix, domain)
        uri = uri.strip()
    return uri


def normalize_uri(uri, normalize=True):
    if normalize:
        uri = urlnorm.norm(uri)
    return uri


def URI(uri, normalize=True, convention=u'uri-2'):
    """Usage:
        from abouttag.uri import URI

        normalURL = URI(u'FluidDB.fluidinfo.com')
    """
    assert convention.lower() in (u'uri-1', u'uri-2')
    if convention == u'uri-1':
        return normalize_uri_1(uri, normalize)
    else:
        if normalize and not u'://' in uri:
            uri = u'http://' + uri
        return normalize_uri(uri, normalize)


class TestURI(about.AboutTestCase):
    def testFluidDBBadConvention(self):
        self.assertRaises(AssertionError, URI, u'hello', convention='unknown')

    def testFluidDBNormalize1(self):
        expected = (
            ('FluidDB.fluidinfo.com', 'http://fluiddb.fluidinfo.com'),
            ('FluidDB.fluidinfo.com/one/two/',
                'http://fluiddb.fluidinfo.com/one/two'),
            ('https://FluidDB.fluidinfo.com/one/two/',
                'https://fluiddb.fluidinfo.com/one/two'),
            ('http://fluiddb.fluidinfo.com/one/two/',
                'http://fluiddb.fluidinfo.com/one/two'),
            ('http://test.com/one/two/?referrer=http://a.b/c',
                'http://test.com/one/two/?referrer=http://a.b/c')
        )
        self.normalizeTest(expected, URI, convention=u'uri-1')

    def testFluidDBNormalize(self):
        expected = (
            ('FluidDB.fluidinfo.com', 'http://fluiddb.fluidinfo.com/'),
            ('FluidDB.fluidinfo.com/one/two/',
                'http://fluiddb.fluidinfo.com/one/two/'),
            ('https://FluidDB.fluidinfo.com/one/two/',
                'https://fluiddb.fluidinfo.com/one/two/'),
            ('http://fluiddb.fluidinfo.com/one/two/',
                'http://fluiddb.fluidinfo.com/one/two/'),
            ('http://test.com/one/two/?referrer=http://a.b/c',
                'http://test.com/one/two/?referrer=http://a.b/c')
        )
        self.normalizeTest(expected, URI)
