# Generated by Django 4.2.6 on 2023-10-31 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_spaces', '0005_studyspace_denial_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='studyspace',
            name='information',
            field=models.TextField(default=''),
        ),
    ]
