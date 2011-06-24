# -*- coding: utf-8 -*-
import re
import unittest

import urllib
import books
import music

AZ_NO_RE = r'^(.*)(\(\d{6}\d*\))$'
AZ_EDITION_RE = r'^(.*)(\(.* edition\))$'
ENCODING = 'latin-1'

class NoTitleError(Exception):
    pass


class NotBookError(Exception):
    pass


def get_html_page_title(url):
    """Gets the stripped contents of the <title> element from a web page,
       specified by a (unicode) URL.

    """
    h = urllib.urlopen(url.encode('UTF-8'))
    line = h.readline()
    while not ('<title') in line:
        line = h.readline()
    lines = [line]
    while not ('</title') in line:
        line = h.readline()
        line.append(line)

    title = ' '.join(lines)
    start = title.find('<title')
    end = title.find('</title')
    title = title[start:end]
    start = title.find('>')
    if start >= 0:
        title = title[start+1:]
    else:
        raise NoTitleError(u'The URL %s apparently has no title' % url)
    return title.replace('&#39;', "'"), h


def process_title(title, kinds):
    parts = [p.strip() for p in title.split(':')]
    kind = parts[-1].lower()
    if not (len(parts) >= 4 and kind in kinds):
        return None, None, None
    parts = parts[:-1]
    for i in range(len(parts)):
        if parts[i].lower().startswith('amazon.'):
            del parts[i]
            break
    if not len(parts) > 1:
        return None, None, None
    title, work = ': '.join(parts[:-1]), parts[-1]
    return title, work, kind


def get_about_tag_for_book(title, h):
    """Attempts to find the information about a product from
       an Amazon UK or Amazon US web page.
       Currently suports only books (and e-books).

       If it succeeds, this returns the best guess at the book-u
       about tag for that book.

       If not, returns None.
    """
    title, author, kind = process_title(title, ('books', 'kindle store'))
    if kind is None:
        return None
    authors = author.decode(ENCODING).split(u',')
    m = re.match(AZ_NO_RE, title)
    if m:
        title = m.group(1).strip()
    m = re.match(AZ_EDITION_RE, title.lower())
    if m:
        title = title[:-len(m.group(2))].strip()
    if title.lower().endswith('ebook'):
        title = title[:-5].strip()
    title = title.decode(ENCODING)
        
    return books.ubook(title, *authors)

def get_about_tag_for_music(title, h):
    work, artist, kind = process_title(title, ('music', 'mp3 downloads'))
    if kind is None:
        return None
    a = artist
    i = a.find(',')     # Change final comma to ampersand
    if i >= 0:
        while i > 0:
            a = a[i+1:]
            i = a.find(',')
        assert artist[-len(a) - 1] == ','
        artist = artist[:-len(a)] + '&' + artist[-len(a):]
    if kind == 'music':
        return music.album(work.decode(ENCODING),  artist.decode(ENCODING))
    else:
        return music.track(work.decode(ENCODING),  artist.decode(ENCODING))

def get_about_tag_for_item(url):
    item = None
    title, h = get_html_page_title(url)
    for method in (get_about_tag_for_book,
                   get_about_tag_for_music):
        item = method(title, h)
        if item:
            break
            h.close()
    return item


class TestAmazonBooks(unittest.TestCase):
    def testURLs(self):
        bookurls = (
            (u"http://www.amazon.co.uk/gp/product/0321616952/ref=s9_simh_gw_p14_d2_i1?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=center-2&pf_rd_r=18GX16Y6EBQVN4SWE9SZ&pf_rd_t=101&pf_rd_p=467128533&pf_rd_i=468294", u"book:designing with web standards voices that matter (jeffrey zeldman; ethan marcotte)"),

        (u"http://www.amazon.com/gp/product/0321616952/ref=s9_simh_gw_p14_d2_i1?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=center-2&pf_rd_r=1QR600K59G2T86FF5KXE&pf_rd_t=101&pf_rd_p=470938631&pf_rd_i=507846", u'book:designing with web standards (jeffrey zeldman; ethan marcotte)'),

       (u"http://www.amazon.com/Before-I-Go-Sleep-Novel/dp/0062060554/ref=bhp_9p2_botm_02?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=center-4&pf_rd_r=1MW9TP9FWZJZ4DXAXSES&pf_rd_t=101&pf_rd_p=1299446602&pf_rd_i=283155", u'book:before i go to sleep a novel (s j watson)'),

        (u"http://www.amazon.com/Hundred-Solitude-Gabriel-Garcia-Marquez/dp/0060929790/ref=sr_1_1?s=books&ie=UTF8&qid=1307974869&sr=1-1", 'book:one hundred years of solitude (gabriel garcia marquez)'),

        (u"http://www.amazon.co.uk/Hundred-Solitude-Gabriel-Garcia-Marquez/dp/014103243X/ref=sr_1_1?ie=UTF8&qid=1307974975&sr=8-1", u'book:one hundred years of solitude (gabriel garcia marquez)'),

        (u"http://www.amazon.co.uk/Café-Best-Coffee-Shop-Design/dp/3037680458/ref=sr_1_3?ie=UTF8&qid=1307975275&sr=8-3", u'book:café best of coffee shop design (braun)'),

        (u"http://www.amazon.com/The-Café-Book-ebook/dp/B004ZZUNPI/ref=sr_1_15?ie=UTF8&qid=1307975833&sr=8-15", u'book:the café book (gail boushey; joan moser)'),
        (u"http://www.amazon.co.uk/The-Lacuna-ebook/dp/B002TVSF9Q/ref=sr_1_1?ie=UTF8&m=A3TVV12T0I6NSM&s=digital-text&qid=1307976072&sr=1-1", u'book:the lacuna (barbara kingsolver)'),
        )

        for (url, abouttag) in bookurls:
            self.assertEqual(get_about_tag_for_item(url), abouttag)

    def testNonBookURL(self):
        url = u"http://www.amazon.co.uk/Kindle-Wireless-Reader-Wifi-Graphite/dp/B002Y27P46/ref=amb_link_160235127_2?pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=center-1&pf_rd_r=0Z9JKC2J7ERVSXFD39XS&pf_rd_t=101&pf_rd_p=244141367&pf_rd_i=468294"

        self.assertEqual(get_about_tag_for_item(url), None)

    def testNonAmazonURL(self):
        url = u"http://stochasticsolutions.com"
        self.assertEqual(get_about_tag_for_item(url), None)

if __name__ == '__main__':
    unittest.main()

