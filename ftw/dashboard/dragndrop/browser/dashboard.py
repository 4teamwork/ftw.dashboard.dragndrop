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

        if not self.showleftcolumn:
            request.set('disable_plone.leftcolumn', True)
        else:
            request.set('disable_plone.leftcolumn', False)
        if not self.showrightcolumn:
            request.set('disable_plone.rightcolumn', True)
        else:
            request.set('disable_plone.rightcolumn', False)


    def dashboard_props(self):
        return getattr(self.context.portal_properties, 'ftw.dashboard', None)

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
