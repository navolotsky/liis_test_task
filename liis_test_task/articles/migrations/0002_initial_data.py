from django.db import migrations

from ..initial_data_migration_code import create_default_groups, get_this_app_label, migrate_permissions


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        (get_this_app_label(), '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_permissions),
        migrations.RunPython(create_default_groups)
    ]
