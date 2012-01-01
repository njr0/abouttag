from distutils.core import setup

setup(name='abouttag',
      version='1.0',
      description='Normalized Fluidinfo about tags',
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
          'License :: OSI Approved :: BSD License',
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet',
      ],
      long_description = '''\
This package provides functions for generating about tags for
Fluidinfo following various conventions.

Fluidinfo is a hosted, online database based on the notion of tagging.
For more information on FluidDB, visit http://fluidinfo.com.

For more information on the ideas that motivated this module,
see posts at http://abouttag.blogspot.com.   A good place to
start is

http://abouttag.blogspot.com/2010/03/about-tag-conventions-in-fluiddb.html
      '''
      
     )
