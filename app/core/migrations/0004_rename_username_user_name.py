# Generated by Django 4.1.5 on 2023-04-22 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_name_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
    ]
