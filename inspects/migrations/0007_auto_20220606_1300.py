# Generated by Django 3.2.13 on 2022-06-06 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspects', '0006_auto_20220604_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspection_details',
            old_name='compliance',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='inspection_details',
            old_name='item_no',
            new_name='inspection_no',
        ),
        migrations.RenameField(
            model_name='inspection_details',
            old_name='compliance_recieved_on',
            new_name='modified_on',
        ),
        migrations.RemoveField(
            model_name='inspection_details',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='marked_officers',
            name='inspection_item_no',
        ),
        migrations.AddField(
            model_name='inspection_details',
            name='inspection_officer',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='compliance',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='compliance_recieved_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='created_by',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='created_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='modified_by',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='modified_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Item_details',
            fields=[
                ('item_no', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=10, null=True)),
                ('status_flag', models.IntegerField()),
                ('observation', models.CharField(max_length=50, null=True)),
                ('modified_on', models.DateTimeField(null=True)),
                ('created_on', models.DateTimeField(null=True)),
                ('modified_by', models.CharField(max_length=10, null=True)),
                ('created_by', models.CharField(max_length=10, null=True)),
                ('inspection_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inspects.inspection_details')),
            ],
        ),
        migrations.AddField(
            model_name='marked_officers',
            name='item_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inspects.item_details'),
        ),
    ]
