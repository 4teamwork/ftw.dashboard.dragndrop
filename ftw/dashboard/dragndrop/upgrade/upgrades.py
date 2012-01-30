from utils import load_migration_profile


def one114_one15(context):
    """1.1.4 -> 1.1.5"""
    load_migration_profile(context, 'profile-ftw.dashboard.dragndrop.upgrade:114-to-115')
