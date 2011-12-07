import unittest2 as unittest
import doctest
from plone.testing import layered
from ftw.dashboard.dragndrop.testing import \
    FTW_DASHBOARD_DRAGNDROP_INTEGRATION_TESTING


DOCTEST_FILES = [
    'dashboard.txt', 
    'dashboard_edit.txt', 
    'dashboard_reset.txt', 
    'portlet_actions.txt', 
    ]


def test_suite():
    suite = unittest.TestSuite()
    for doctest_file in DOCTEST_FILES:
        suite.addTests([
            layered(doctest.DocFileSuite(doctest_file),
                    layer=FTW_DASHBOARD_DRAGNDROP_INTEGRATION_TESTING),
        ])
    return suite
