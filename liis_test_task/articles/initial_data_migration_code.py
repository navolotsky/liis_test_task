from django.apps.registry import apps as application_registry
from django.contrib.auth.management import create_permissions

from . import models


def get_this_app_label():
    return application_registry.get_containing_app_config("liis_test_task.articles").label


def migrate_permissions(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, using=schema_editor.connection.alias, apps=apps, verbosity=0)
        app_config.models_module = None


def create_default_groups(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    Group = apps.get_model("auth", "Group")

    # With ContentType, need to use db_manager() instead of using() to support multiple databases
    ct = ContentType.objects.get_for_model(models.Article)

    admins = Group.objects.using(db_alias).create(name="admins")
    admins.permissions.add(Permission.objects.using(db_alias).get(codename="do_anything", content_type=ct))

    authors = Group.objects.using(db_alias).create(name="authors")
    authors.permissions.add(
        *[Permission.objects.using(db_alias).get(codename=f"{action}_article", content_type=ct)
          for action in ("view", "add", "change", "delete")]
    )

    subscribers = Group.objects.using(db_alias).create(name="subscribers")
    subscribers.permissions.add(
        Permission.objects.using(db_alias).get(codename="view_not_public_article", content_type=ct))
