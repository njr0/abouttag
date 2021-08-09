# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='abouttag',
      version='1.3.1',
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
          'Programming Language :: Python :: 3',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet',
      ],
      install_requires = ['urlnorm>=1.1.2'],
      long_description_content_type="text/markdown",
      long_description = '''\
This package provides functions for generating about tags for
Fluidinfo following various conventions.

Fluidinfo is a hosted, online database based on the notion of tagging.
For more information on FluidDB, visit http://fluidinfo.com.

For more information on the ideas that motivated this module,
see posts at http://abouttag.blogspot.com.   A good place to
start is

http://abouttag.blogspot.com/2010/03/about-tag-conventions-in-fluiddb.html

EXAMPLE

Examples of usage are provided in the examples directory.
Some simple examples are:

    from abouttag.books import book
    from abouttag.music import album, artist, track
    from abouttag.film import film, movie

    print book(u"One Hundred Years of Solitude", u'Gabriel García Márquez')
    print book(u'The Feynman Lectures on Physics',
               u'Richard P. Feynman', u'Robert B. Leighton',
               u'Matthew Sands')
    print track(u'Bamboulé', u'Bensusan and Malherbe')
    print album(u"Solilaï", u'Pierre Bensusan')
    print artist(u"Crosby, Stills, Nash & Young")
    print film(u"Citizen Kane", u'1941')
    print movie(u"L'Âge d'Or", u'1930')


INSTALLATION

    pip install -U abouttag

DEPENDENCIES

    urlnorm
'''
     )
