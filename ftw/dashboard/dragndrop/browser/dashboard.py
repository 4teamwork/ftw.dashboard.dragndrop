from plone.app.layout.dashboard.dashboard import DashboardView
from plone.portlets.interfaces import IPortletType
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility


# Try to get the plone.protect's createToken method, because it's only
# available since version 2.0.2, otherwise we just use a mocked method.
try:
    from plone.protect import createToken
except ImportError:
    def createToken():
        return ''


class FTWDashBoard(DashboardView):
    """ Improve the default Plone Dashboard """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.props = getattr(
            self.context.portal_properties,
            'ftw.dashboard',
            None)

        if not self.showleftcolumn:
            request.set('disable_plone.leftcolumn', True)
        else:
            request.set('disable_plone.leftcolumn', False)
        if not self.showrightcolumn:
            request.set('disable_plone.rightcolumn', True)
        else:
            request.set('disable_plone.rightcolumn', False)

    def authenticator_token(self):
        return createToken()

    def dashboard_props(self):
        return getattr(self.context.portal_properties, 'ftw.dashboard', None)

    @property
    def editable(self):
        return self.props.getProperty('dashboardEditable', False)

    def add_portlet_options(self):
        mtool = getToolByName(self.context, 'portal_membership')
        userid = mtool.getAuthenticatedMember().getId()
        manager_base = '/++dashboard++plone.dashboard1+%s/' % userid

        options = []

        for info in self.registered_portlelts():
            if info['id'].startswith('@@'):
                value = '%s/%s' % (manager_base, info['id'])
            else:
                value = '%s+/%s' % (manager_base, info['id'])

            options.append({
                    'value': value,
                    'label': info['title']})
        return options

    def registered_portlelts(self):
        """ Returns the registered portlets in a list with 2 item tuple
        [('id', 'user friendly'), ( 'id2', 'Another Portlet')] """

        ret = []
        if self.props:
            portlets = self.props.addable_portlets
            for portlet in portlets:
                id_, title = self._get_portlet_id_and_title(portlet)
                ret.append(dict(id=id_, title=title))
        return ret

    def _get_portlet_id_and_title(self, name):
        """Returns the title of the portlet by the name configured in
        the addable_portlets property. The name may have the form
        "[id]:[title]", in this case the title defined in
        the porperty is used, otherwise the default portlet property
        is retrieved.
        Returns the portlet id and the title to use.
        """

        if ':' in name:
            return name.split(':', 1)

        portlet = queryUtility(IPortletType, name=name)

        if portlet:
            return name, portlet.title

        else:
            return name, name

    @property
    def showleftcolumn(self):
        return bool(getattr(self.props, 'showleftcolumn', False))

    @property
    def showrightcolumn(self):
        return bool(getattr(self.props, 'showrightcolumn', False))
