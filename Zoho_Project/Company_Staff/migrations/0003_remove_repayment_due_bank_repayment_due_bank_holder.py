# Generated by Django 5.0 on 2024-02-06 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Staff', '0002_repayment_due'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repayment_due',
            name='bank',
        ),
        migrations.AddField(
            model_name='repayment_due',
            name='bank_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.bankaccount'),
        ),
    ]
