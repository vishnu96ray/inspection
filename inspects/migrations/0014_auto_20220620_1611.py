# Generated by Django 2.0.7 on 2022-06-20 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspects', '0013_auto_20220620_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspection_checklist',
            old_name='Inspection_type',
            new_name='inspection_type',
        ),
    ]