from django.db import models
from Register_Login.models import LoginDetails
from Register_Login.models import CompanyDetails
from datetime import datetime
from datetime import date

# Create your models here.

#---------------- models for zoho modules--------------------
class Banking(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE)
    bnk_name = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_branch = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_acno = models.CharField(max_length=220,default='', null=True, blank=True)
    bnk_ifsc = models.CharField(max_length=220,default='', null=True, blank=True)
    BAL_TYPE = [
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    ]
    bnk_bal_type = models.CharField(max_length=220,choices=BAL_TYPE, default='Debit')
    bnk_opnbal =models.FloatField(null=True, blank=True)
    bnk_bal =models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    document=models.FileField(upload_to='bank/',null=True,blank=True)
    status= models.TextField(default='Active')


class BankAccount(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    bank=models.ForeignKey(Banking, on_delete=models.CASCADE,null=True,blank=True)
    customer_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    account_type = models.CharField(max_length=2)
    bankname=models.CharField(max_length=100)
    account_number = models.CharField(max_length=15, unique=True)
    ifsc_code = models.CharField(max_length=11)
    swift_code = models.CharField(max_length=11)
    branch_name = models.CharField(max_length=100)
    cheque_book_range = models.CharField(max_length=5)
    enable_cheque_printing = models.CharField(max_length=3)
    cheque_printing_configuration = models.CharField(max_length=3)
    mailing_name = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    pin = models.CharField(max_length=6)
    pan_number = models.CharField(max_length=10, blank=True,unique=True)
    registration_type = models.CharField(max_length=15)
    gst_num = models.CharField(max_length=15, blank=True)
    alter_gst_details = models.BooleanField(default=False)
    date = models.DateField()
    amount_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class BankAccountHistory(models.Model):
    company=models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    logindetails= models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    bank_holder=models.ForeignKey(BankAccount, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    action = models.CharField(max_length=10)

class Loan_Term(models.Model):
    duration= models.IntegerField(null=True,blank=True)
    term = models.CharField(max_length=255,null=True,blank=True)
    days = models.IntegerField(null=True,blank=True)
    company = models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)

class loan_account(models.Model):
    bank_holder=models.ForeignKey(BankAccount,on_delete=models.CASCADE,null=True)
    logindetails = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company = models.ForeignKey(CompanyDetails, on_delete=models.CASCADE,null=True,blank=True)
    loan_term = models.ForeignKey(Loan_Term, on_delete=models.CASCADE,null=True,blank=True)
    account_number = models.CharField(max_length=15, unique=True,null=True)
    loan_amount=models.IntegerField()
    balance=models.IntegerField(default=0,null=True)
    lender_bank=models.CharField(max_length=255)
    loan_date = models.DateField()
    payment_method=models.CharField(max_length=255)
    upi_id=models.CharField(max_length=255)
    cheque=models.CharField(max_length=255)
    loan_rec_bank_acc=models.CharField(max_length=255)
    processing_method=models.CharField(max_length=255)
    processing_upi=models.CharField(max_length=255,null=True)
    processing_cheque=models.CharField(max_length=255,null=True)
    processing_acc=models.CharField(max_length=255,null=True)
    processing_fee=models.IntegerField()
    term=models.CharField(max_length=15,null=True)
    interest=models.IntegerField()
    description=models.CharField(max_length=255)
    status= models.TextField(default='Active')



class LoanRepayemnt(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    loan=models.ForeignKey(loan_account, on_delete=models.CASCADE,null=True,blank=True)
    principal_amount=models.IntegerField(null=True,blank=True)
    interest_amount=models.IntegerField(null=True,blank=True)
    payment_method=models.CharField(max_length=255)
    upi_id=models.CharField(max_length=255)
    cheque=models.CharField(max_length=255)
    payment_date=models.DateField(default=date.today)
    total_amount=models.IntegerField(null=True,blank=True)
    type=models.CharField(max_length=255,null=True)

class LoanAccountHistory(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    loan=models.ForeignKey(loan_account,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(default=date.today)
    action=models.CharField(max_length=255)

class LoanRepaymentHistory(models.Model):
    login_details = models.ForeignKey(LoginDetails, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True,blank=True)
    repayment=models.ForeignKey(LoanRepayemnt,on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(default=date.today)
    action=models.CharField(max_length=255)




    