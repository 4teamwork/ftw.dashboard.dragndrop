from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig


class FtwDashboardDragnDropLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.dashboard.dragndrop
        xmlconfig.file('configure.zcml',
            ftw.dashboard.dragndrop,
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.dashboard.dragndrop')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.dashboard.dragndrop:default')


FTW_DASHBOARD_DRAGNDROP_FIXTURE = FtwDashboardDragnDropLayer()
FTW_DASHBOARD_DRAGNDROP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_DASHBOARD_DRAGNDROP_FIXTURE, ),
    name="ftw.dashboard.dragndrop:Integration")
