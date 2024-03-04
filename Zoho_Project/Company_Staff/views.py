from django.shortcuts import render,redirect
from Register_Login.models import *
from Register_Login.views import logout
from django.contrib import messages
from django.conf import settings
from datetime import date
from django.http import HttpResponse
from datetime import datetime, timedelta
from Company_Staff.models import BankAccount
from Company_Staff.models import loan_account
from Company_Staff.models import LoanRepayemnt
from Company_Staff.models import LoanAccountHistory
from Company_Staff.models import LoanRepaymentHistory
from Company_Staff.models import BankAccountHistory
from Company_Staff.models import Comments
from Company_Staff.models import Banking
from django.shortcuts import render, get_object_or_404
from datetime import date as dt
from django.db.models import Sum
from django.utils.timezone import now
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
from xhtml2pdf import pisa


# Create your views here.



# -------------------------------Company section--------------------------------

# company dashboard
def company_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')

        # Calculate the date 20 days before the end date for payment term renew
        reminder_date = dash_details.End_date - timedelta(days=20)
        current_date = date.today()
        alert_message = current_date >= reminder_date

        # Calculate the number of days between the reminder date and end date
        days_left = (dash_details.End_date - current_date).days
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'alert_message':alert_message,
            'days_left':days_left,
        }
        return render(request, 'company/company_dash.html', context)
    else:
        return redirect('/')


# company staff request for login approval
def company_staff_request(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        staff_request=StaffDetails.objects.filter(company=dash_details.id, company_approval=0).order_by('-id')
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'requests':staff_request,
        }
        return render(request, 'company/staff_request.html', context)
    else:
        return redirect('/')

# company staff accept or reject
def staff_request_accept(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    staff.company_approval=1
    staff.save()
    return redirect('company_staff_request')

def staff_request_reject(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    login_details=LoginDetails.objects.get(id=staff.company.id)
    login_details.delete()
    staff.delete()
    return redirect('company_staff_request')


# All company staff view, cancel staff approval
def company_all_staff(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        all_staffs=StaffDetails.objects.filter(company=dash_details.id, company_approval=1).order_by('-id')
       
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'staffs':all_staffs,
        }
        return render(request, 'company/all_staff_view.html', context)
    else:
        return redirect('/')

def staff_approval_cancel(request, pk):
    """
    Sets the company approval status to 2 for the specified staff member, effectively canceling staff approval.

    This function is designed to be used for canceling staff approval, and the company approval value is set to 2.
    This can be useful for identifying resigned staff under the company in the future.

    """
    staff = StaffDetails.objects.get(id=pk)
    staff.company_approval = 2
    staff.save()
    return redirect('company_all_staff')


# company profile, profile edit
def company_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        terms=PaymentTerms.objects.all()

        # Calculate the date 20 days before the end date
        reminder_date = dash_details.End_date - timedelta(days=20)
        current_date = date.today()
        renew_button = current_date >= reminder_date

        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'renew_button': renew_button,
            'terms':terms,
        }
        return render(request, 'company/company_profile.html', context)
    else:
        return redirect('/')

def company_profile_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_profile_editpage.html', context)
    else:
        return redirect('/')

def company_profile_basicdetails_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            log_details.first_name = request.POST.get('fname')
            log_details.last_name = request.POST.get('lname')
            log_details.email = request.POST.get('eid')
            log_details.username = request.POST.get('uname')
            log_details.save()
            messages.success(request,'Updated')
            return redirect('company_profile_editpage') 
        else:
            return redirect('company_profile_editpage') 

    else:
        return redirect('/')
    
def company_password_change(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            if password == cpassword:
                log_details.password=password
                log_details.save()

            messages.success(request,'Password Changed')
            return redirect('company_profile_editpage') 
        else:
            return redirect('company_profile_editpage') 

    else:
        return redirect('/')
       
def company_profile_companydetails_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details = LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)

        if request.method == 'POST':
            # Get data from the form
            gstno = request.POST.get('gstno')
            profile_pic = request.FILES.get('image')

            # Update the CompanyDetails object with form data
            dash_details.company_name = request.POST.get('cname')
            dash_details.contact = request.POST.get('phone')
            dash_details.address = request.POST.get('address')
            dash_details.city = request.POST.get('city')
            dash_details.state = request.POST.get('state')
            dash_details.country = request.POST.get('country')
            dash_details.pincode = request.POST.get('pincode')
            dash_details.pan_number = request.POST.get('pannumber')

            if gstno:
                dash_details.gst_no = gstno

            if profile_pic:
                dash_details.profile_pic = profile_pic

            dash_details.save()

            messages.success(request, 'Updated')
            return redirect('company_profile_editpage')
        else:
            return redirect('company_profile_editpage')
    else:
        return redirect('/')    

# company modules editpage
def company_module_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_module_editpage.html', context)
    else:
        return redirect('/')

def company_module_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')

        if request.method == 'POST':
            # Retrieve values
            items = request.POST.get('items', 0)
            price_list = request.POST.get('price_list', 0)
            stock_adjustment = request.POST.get('stock_adjustment', 0)
            godown = request.POST.get('godown', 0)

            cash_in_hand = request.POST.get('cash_in_hand', 0)
            offline_banking = request.POST.get('offline_banking', 0)
            upi = request.POST.get('upi', 0)
            bank_holders = request.POST.get('bank_holders', 0)
            cheque = request.POST.get('cheque', 0)
            loan_account = request.POST.get('loan_account', 0)

            customers = request.POST.get('customers', 0)
            invoice = request.POST.get('invoice', 0)
            estimate = request.POST.get('estimate', 0)
            sales_order = request.POST.get('sales_order', 0)
            recurring_invoice = request.POST.get('recurring_invoice', 0)
            retainer_invoice = request.POST.get('retainer_invoice', 0)
            credit_note = request.POST.get('credit_note', 0)
            payment_received = request.POST.get('payment_received', 0)
            delivery_challan = request.POST.get('delivery_challan', 0)

            vendors = request.POST.get('vendors', 0)
            bills = request.POST.get('bills', 0)
            recurring_bills = request.POST.get('recurring_bills', 0)
            vendor_credit = request.POST.get('vendor_credit', 0)
            purchase_order = request.POST.get('purchase_order', 0)
            expenses = request.POST.get('expenses', 0)
            recurring_expenses = request.POST.get('recurring_expenses', 0)
            payment_made = request.POST.get('payment_made', 0)

            projects = request.POST.get('projects', 0)

            chart_of_accounts = request.POST.get('chart_of_accounts', 0)
            manual_journal = request.POST.get('manual_journal', 0)

            eway_bill = request.POST.get('ewaybill', 0)

            employees = request.POST.get('employees', 0)
            employees_loan = request.POST.get('employees_loan', 0)
            holiday = request.POST.get('holiday', 0)
            attendance = request.POST.get('attendance', 0)
            salary_details = request.POST.get('salary_details', 0)

            reports = request.POST.get('reports', 0)

            update_action=1
            status='Pending'

            # Create a new ZohoModules instance and save it to the database
            data = ZohoModules(
                company=dash_details,
                items=items, price_list=price_list, stock_adjustment=stock_adjustment, godown=godown,
                cash_in_hand=cash_in_hand, offline_banking=offline_banking, upi=upi, bank_holders=bank_holders,
                cheque=cheque, loan_account=loan_account,
                customers=customers, invoice=invoice, estimate=estimate, sales_order=sales_order,
                recurring_invoice=recurring_invoice, retainer_invoice=retainer_invoice, credit_note=credit_note,
                payment_received=payment_received, delivery_challan=delivery_challan,
                vendors=vendors, bills=bills, recurring_bills=recurring_bills, vendor_credit=vendor_credit,
                purchase_order=purchase_order, expenses=expenses, recurring_expenses=recurring_expenses,
                payment_made=payment_made,
                projects=projects,
                chart_of_accounts=chart_of_accounts, manual_journal=manual_journal,
                eway_bill=eway_bill,
                employees=employees, employees_loan=employees_loan, holiday=holiday,
                attendance=attendance, salary_details=salary_details,
                reports=reports,update_action=update_action,status=status    
            )
            data.save()
            messages.info(request,"Request sent successfully. Please wait for approval.")
            return redirect('company_module_editpage')
        else:
            return redirect('company_module_editpage')  
    else:
        return redirect('/')


def company_renew_terms(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        if request.method == 'POST':
            select=request.POST['select']
            terms=PaymentTerms.objects.get(id=select)
            update_action=1
            status='Pending'
            newterms=PaymentTermsUpdates(
               company=dash_details,
               payment_term=terms,
               update_action=update_action,
               status=status 
            )
            newterms.save()
            messages.success(request,'Successfully requested an extension of payment terms. Please wait for approval.')
            return redirect('company_profile')
    else:
        return redirect('/')









# -------------------------------Staff section--------------------------------

# staff dashboard
def staff_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_dash.html',context)
    else:
        return redirect('/')


# staff profile
def staff_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_profile.html',context)
    else:
        return redirect('/')


def staff_profile_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'staff/staff_profile_editpage.html', context)
    else:
        return redirect('/')

def staff_profile_details_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        if request.method == 'POST':
            # Get data from the form
            log_details.first_name = request.POST.get('fname')
            log_details.last_name = request.POST.get('lname')
            log_details.email = request.POST.get('eid')
            log_details.username = request.POST.get('uname')
            log_details.save()
            dash_details.contact = request.POST.get('phone')
            old=dash_details.image
            new=request.FILES.get('profile_pic')
            print(new,old)
            if old!=None and new==None:
                dash_details.image=old
            else:
                print(new)
                dash_details.image=new
            dash_details.save()
            messages.success(request,'Updated')
            return redirect('staff_profile_editpage') 
        else:
            return redirect('staff_profile_editpage') 

    else:
        return redirect('/')

def staff_password_change(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            if password == cpassword:
                log_details.password=password
                log_details.save()

            messages.success(request,'Password Changed')
            return redirect('staff_profile_editpage') 
        else:
            return redirect('staff_profile_editpage') 

    else:
        return redirect('/')






# -------------------------------Zoho Modules section--------------------------------
#### Kesia  ####

def loan_listing(request):
  if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            
            
            loan_details = loan_account.objects.filter(company=company)

            # Calculate balance for each loan account
            for loan in loan_details:
                total_emis_paid = LoanRepayemnt.objects.filter(loan=loan, type='EMI paid').aggregate(total=Sum('principal_amount'))['total'] or 0
                total_additional_loan = LoanRepayemnt.objects.filter(loan=loan, type='Additional Loan').aggregate(total=Sum('principal_amount'))['total'] or 0
                loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan
            
            context = {
                'details': dash_details,
                'allmodules': allmodules,
                'loan_details': loan_details,
                'log_details':log_details
                
            }
  return render(request,'zohomodules/loan_account/loan_listing.html',context)

def get_account_number(request, account_id):
    try:
        bank_account = BankAccount.objects.get(id=account_id,)
        account_number = bank_account.account_number
        return JsonResponse({'account_number': account_number})
    except BankAccount.DoesNotExist:
        return JsonResponse({'error': 'Bank account not found'}, status=404)
    
# def full_account_number(request):
#     try:
#         bank_id=request.GET.get('id')
#         acc=Banking.objects.get(bnk_name=bank_id)
#         data = {'bank':acc.bnk_acno}
#         print(data)
#         return JsonResponse(data)
#     except Banking.DoesNotExist:
#         return JsonResponse({'error': 'Banking record not found'}, status=404)
def full_account_number(request):
    try:
        print('bank')
        bank_id = request.GET.get('bank_id')
        acc = Banking.objects.get(bnk_name=bank_id)
        data = {'bank':acc.bnk_acno}
        print(data)
        return JsonResponse(data)
    except Banking.DoesNotExist:
        return JsonResponse({'error': 'Banking record not found'}, status=404)

def add_loan(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                # Fetch company details
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                # Fetch staff details
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            banks = Banking.objects.values('bnk_name','bnk_acno','bnk_ifsc').filter(company=company).distinct()
            today_date=date.today()
            loaned_bank_account_ids = loan_account.objects.values_list('bank_holder_id', flat=True)
            context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'bank_holder': BankAccount.objects.filter(company=company).exclude(id__in=loaned_bank_account_ids),
                    'loan_details': loan_account.objects.filter(company=company),
                    'banks': banks,
                    'today_date':today_date,
                    'log_details':log_details
                }
            

            if request.method == 'POST':
                # account_name = request.POST.get('customer_name')
                # customer_name = BankAccount.objects.get(id=account_name)
                account_name = request.POST.get('account_name')
                account_number = request.POST.get('account_number')
                loan_amount = request.POST.get('loan_amount')
                balance=request.POST.get('loan_amount')
                lender_bank = request.POST.get('lender_bank')
                loan_date = request.POST.get('loan_date')
                payment_method = request.POST.get('payment_method')
                upi_id=request.POST.get('upi_id')
                cheque=request.POST.get('cheque_number')
                payment_accountnumber=request.POST.get('laccount_number')
                processing_method = request.POST.get('processing_method')
                processing_upi=request.POST.get('pupi_id')
                processing_cheque=request.POST.get('pcheque_number')
                processing_acc=request.POST.get('paccount_number')
                interest = request.POST.get('interest', 0)
                processing_fee = request.POST.get('processing_fee', 0)
                description = request.POST.get('description')
                term=request.POST.get('terms')
                
               
                loaned_bank_account_ids = loan_account.objects.values_list('bank_holder_id', flat=True)
                loan = loan_account(
                    company=company,
                    logindetails=log_details,
                    bank_holder_id=account_name,
                    account_number=account_number,
                    loan_amount=loan_amount,
                    balance=balance,
                    lender_bank=lender_bank,
                    loan_date=loan_date,
                    payment_method=payment_method,
                    upi_id=upi_id,
                    cheque=cheque,
                    payment_accountnumber=payment_accountnumber,
                    processing_method=processing_method,
                    processing_upi=processing_upi,
                    processing_cheque=processing_cheque,
                    processing_acc=processing_acc,
                    interest=interest,
                    processing_fee=processing_fee,
                    description=description,
                    term=term
                )
                loan.save()
                
                history=LoanAccountHistory.objects.create(
                    login_details=log_details,
                    company=dash_details,
                    loan=loan,
                    date=now().date(),
                    action='Created'
                )
                history.save()
                
                context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'bank_holder': BankAccount.objects.filter(company=company).exclude(id__in=loaned_bank_account_ids),
                    'loan_details': loan_account.objects.filter(company=company),
                    'banks':banks,
                    'today_date':today_date,
                    'selected_account_name': account_name,
                    'loan': loan,
                    'log_details':log_details
                }

                
                
                return redirect('loan_listing')
            else:
               
                return render(request, 'zohomodules/loan_account/add_loan.html', context)
        else:
            
            return HttpResponse("Unauthorized access")
    else:
        return redirect('/')
    

def save_account_details(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                # Fetch company details
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else:
                # Fetch staff details
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            
            if request.method == 'POST':
               print('inside post')
               customer_name = request.POST.get('customer_name')
               alias = request.POST.get('alias')
               phone_number = request.POST.get('phone_number')
               email = request.POST.get('email')
               account_type = request.POST.get('account_type')
               bankname = request.POST.get('bankname')
               account_number = request.POST.get('baccount_no')
               ifsc_code = request.POST.get('ifsc_code')
               swift_code = request.POST.get('swift_code')
               branch_name = request.POST.get('branch_name')
               cheque_book_range = request.POST.get('cheque_book_range')
               enable_cheque_printing = request.POST.get('enable_cheque_printing')
               cheque_printing_configuration = request.POST.get('cheque_printing_configuration')
               mailing_name = request.POST.get('mailing_name')
               address = request.POST.get('address')
               country = request.POST.get('country')
               state = request.POST.get('state')
               pin = request.POST.get('pin')
               pan_number = request.POST.get('pan_number')
               registration_type = request.POST.get('registration_type')
               gst_num = request.POST.get('gst_num')
               alter_gst_details = request.POST.get('gst_alter_details')
               date = request.POST.get('date')
               #amount_type = request.POST.get('amount_type')
               amount = request.POST.get('amount')
            try:
                bank=BankAccount(
                customer_name=customer_name,
                alias=alias,
                phone_number=phone_number,
                email=email,
                account_type=account_type,
                bankname=bankname,
                account_number=account_number,
                ifsc_code=ifsc_code,
                swift_code=swift_code,
                branch_name=branch_name,
                cheque_book_range=cheque_book_range,
                enable_cheque_printing=enable_cheque_printing,
                cheque_printing_configuration=cheque_printing_configuration,
                mailing_name=mailing_name,
                address=address,
                country=country,
                state=state,
                pin=pin,
                pan_number=pan_number,
                registration_type=registration_type,
                gst_num=gst_num,
                alter_gst_details=alter_gst_details,
                date=date,
                #    amount_type=amount_type,
                amount=amount,
                company=company,
                login_details=log_details,
                    
                    )
                bank.save()
                    
                BankAccountHistory
                bank_history=BankAccountHistory.objects.create(
                            logindetails=log_details,
                            company=dash_details,
                            bank_holder=bank,
                            date=now().date(),
                            action='Created'
                        )
                bank_history.save()
                new_account_id = bank.id  
                new_account_name = customer_name
                data = {
                        'status': 'success',
                        'account_id': new_account_id,
                        'customer_name': new_account_name
                    }
                    
                print(data)
                print('created')
                return JsonResponse(data)
            except Exception as e:
                error_message = str(e)
                return JsonResponse({'status': 'error', 'message': error_message})
            #    context = {
            #         'details': dash_details,
            #         'allmodules': allmodules,}
               

            # return redirect('add_loan')
    # else:
    #     return render(request,'zohomodules/loan_account/add_loan.html')
    
    

def holder_dropdown(request):
    print("start fuction")
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules =ZohoModules.objects.get(company=dash_details.company, status='New')

            loaned_bank_account_ids = loan_account.objects.values_list('bank_holder_id', flat=True)    
            print("inside holder")
            options = {}
            option_objects = BankAccount.objects.filter(company=company).exclude(id__in=loaned_bank_account_ids)
            for option in option_objects:
                options[option.id] = option.customer_name
                print(option.customer_name)
            return JsonResponse(options)

   


def overview(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else: 
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            
            today=date.today()
            today_date = today.strftime("%Y-%m-%d")

            # loan_info = get_object_or_404(loan_account, id=account_id, company=company)
            # account = loan_info.bank_holder
            account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan_info = loan_account.objects.filter(bank_holder=account,company=company).first()
            repayment_details = LoanRepayemnt.objects.filter(loan=loan_info,company=company)
            repayment_history = LoanRepaymentHistory.objects.filter(repayment__in=repayment_details,company=company)
            # repayment_history = LoanRepaymentHistory.objects.filter(repayment='3')
            
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()

            current_balance = loan_info.loan_amount  
            balances = [] 
            loan_side = loan_account.objects.filter(company=company) 
            for loan in loan_side:
                total_emis_paid = LoanRepayemnt.objects.filter(company=company,loan=loan, type='EMI paid').aggregate(total=Sum('principal_amount'))['total'] or 0
                total_additional_loan = LoanRepayemnt.objects.filter(company=company,loan=loan, type='Additional Loan').aggregate(total=Sum('principal_amount'))['total'] or 0
                loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan 

            for repayment in repayment_details:
                if repayment.type == 'EMI paid':
                    current_balance -= repayment.principal_amount
                elif repayment.type == 'Additional Loan':
                    current_balance += repayment.principal_amount     
                balances.append(current_balance)

            overall_balance = current_balance
            repayment_details_with_balances = zip(repayment_details, balances)
            total_amount= loan_info.loan_amount + loan_info.interest


            history=LoanAccountHistory.objects.filter(loan=loan_info,company=company)
            comment=Comments.objects.filter(loan=loan_info,company=company)

            context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'log_id':log_details,
                    'account':account,
                    'loan_info':loan_info,
                    'repayment_details': repayment_details,
                    'repayment_details_with_balances': repayment_details_with_balances,
                    'overall_balance': overall_balance, 
                    'total_amount':total_amount,
                    'history':history,
                    'loan_side':loan_side,
                    'today_date':today_date,
                    'repayment_history':repayment_history,
                    'comment':comment,
                    'banks':banks,
                    
                    'account_id':account_id,
                    'loanpage':'0'
                    
                    
                     }          
    
            return render(request,'zohomodules/loan_account/overview.html',context)
        

def transactoverview(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else: 
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            
            today=date.today()
            today_date = today.strftime("%Y-%m-%d")

            # loan_info = get_object_or_404(loan_account, id=account_id, company=company)
            # account = loan_info.bank_holder
            account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan_info = loan_account.objects.filter(bank_holder=account,company=company).first()
            repayment_details = LoanRepayemnt.objects.filter(loan=loan_info,company=company)
            repayment_history = LoanRepaymentHistory.objects.filter(repayment__in=repayment_details,company=company)
            # repayment_history = LoanRepaymentHistory.objects.filter(repayment='3')
            
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()

            current_balance = loan_info.loan_amount  
            balances = [] 
            loan_side = loan_account.objects.filter(company=company) 
            for loan in loan_side:
                total_emis_paid = LoanRepayemnt.objects.filter(company=company,loan=loan, type='EMI paid').aggregate(total=Sum('principal_amount'))['total'] or 0
                total_additional_loan = LoanRepayemnt.objects.filter(company=company,loan=loan, type='Additional Loan').aggregate(total=Sum('principal_amount'))['total'] or 0
                loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan 

            for repayment in repayment_details:
                if repayment.type == 'EMI paid':
                    current_balance -= repayment.principal_amount
                elif repayment.type == 'Additional Loan':
                    current_balance += repayment.principal_amount     
                balances.append(current_balance)

            overall_balance = current_balance
            repayment_details_with_balances = zip(repayment_details, balances)
            total_amount= loan_info.loan_amount + loan_info.interest


            history=LoanAccountHistory.objects.filter(loan=loan_info,company=company)
            comment=Comments.objects.filter(loan=loan_info,company=company)

            context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'log_id':log_details,
                    'account':account,
                    'loan_info':loan_info,
                    'repayment_details': repayment_details,
                    'repayment_details_with_balances': repayment_details_with_balances,
                    'overall_balance': overall_balance, 
                    'total_amount':total_amount,
                    'history':history,
                    'loan_side':loan_side,
                    'today_date':today_date,
                    'repayment_history':repayment_history,
                    'comment':comment,
                    'banks':banks,
                    
                    'account_id':account_id,
                    'loanpage':'1'
                    
                    
                     }          
    
            return render(request,'zohomodules/loan_account/overview.html',context)
        

from django.http import JsonResponse

def update_status(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else: 
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
        try:
            bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan = loan_account.objects.get(bank_holder=bank_account,company=company)     
            if loan.status == 'Active':
               loan.status = 'Inactive'
            else:
              loan.status = 'Active'   
            loan.save()       
            return redirect('overview',account_id=account_id)
        except loan_account.DoesNotExist:
         return render(request, 'zohomodules/loan_account/overview.html', {'message': 'Loan account does not exist'})


from django.urls import reverse
def repayment_due_form(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
                
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()

            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method=request.POST.get('payment_method')
                upi_id=request.POST.get('upi_id')
                cheque=request.POST.get('cheque_number')
                account_number=request.POST.get('acc_no')
                date = request.POST.get('date')
                total_amount = float(principal_amount) + float(interest_amount)
                type = 'EMI paid'
                print(payment_method)
                repayment = LoanRepayemnt(
                    login_details=login_details,
                    company=company,
                    principal_amount=principal_amount,
                    interest_amount=interest_amount,
                    payment_method=payment_method,
                    upi_id=upi_id,
                    cheque=cheque,
                    account_number=account_number,
                    payment_date=date,
                    total_amount=total_amount,
                    type = type
                )
                
                
                bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
                loan = loan_account.objects.get(bank_holder=bank_account,company=company)
                repayment.loan = loan
                repayment.save()
                repayment_history=LoanRepaymentHistory.objects.create(
                    login_details=login_details,
                    company=company,
                    repayment=repayment,
                    date=now().date(),
                    action='Created'
                )
                repayment_history.save()
                # url = reverse('overview', kwargs={'account_id': account_id}) + '?Transaction=True'
                # return redirect(url)
                return redirect('transactoverview', account_id=account_id)
            else:
                today_date = dt.today()
                
                return render(request, 'zohomodules/loan_account/overview.html', { 'details': dash_details, 'allmodules': allmodules,  'today_date': today_date,'account_id': account_id,'banks':banks,'repayment_history':repayment_history,'login_details':login_details})
    return redirect('/')

def new_loan(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
                
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
                
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()

            today_date = dt.today()
            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method=request.POST.get('payment_method')
                upi_id=request.POST.get('upi_id')
                cheque=request.POST.get('cheque_number')
                account_number=request.POST.get('acc_num')
                date = request.POST.get('date')
                total_amount = request.POST.get('total_amount')
                type = 'Additional Loan'
                
                repayment = LoanRepayemnt(
                    login_details=login_details,
                    company=company,
                    principal_amount=principal_amount,
                    interest_amount=interest_amount,
                    payment_method=payment_method,
                    upi_id=upi_id,
                    cheque=cheque,
                    account_number=account_number,
                    payment_date=date,
                    total_amount=total_amount,
                    type = type
                )
                bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
                loan = loan_account.objects.get(bank_holder=bank_account,company=company)
                
                repayment.loan = loan
                repayment.save()

                repayment_history=LoanRepaymentHistory.objects.create(
                    login_details=login_details,
                    company=company,
                    repayment=repayment,
                    date=now().date(),
                    action='Created'
                )
                repayment_history.save()
                
                return redirect('transactoverview', account_id=account_id)    

            context={
                'allmodules':allmodules,
                'details': dash_details,
                'today_date': today_date,
                'account_id': account_id,
                'banks':banks,
                'repayment_history':repayment_history,
                'login_details': login_details
                
            }
            return render(request, 'zohomodules/loan_account/overview.html',context)
    return redirect('/')

def edit_loanaccount(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')

            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()
            bank_holder=BankAccount.objects.filter(company=company)

            bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan = loan_account.objects.get(bank_holder=bank_account,company=company)


            return render(request, 'zohomodules/loan_account/edit_loan.html', {'account': loan, 'details':dash_details,'bank_holder':bank_holder, 'user_type': user_type, 'allmodules': allmodules,'banks':banks,'login_details':login_details})

    

def edit_loantable(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')

            bank_account = BankAccount.objects.get(id=account_id,company=company)
            loan = loan_account.objects.get(bank_holder=bank_account,company=company)
            banks = Banking.objects.values('bnk_name','bnk_acno').distinct()

            if request.method == 'POST':
                
                loan.bank_holder.customer_name = request.POST.get('account_name')
                loan.loan_amount = request.POST.get('loan_amount')
                loan.lender_bank = request.POST.get('lender_bank')
                loan.loan_date = request.POST.get('loan_date')
                loan.payment_method = request.POST.get('payment_method')
                loan.upi_id = request.POST.get('upi_id')
                loan.cheque = request.POST.get('cheque_number')
                loan.payment_accountnumber = request.POST.get('account_number')
                loan.term = request.POST.get('terms')
                loan.processing_method = request.POST.get('processing_method')
                loan.processing_upi = request.POST.get('p_upi_id')
                loan.processing_cheque = request.POST.get('p_cheque_number')
                loan.processing_acc = request.POST.get('p_account_number')
                loan.interest = request.POST.get('interest')
                loan.processing_fee = request.POST.get('processing_fee')
                loan.description = request.POST.get('description')
                
                loan.save()

                history=LoanAccountHistory.objects.create(
                    login_details=login_details,
                    company=company,
                    loan=loan,
                    date=now().date(),
                    action='Edited'
                )
                history.save()
                
               
                return redirect('overview', account_id=account_id)  

        return render(request, 'zohomodules/loan_account/edit_loan.html', {'loan': loan, 'details': dash_details, 'allmodules': allmodules,'history':history,'banks':banks,'account_id':account_id})



def calculate_overall_balance(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan_info = loan_account.objects.filter(bank_holder=account,company=company).first()
            repayment_details = LoanRepayemnt.objects.filter(loan=loan_info,company=company)
            current_balance = loan_info.loan_amount
            balances = [] 
            loan_side = loan_account.objects.all() 
            for loan in loan_side:
              total_emis_paid = LoanRepayemnt.objects.filter(company=company,loan=loan, type='EMI paid').aggregate(total=Sum('total_amount'))['total'] or 0
              total_additional_loan = LoanRepayemnt.objects.filter(company=company,loan=loan, type='Additional Loan').aggregate(total=Sum('total_amount'))['total'] or 0
              loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan 

            for repayment in repayment_details:
                if repayment.type == 'EMI paid':
                    current_balance -= repayment.total_amount
                elif repayment.type == 'Additional Loan':
                    current_balance += repayment.total_amount     
                balances.append(current_balance)

            overall_balance = current_balance
            return overall_balance

def edit_repayment(request, repayment_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            repayment = get_object_or_404(LoanRepayemnt, id=repayment_id,company=company)
            account_id = repayment.loan.bank_holder_id 
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()
            
           
            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method = request.POST.get('payment_method')
                upi_id = request.POST.get('upi_id')
                cheque = request.POST.get('cheque_number')
                account_number=request.POST.get('acc_no')
                payment_date = request.POST.get('date')
                total_amount = request.POST.get('total_amount')
                type = 'EMI paid' 
                print(repayment.payment_method)
                repayment.principal_amount = principal_amount
                repayment.interest_amount = interest_amount
                repayment.payment_method = payment_method
                repayment.upi_id = upi_id
                repayment.cheque = cheque
                repayment.account_number=account_number
                repayment.payment_date = payment_date
                repayment.total_amount = total_amount
                repayment.type = type
        
                repayment.save()
                
                return redirect('transactoverview' ,account_id=account_id)
            else:
                repayment_history=LoanRepaymentHistory.objects.create(
                    login_details=login_details,
                    company=company,
                    repayment=repayment,
                    date=now().date(),
                    action='Edited'
                )
                repayment_history.save()
                
                
                return render(request, 'zohomodules/loan_account/edit_repayment.html', {'repayment': repayment,'details': dash_details,  'allmodules': allmodules, 'repayment_history':repayment_history,'banks':banks,'login_details':login_details})


def edit_additional_loan(request, repayment_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')
            repayment = get_object_or_404(LoanRepayemnt, id=repayment_id,company=company)
            account_id = repayment.loan.bank_holder_id 
            current_balance=calculate_overall_balance(request,account_id)
            banks = Banking.objects.values('bnk_name','bnk_acno').filter(company=company).distinct()
    
            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method = request.POST.get('payment_method')
                upi_id = request.POST.get('upi_id')
                cheque = request.POST.get('cheque_number')
                account_number=request.POST.get('acc_num')
                payment_date = request.POST.get('date')
                total_amount = request.POST.get('total_amount')
                type = 'Additional Loan'
        
                repayment.principal_amount = principal_amount
                repayment.interest_amount = interest_amount
                repayment.payment_method = payment_method
                repayment.upi_id = upi_id
                repayment.cheque = cheque
                repayment.account_number=account_number
                repayment.payment_date = payment_date
                repayment.total_amount = total_amount
                repayment.type = type
        
                repayment.save()
                
                return redirect('transactoverview',account_id=account_id)
            else:
                hist=LoanRepaymentHistory.objects.create(
                    login_details=login_details,
                    company=company,
                    repayment=repayment,
                    date=now().date(),
                    action='Edited'
                )
                hist.save()
                return render(request, 'zohomodules/loan_account/edit_additional_loan.html', {'repayment': repayment,'details': dash_details,  'allmodules': allmodules,'overall_balance':current_balance,'hist':hist,'banks':banks,'login_details':login_details})            
            
from django.template.loader import render_to_string

def share_email(request, account_id):
    try:
        if request.method == 'POST':
            emails_string = request.POST['email']
            emails_list = [email.strip() for email in emails_string.split(',')]
            bank_account = get_object_or_404(BankAccount, id=account_id)
            loan_info = loan_account.objects.get(bank_holder=bank_account)

            repayment_details = LoanRepayemnt.objects.filter(loan=loan_info)
            current_balance = loan_info.loan_amount  
            balances = [] 
            for repayment in repayment_details:
                if repayment.type == 'EMI paid':
                    current_balance -= repayment.total_amount
                elif repayment.type == 'Additional Loan':
                    current_balance += repayment.total_amount     
                balances.append(current_balance)
            overall_balance = current_balance
            total_amount= loan_info.loan_amount + loan_info.interest

            context = {
                'loan_info': loan_info,
                'repayment_details': repayment_details,
                'repayment_details_with_balances': zip(repayment_details, balances),
                'overall_balance': overall_balance, 
                'total_amount': total_amount,
            }

            html_content = render_to_string('zohomodules/loan_account/mailoverview.html', context)

            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
            pdf = result.getvalue()

            filename = f'{loan_info.bank_holder.customer_name}-statement - {loan_info.id}.pdf'
            subject = f"{loan_info.bank_holder.customer_name} - {loan_info.id}- statement"
            email = EmailMessage(subject, f"Hi,\nPlease find the attached statement - File-{loan_info.bank_holder.customer_name}  .\n--\nRegards,\n", to=emails_list)
            email.attach(filename, pdf, "application/pdf")
            email.from_email = settings.EMAIL_HOST_USER  
            email.send(fail_silently=False)

            messages.success(request, 'Statement has been shared via email successfully..!')
            return redirect('overview', account_id)
    except Exception as e:
        print(e)
        messages.error(request, f'{e}')
        return redirect('overview', account_id)
    

def adding_comment(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')

            bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan_info = loan_account.objects.get(bank_holder=bank_account,company=company)
            if request.method == 'POST':

                comment = request.POST.get('comments')

                comm=Comments.objects.create(
                    login_details=login_details,
                    loan=loan_info,
                    company=company,
                    comment=comment
                )
                comm.save()
                context={'details': dash_details,  'allmodules': allmodules}
                return redirect('overview',account_id=account_id)

        return render(request, 'zohomodules/loan_account/overview.html', context) 
    
def delete_comment(request, comment_id,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')   
              
            comment = get_object_or_404(Comments, id=comment_id,company=company)
            comment.delete()

            context={'details': dash_details,  'allmodules': allmodules,'account_id':account_id}

            return redirect('overview',account_id=account_id)
        return render(request, 'zohomodules/loan_account/overview.html',context) 
    

def delete_repaymenttable(request, id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')

            repayment = get_object_or_404(LoanRepayemnt, id=id,company=company)
            repayment.delete()
            account_id = repayment.loan.bank_holder_id
            context={'details': dash_details,  'allmodules': allmodules}

            return redirect('transactoverview',account_id=account_id)
        return render(request, 'zohomodules/loan_account/overview.html',context)
    
def delete_loan(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                company=dash_details
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                company=dash_details.company
                allmodules = ZohoModules.objects.get(company=dash_details.company, status='New')

            bank_account = get_object_or_404(BankAccount, id=account_id,company=company)
            loan_info = loan_account.objects.get(bank_holder=bank_account,company=company)
            transactions = LoanRepayemnt.objects.filter(loan=loan_info,company=company)
           
            context={'details': dash_details,  'allmodules': allmodules,'loanaccount': loan_info}
            if transactions.exists():
                 messages.error(request, 'This account can be deleted as it has done some transactions !!')
                 return redirect('overview', account_id=account_id)
            else:
                loan_info.delete()
                return redirect('loan_listing')
        return render(request, 'zohomodules/loan_account/overview.html',context)
    

            

        

                



            
                
    

        
        