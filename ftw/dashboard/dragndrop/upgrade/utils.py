from Products.GenericSetup.interfaces import ISetupTool
from Products.CMFCore.utils import getToolByName


_marker = object()


def load_migration_profile(context, profile, steps=_marker):
    if not ISetupTool.providedBy(context):
        context = getToolByName(context, "portal_setup")
    if steps is _marker:
        context.runAllImportStepsFromProfile(profile, purge_old=False)
    else:
        for step in steps:
            context.runImportStepFromProfile(profile,
                                             step,
                                             run_dependencies=False,
                                             purge_old=False)
