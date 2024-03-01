# Generated by Django 5.0 on 2024-03-01 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Staff', '0017_rename_loan_rec_bank_acc_loan_account_payment_accountnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan_account',
            name='cheque',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='interest',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='payment_accountnumber',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='processing_acc',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='processing_cheque',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='processing_fee',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='processing_upi',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='term',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='loan_account',
            name='upi_id',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayemnt',
            name='cheque',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='loanrepayemnt',
            name='upi_id',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
