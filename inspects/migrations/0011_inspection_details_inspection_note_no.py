# Generated by Django 2.0.7 on 2022-06-15 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspects', '0010_auto_20220610_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection_details',
            name='inspection_note_no',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
