from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IDashboard(Interface):
    """ marker interface"""


class IDashboardViewable(Interface):
    """ marker interface"""


class IDashboardEditViewable(IDashboardViewable):
    """ marker interface"""


class IDashboardLayer(IDefaultPloneLayer):
    """Browserlayer"""
