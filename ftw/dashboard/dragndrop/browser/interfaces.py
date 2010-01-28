from zope.interface import Interface


class IDashboard(Interface):
    """ marker interface"""


class IDashboardViewable(Interface):
    """ marker interface"""


class IDashboardEditViewable(IDashboardViewable):
    """ marker interface"""
