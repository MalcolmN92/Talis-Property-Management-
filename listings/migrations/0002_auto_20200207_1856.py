# Generated by Django 3.0.3 on 2020-02-07 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='city',
            new_name='neighborhood',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='state',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='zipcode',
        ),
    ]