# Generated by Django 3.0.2 on 2020-01-26 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0011_delete_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply',
        ),
    ]