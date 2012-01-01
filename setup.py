from distutils.core import setup

setup(name='abouttag',
      version='1.1',
      description='Normalizes about tags for Fluidinfo',
      author='Nicholas J. Radcliffe',
      author_email='njr@StochasticSolutions.com',
      packages=['abouttag'],
      url="http://github.com/njr0/abouttag/",
      download_url="https://github.com/njr0/abouttag",
      keywords=[
          'fluidinfo',
          'about',
          'tag',
          'normalization',
          'canonicalization',
          'standardarization'
      ],
      classifiers = [
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet',
      ],
      install_requires = ['urlnorm>=1.1.2'],
      long_description = '''\
This package provides functions for generating about tags for
Fluidinfo following various conventions.

Fluidinfo is a hosted, online database based on the notion of tagging.
For more information on FluidDB, visit http://fluidinfo.com.

For more information on the ideas that motivated this module,
see posts at http://abouttag.blogspot.com.   A good place to
start is

http://abouttag.blogspot.com/2010/03/about-tag-conventions-in-fluiddb.html

Examples
--------
::

    from abouttag.books import book, ubook, author
    from abouttag.music import album, track, artist, isrc_recording
    from abouttag.film import film, movie

    print '\nBOOKS (book-u convention):\n'

    print book(u"Gödel, Escher, Bach: An Eternal Golden Braid",
               u'Douglas R. Hofstader')
    print
    print book(u"One Hundred Years of Solitude", u'Gabriel García Márquez')
    print book(u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'Robert B. Leighton',
               u'Matthew Sands')
    print
    print book(u'The Oxford English Dictionary: second edition, volume 3',
               u'John Simpson', u'Edmund Weiner')
    print

    print '\nAUTHORS:'

    print author(u'Gabriel García Márquez', 1927, 3, 6)
    print author(u"Douglas R. Hofstadter", 1945, 2, 15)

    print '\nMUSIC (album-u, track-u, artist-u and isrc-1 conventions):\n'
    print track(u'Bamboulé', u'Bensusan and Malherbe')
    print album(u"Solilaï", u'Pierre Bensusan')
    print artist(u"Crosby, Stills, Nash & Young")
    print isrc_recording(u'US-PR3-73-00012')

    print '\nFILM (film-u convention):\n'
    print film(u"Citizen Kane", u'1941')
    print movie(u"L'Âge d'Or", u'1930')
    print


Installation
------------

::

    pip install -U abouttag


Dependencies
------------

`urlnorm <http://pypi.python.org/pypi/urlnorm>`_


      '''
      
     )
