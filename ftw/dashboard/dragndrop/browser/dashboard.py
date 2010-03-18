from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from plone.app.layout.dashboard.dashboard import DashboardView
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility, queryMultiAdapter


class FTWDashBoard(DashboardView):
    """ Improve the default Plone Dashboard """

    def registered_portlelts(self):
        """ Returns the registered portlets in a list with 2 item tuple
        [('id', 'user friendly'), ( 'id2', 'Another Portlet')] """
        props = self.dashboard_props()
        ret = []
        if props:
            portlets = props.addable_portlets
            for portlet in portlets:
                if ':' in portlet:
                    parts = portlet.split(':')
                    id_ = parts[0]
                    title = ''.join(parts[1:])
                else:
                    id_ = title = portlet
                ret.append(dict(id=id_, title=title))
        return ret

    def dashboard_props(self):
        return getattr(self.context.portal_properties, 'ftw.dashboard', None)

    @property
    def is_editable(self):
        return not ISiteRoot.providedBy(self.context)

    def editable_url(self,view='',manager=''):
        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        manager_name = manager.__name__
        portletManager = getUtility(IPortletManager, name=manager.__name__)['user'].get(member.getId())
        if portletManager is None:
            return ''
        assignments = portletManager.values()
        portlet = None
        for a in assignments:
            if a.__name__ == view.__name__:
                portlet = a
        if portlet is None:
            return ''
        name = portlet.__name__
        editview = queryMultiAdapter((portlet, self.request), name='edit', default=None)
        if editview is None:
            editviewName = ''
        else:
            baseUrl = '%s/++dashboard++%s+%s' % (self.context.portal_url(),manager_name,member.getId())
            referer = '%s/%s' % (self.context.absolute_url(),self.__name__)
            editviewName = '%s/%s/edit?referer=%s' % (baseUrl,name,referer)

        return editviewName
