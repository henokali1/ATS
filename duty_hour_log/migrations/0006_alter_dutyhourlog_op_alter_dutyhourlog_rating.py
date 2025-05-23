# Generated by Django 5.1.4 on 2025-04-21 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duty_hour_log', '0005_alter_dutyhourlog_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutyhourlog',
            name='op',
            field=models.CharField(choices=[('Solo', 'Solo'), ('OJT', 'OJT'), ('Assessment', 'Assessment')], max_length=20, verbose_name='Operation Type'),
        ),
        migrations.AlterField(
            model_name='dutyhourlog',
            name='rating',
            field=models.CharField(choices=[('', 'ADC'), ('', 'APP'), ('', 'APS'), ('', 'ATCA')], max_length=10),
        ),
    ]
