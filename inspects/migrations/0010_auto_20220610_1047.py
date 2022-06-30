# Generated by Django 2.0.7 on 2022-06-10 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspects', '0009_marked_officers_myuser_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation_master',
            name='railway_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inspects.railwayLocationMaster'),
        ),
        migrations.AlterField(
            model_name='level_desig',
            name='rly_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inspects.railwayLocationMaster'),
        ),
    ]
