# Generated by Django 3.2.6 on 2021-08-02 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
