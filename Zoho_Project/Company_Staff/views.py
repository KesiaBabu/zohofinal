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
from django.shortcuts import render, get_object_or_404
from datetime import date as dt
from django.db.models import Sum
from django.utils.timezone import now

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
                # Fetch company details
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                # Fetch staff details
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                allmodules = None
            
            
            loan_details = loan_account.objects.all()

            # Calculate balance for each loan account
            for loan in loan_details:
                total_emis_paid = LoanRepayemnt.objects.filter(loan=loan, type='EMI paid').aggregate(total=Sum('total_amount'))['total'] or 0
                total_additional_loan = LoanRepayemnt.objects.filter(loan=loan, type='Additional Loan').aggregate(total=Sum('total_amount'))['total'] or 0
                loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan
            
            context = {
                'details': dash_details,
                'allmodules': allmodules,
                'loan_details': loan_details,
                
            }
  return render(request,'zohomodules/loan_account/loan_listing.html',context)

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
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                # Fetch staff details
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                allmodules = None
            context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'bank_holder': BankAccount.objects.all(),
                    'loan_details': loan_account.objects.all(),
                }

            if request.method == 'POST':
                account_name = request.POST.get('account_name')
                customer_name = BankAccount.objects.get(id=account_name)
                # account_number = request.POST.get('account_number')
                loan_amount = request.POST.get('loan_amount')
                lender_bank = request.POST.get('lender_bank')
                loan_date = request.POST.get('loan_date')
                payment_method = request.POST.get('payment_method')
                processing_method = request.POST.get('processing_method')
                interest = request.POST.get('interest', 0)
                processing_fee = request.POST.get('processing_fee', 0)
                description = request.POST.get('description')
                try:
                    bank_account = BankAccount.objects.get(id=account_name)
                    account_number = bank_account.account_number
                except BankAccount.DoesNotExist:
                    account_number = ""

                loan = loan_account(
                    bank_holder=customer_name,
                    # account_number=account_number,
                    loan_amount=loan_amount,
                    lender_bank=lender_bank,
                    loan_date=loan_date,
                    payment_method=payment_method,
                    processing_method=processing_method,
                    interest=interest,
                    processing_fee=processing_fee,
                    description=description
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
                    'bank_holder': BankAccount.objects.all(),
                    'loan_details': loan_account.objects.all(),
                }

                
                
                return redirect('loan_listing')
            else:
               
                return render(request, 'zohomodules/loan_account/add_loan.html', context)
        else:
            
            return HttpResponse("Unauthorized access")
    else:
        return redirect('/')
    

def save_account_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        alias = request.POST.get('alias')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        account_type = request.POST.get('account_type')
        bankname = request.POST.get('bankname')
        account_number = request.POST.get('account_number')
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
        # alter_gst_details = request.POST.get('alter_gst_details')
        date = request.POST.get('date')
        amount_type = request.POST.get('amount_type')
        amount = request.POST.get('amount')

        
        BankAccount.objects.create(
            customer_name=name,
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
            # alter_gst_details=alter_gst_details,
            date=date,
            amount_type=amount_type,
            amount=amount
            
        )

        return render(request,'zohomodules/loan_account/add_loan.html')
    else:
        return render(request,'zohomodules/loan_account/add_loan.html')
    
# def holder_dropdown(request):
#     if 'login_id' in request.session:
#         log_id = request.session['login_id']
#         if 'login_id' not in request.session:
#             return redirect('/')
#     log_details = LoginDetails.objects.get(id=log_id)

#     options = {}
#     option_objects = BankAccount.objects.filter(user = user)
#     for option in option_objects:
        
#         options[option.id] = [option.salutation, option.first_name, option.last_name, option.id]
#     return JsonResponse(options)
# def employeeloan_create(request):
#     if 'login_id' in request.session:
#         log_id = request.session['login_id']
#         if 'login_id' not in request.session:
#             return redirect('/')
#     log_details= LoginDetails.objects.get(id=log_id)
  
#     if log_details.user_type == "Company":
#         dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
#         allmodules= ZohoModules.objects.get(company=dash_details,status='New')
#         pay = payroll_employee.objects.filter(company=dash_details,status='active')
#         loan_term =Loan_Term.objects.filter(company=dash_details)
#         toda = date.today()
#         tod = toda.strftime("%Y-%m-%d") 
        
       


#     if log_details.user_type == "Staff":
#         dash_details = StaffDetails.objects.get(login_details=log_details)
#         allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
#         pay = payroll_employee.objects.filter(company=dash_details.company,status='active')
#         loan_term =Loan_Term.objects.filter(company=dash_details.company)
#         toda = date.today()
#         tod = toda.strftime("%Y-%m-%d") 
#     content = {
#             'details': dash_details,
#             'allmodules': allmodules,
#             'log_id':log_details,
#             'pay':pay,
#             'loan_term':loan_term,
#             'tod':tod

           
            
#     }
#     return render(request,'zohomodules/employe_loan/employee_loan_create.html',content)   


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
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
               
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                allmodules = None

            account = get_object_or_404(BankAccount, id=account_id)
            loan_info = loan_account.objects.filter(bank_holder=account).first()
            repayment_details = LoanRepayemnt.objects.filter(loan=loan_info)
           


            current_balance = loan_info.loan_amount  
            balances = [] 
            loan_side = loan_account.objects.all() 
            for loan in loan_side:
                total_emis_paid = LoanRepayemnt.objects.filter(loan=loan, type='EMI paid').aggregate(total=Sum('total_amount'))['total'] or 0
                total_additional_loan = LoanRepayemnt.objects.filter(loan=loan, type='Additional Loan').aggregate(total=Sum('total_amount'))['total'] or 0
                loan.balance = loan.loan_amount - total_emis_paid + total_additional_loan 

            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            # Filter repayment details by date range if start_date and end_date are provided
            if start_date and end_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                repayment_details = repayment_details.filter(payment_date__range=(start_date, end_date))  
                 
            
            
            for repayment in repayment_details:
                if repayment.type == 'EMI paid':
                    current_balance -= repayment.total_amount
                elif repayment.type == 'Additional Loan':
                    current_balance += repayment.total_amount     
                balances.append(current_balance)

            overall_balance = current_balance
            repayment_details_with_balances = zip(repayment_details, balances)
            total_amount= loan_info.loan_amount + loan_info.interest

            history=LoanAccountHistory.objects.filter(loan=loan_info)

            

            
        
       
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
                    'loan_side':loan_side
                     }          
    
            return render(request,'zohomodules/loan_account/overview.html',context)
        
from django.http import JsonResponse

def update_status(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        new_status = request.POST.get('new_status')
        if loan_id and new_status in ['Active', 'Inactive']:
            try:
                loanaccount = loan_account.objects.get(pk=loan_id)
                loanaccount.status = new_status
                loanaccount.save()
                return JsonResponse({'status': new_status})
            except loan_account.DoesNotExist:
                return JsonResponse({'error': 'Loan account does not exist'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def transaction(request,account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        log_details = LoginDetails.objects.get(id=log_id)
        user_type = log_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                
                dash_details = CompanyDetails.objects.get(login_details=log_details, superadmin_approval=1, Distributor_approval=1)
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                
                dash_details = StaffDetails.objects.get(login_details=log_details, company_approval=1)
                allmodules = None
            loan = get_object_or_404(loan_account, id=account_id)
            repayment_details = LoanRepayemnt.objects.filter(loan=loan)
            loan_info = loan_account.objects.get(id=account_id)
            total_emi_paid = repayment_details.aggregate(total_emi_paid=Sum('total_amount'))['total_emi_paid'] or 0
            current_balance = loan_info.loan_amount- total_emi_paid
            total_amount= loan_info.loan_amount + loan_info.interest

            context = {
                    'details': dash_details,
                    'allmodules': allmodules,
                    'loan_info':loan_info,
                    'repayment_details': repayment_details,
                    'account_id': account_id,
                    'current_balance': current_balance,
                    'total_amount':total_amount
                    
                     }
            return render(request,'zohomodules/loan_account/transaction.html', context)

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
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                allmodules = None

            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method=request.POST.get('payment_method'),
                upi_id=request.POST.get('upi_id'),
                cheque=request.POST.get('cheque'),
                date = request.POST.get('date')
                total_amount = float(principal_amount) + float(interest_amount)
                type = 'EMI paid'
                
                repayment = LoanRepayemnt(
                    login_details=login_details,
                    principal_amount=principal_amount,
                    interest_amount=interest_amount,
                    payment_method=payment_method,
                    upi_id=upi_id,
                    cheque=cheque,
                    payment_date=date,
                    total_amount=total_amount,
                    type = type
                )
                
                loan = loan_account.objects.get(pk=account_id)
                repayment.loan = loan
                repayment.save()
                
                return redirect('overview', account_id=account_id)
            else:
                today_date = dt.today()
                
                return render(request, 'zohomodules/loan_account/overview.html', { 'details': dash_details, 'allmodules': allmodules,  'today_date': today_date,'account_id': account_id,})
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
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                allmodules = None
            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method=request.POST.get('payment_method'),
                upi_id=request.POST.get('upi_id'),
                cheque=request.POST.get('cheque'),
                date = request.POST.get('date')
                total_amount = float(principal_amount) + float(interest_amount)
                type = 'Additional Loan'
                
                repayment = LoanRepayemnt(
                    login_details=login_details,
                    principal_amount=principal_amount,
                    interest_amount=interest_amount,
                    payment_method=payment_method,
                    upi_id=upi_id,
                    cheque=cheque,
                    payment_date=date,
                    total_amount=total_amount,
                    type = type
                )
                
                loan = loan_account.objects.get(pk=account_id)
                repayment.loan = loan
                repayment.save()
                
                return redirect('overview', account_id=account_id)
            else:
                today_date = dt.today()

            context={
                'allmodules':allmodules,
                'details': dash_details,
            }
            return render(request, 'zohomodules/loan_account/overview.html', { 'details': dash_details, 'allmodules': allmodules,  'today_date': today_date,'account_id': account_id,})
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
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                allmodules = None
            bank_holder=BankAccount.objects.all()

            loan = loan_account.objects.get(pk=account_id)


            return render(request, 'zohomodules/loan_account/edit_loan.html', {'account': loan, 'details':dash_details,'bank_holder':bank_holder, 'user_type': user_type, 'allmodules': allmodules})

    return redirect('/')

def edit_loan(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                allmodules = None

            loan = loan_account.objects.get(pk=account_id)

            if request.method == 'POST':
                
                loan.bank_holder.customer_name = request.POST.get('account_name')
                loan.account_number = request.POST.get('account_number')
                loan.loan_amount = request.POST.get('loan_amount')
                loan.lender_bank = request.POST.get('lender_bank')
                loan.loan_date = request.POST.get('loan_date')
                loan.payment_method = request.POST.get('payment_method')
                loan.term = request.POST.get('terms')
                loan.processing_method = request.POST.get('processing_method')
                loan.interest = request.POST.get('interest')
                loan.processing_fee = request.POST.get('processing_fee')
                loan.description = request.POST.get('description')
                
                loan.save()

                history=LoanAccountHistory.objects.create(
                    login_details=login_details,
                    company=dash_details,
                    loan=loan,
                    date=now().date(),
                    action='Edited'
                )
                history.save()
                
               
                return redirect('overview', account_id=account_id)  

            return render(request, 'zohomodules/loan_account/edit_loanaccount.html', {'loan': loan, 'details': dash_details, 'user_type': user_type, 'allmodules': allmodules,'history':history})

    return redirect('/')

def edit_repayment(request, account_id):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        
        login_details = LoginDetails.objects.get(id=log_id)
        user_type = login_details.user_type

        if user_type in ['Company', 'Staff']:
            if user_type == 'Company':
                dash_details = CompanyDetails.objects.get(login_details=login_details, superadmin_approval=1, Distributor_approval=1)
                allmodules = ZohoModules.objects.get(company=dash_details, status='New')
            else:
                dash_details = StaffDetails.objects.get(login_details=login_details, company_approval=1)
                allmodules = None
            repayment = get_object_or_404(LoanRepayemnt, id=account_id)
    
            if request.method == 'POST':
                principal_amount = request.POST.get('principal_amount')
                interest_amount = request.POST.get('interest_amount')
                payment_method = request.POST.get('payment_method')
                upi_id = request.POST.get('upi_id')
                cheque = request.POST.get('cheque')
                payment_date = request.POST.get('date')
                total_amount = request.POST.get('total_amount')
                repayment_type = request.POST.get('type')
        
                repayment.principal_amount = principal_amount
                repayment.interest_amount = interest_amount
                repayment.payment_method = payment_method
                repayment.upi_id = upi_id
                repayment.cheque = cheque
                repayment.payment_date = payment_date
                repayment.total_amount = total_amount
                repayment.type = repayment_type
        
                repayment.save()
                return redirect('overview')
            else:
                return render(request, 'zohomodules/loan_account/overview.html', {'repayment': repayment,'details': dash_details,  'allmodules': allmodules})


            
                
    

        
        