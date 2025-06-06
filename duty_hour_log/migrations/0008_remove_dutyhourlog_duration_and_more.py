# Generated by Django 5.1.4 on 2025-04-21 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duty_hour_log', '0007_dutyhourlog_duration_alter_dutyhourlog_op_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dutyhourlog',
            name='duration',
        ),
        migrations.AlterField(
            model_name='dutyhourlog',
            name='examiner',
            field=models.ForeignKey(blank=True, help_text='Select for Assessment operations.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='duty_logs_as_examiner', to='duty_hour_log.initial', verbose_name='Examiner'),
        ),
    ]
