# Generated by Django 5.0.6 on 2024-05-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sylantProject', '0002_alter_machine_client_alter_machine_service_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='shipment_date',
            field=models.DateField(),
        ),
    ]
