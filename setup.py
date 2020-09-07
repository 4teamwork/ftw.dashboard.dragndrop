from setuptools import setup, find_packages
import os

version = '1.7.1'
maintainer = 'Mathias Leimgruber'

tests_require = [
    'unittest2',
    'plone.testing',
    'plone.app.testing',
    'transaction',
    'zope.component',
    'zope.configuration',
    'zope.event',
    'zope.traversing',
    'plone.portlets',
    ]

setup(name='ftw.dashboard.dragndrop',
      version=version,
      description="ftw.dashboard.dragndrop adds dragndrop "
      "functionality to the dashboard",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='ftw dashboard dragndrop',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.dashboard.dragndrop',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.dashboard'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        # Zope
        'Acquisition',
        'zope.component',
        'zope.interface',
        'zope.publisher',
        'Zope2',

        # Plone
        'Plone',
        'plone.portlets',
        'plone.theme',
        'plone.app.contentmenu',
        'plone.app.layout',
        'plone.app.portlets',
        'plone.protect',
        'Products.GenericSetup',
        'Products.statusmessages',
        'Products.CMFCore',

        # Addons
        'collective.js.jqueryui',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
