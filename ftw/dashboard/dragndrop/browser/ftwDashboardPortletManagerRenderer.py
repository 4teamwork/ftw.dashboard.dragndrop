from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.dashboard.dragndrop.browser.interfaces import IDashboardLayer
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.portlets.interfaces import IDashboard
from plone.app.portlets.manager import DashboardPortletManagerRenderer
from zope.component import adapts, queryMultiAdapter
from zope.publisher.interfaces.browser import IBrowserView


class FtwDashboardPortletManagerRenderer(DashboardPortletManagerRenderer):
    """Render a column of the dashboard
    """

    adapts(
        INavigationRoot,
        IDashboardLayer,
        IBrowserView,
        IDashboard)
    template = ViewPageTemplateFile('templates/dashboard-column.pt')

    def isEditable(self, portlet):

        if queryMultiAdapter(
            (portlet, self.request),
            name='edit',
            default=None):
            return True
        else:
            return False
