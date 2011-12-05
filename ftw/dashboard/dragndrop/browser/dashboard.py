from plone.app.layout.dashboard.dashboard import DashboardView


class FTWDashBoard(DashboardView):
    """ Improve the default Plone Dashboard """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.props = getattr(
            self.context.portal_properties,
            'ftw.dashboard',
            None)

    def dashboard_props(self):
        return

    def registered_portlelts(self):
        """ Returns the registered portlets in a list with 2 item tuple
        [('id', 'user friendly'), ( 'id2', 'Another Portlet')] """
        ret = []
        if self.props:
            portlets = self.props.addable_portlets
            for portlet in portlets:
                if ':' in portlet:
                    parts = portlet.split(':')
                    id_ = parts[0]
                    title = ''.join(parts[1:])
                else:
                    id_ = title = portlet
                ret.append(dict(id=id_, title=title))
        return ret

    @property
    def showleftcolumn(self):
        return bool(getattr(self.props, 'showleftcolumn', False))

    @property
    def showrightcolumn(self):
        return bool(getattr(self.props, 'showrightcolumn', False))
