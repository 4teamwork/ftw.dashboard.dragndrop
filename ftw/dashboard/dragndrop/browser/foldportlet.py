from Products.Five import BrowserView
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from plone.portlets.utils import unhashPortletInfo
from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY
from zExceptions import Unauthorized


class FoldPortlet(BrowserView):

    def __call__(self, *args, **kwargs):
        _hash = self.request.get('hash')
        folded = self.request.get('folded')
        portlet_info = unhashPortletInfo(_hash)
        column, portlet = self.get_column_and_portlet(portlet_info)

        userid = portlet_info['key']
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if userid != member.getId():
            raise Unauthorized

        if portlet_info['name'] in column.keys():
            setattr(portlet, "isFolded", bool(int(folded)))
        return ''

    def get_column_and_portlet(self, portlet_info):
        # get column
        column_manager = getUtility(
            IPortletManager,
            name=portlet_info['manager'])
        userid = self.context.portal_membership.getAuthenticatedMember()\
            .getId()
        column = column_manager.get(USER_CATEGORY, {}).get(userid, {})

        # get portlet
        portlet = column.get(portlet_info['name'])
        return column, portlet
