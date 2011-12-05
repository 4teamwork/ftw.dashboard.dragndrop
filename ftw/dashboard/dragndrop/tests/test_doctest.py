import unittest2 as unittest
import doctest
from plone.testing import layered
from ftw.dashboard.dragndrop.testing import \
    FTW_DASHBOARD_DRAGNDROP_INTEGRATION_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('dashboard.txt'),
                layer=FTW_DASHBOARD_DRAGNDROP_INTEGRATION_TESTING),
    ])
    return suite
