# Generated by Django 5.0.6 on 2024-05-22 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sylantProject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_machines', to='sylantProject.reference'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_machines', to='sylantProject.reference'),
        ),
        migrations.AlterField(
            model_name='machine',
            name='shipment_date',
            field=models.DateTimeField(),
        ),
    ]