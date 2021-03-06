from Acquisition import aq_base
from plone.app.portlets.storage import UserPortletAssignmentMapping
from plone.portlets.constants import USER_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.utils import unhashPortletInfo, hashPortletInfo
from Products.Five import BrowserView
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from zExceptions import Unauthorized


class UpdateOrder(BrowserView):

    def __call__(self, *args, **kwargs):
        # prepare submitted data
        dashboard = {}
        for portlet in self.request.get('portlets'):
            column, _hash = portlet.split(':')
            if column not in dashboard.keys():
                dashboard[column] = []
            dashboard[column].append(_hash)
        replace_hashes = []
        # reorder portlets
        for column, portlets in dashboard.items():
            for i in range(len(portlets)):
                replace_hashes += self.reorder_portlet(column, i, portlets[i])
        return ';'.join([':'.join(x) for x in replace_hashes])

    def reorder_portlet(self, new_column_name, new_index, _hash):
        portlet_info = unhashPortletInfo(_hash)
        name = portlet_info['name']
        column = self.get_column_and_portlet(portlet_info)[0]

        userid = portlet_info['key']
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        if userid != member.getId():
            raise Unauthorized

        keys = list(column.keys())
        if name in keys:
            keys.remove(name)
            keys.insert(new_index, name)
            column.updateOrder(keys)

        if column.__manager__ != new_column_name:
            new_column = self.get_column_by_name(new_column_name)
            newhash = self.move_portlet_to_column(portlet_info, new_column)
            return [(_hash, newhash)]
        else:
            return []

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

    def get_column_by_name(self, column_name):
        column_manager = getUtility(IPortletManager, name=column_name)
        userid = self.context.portal_membership.getAuthenticatedMember()\
            .getId()
        category = column_manager.get(USER_CATEGORY, {})
        notfound = object()
        manager = category.get(userid, notfound)
        if manager == notfound:
            manager = category[userid] = \
                UserPortletAssignmentMapping(
                    manager=column_name,
                    category=USER_CATEGORY,
                    name=userid)
        return manager

    def move_portlet_to_column(self, portlet_info, new_column):
        prev_column, portlet = self.get_column_and_portlet(portlet_info)
        prev_column = aq_base(prev_column)
        new_column = aq_base(new_column)
        portlet = aq_base(portlet)
        # check ids
        oldid = portlet.id
        newid = portlet.id
        if oldid in new_column.keys():
            index = 1
            _sum = new_column.keys() + prev_column.keys()
            while '%s%i' % (newid, index) in _sum:
                index += 1
            newid = '%s%i' % (newid, index)
        # remove from current column
        del prev_column[oldid]
        # add to new column
        new_column[newid] = portlet
        portlet_info['name'] = newid
        portlet_info['manager'] = new_column.__manager__
        return hashPortletInfo(portlet_info)


def update_dashboard_order(self, *args, **kwargs):
    view = UpdateOrder(self, self.REQUEST)
    return view(*args, **kwargs)
