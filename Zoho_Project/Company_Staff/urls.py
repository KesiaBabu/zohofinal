from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------Company section--------------------------------
    path('Company/Dashboard',views.company_dashboard,name='company_dashboard'),
    path('Company/Staff-Request',views.company_staff_request,name='company_staff_request'),
    path('Company/Staff-Request/Accept/<int:pk>',views.staff_request_accept,name='staff_request_accept'),
    path('Company/Staff-Request/Reject/<int:pk>',views.staff_request_reject,name='staff_request_reject'),
    path('Company/All-Staffs',views.company_all_staff,name='company_all_staff'),
    path('Company/Staff-Approval/Cancel/<int:pk>',views.staff_approval_cancel,name='staff_approval_cancel'),
    path('Company/Profile',views.company_profile,name='company_profile'),
    path('Company/Profile-Editpage',views.company_profile_editpage,name='company_profile_editpage'),
    path('Company/Profile/Edit/Basicdetails',views.company_profile_basicdetails_edit,name='company_profile_basicdetails_edit'),
    path('Company/Password_Change',views.company_password_change,name='company_password_change'),
    path('Company/Profile/Edit/Companydetails',views.company_profile_companydetails_edit,name='company_profile_companydetails_edit'),
    path('Company/Module-Editpage',views.company_module_editpage,name='company_module_editpage'),
    path('Company/Module-Edit',views.company_module_edit,name='company_module_edit'),
    path('Company/Renew/Payment_terms',views.company_renew_terms,name='company_renew_terms'),







    # -------------------------------Staff section--------------------------------
    path('Staff/Dashboard',views.staff_dashboard,name='staff_dashboard'),
    path('Staff/Profile',views.staff_profile,name='staff_profile'),
    path('Staff/Profile-Editpage',views.staff_profile_editpage,name='staff_profile_editpage'),
    path('Staff/Profile/Edit/details',views.staff_profile_details_edit,name='staff_profile_details_edit'),
    path('Staff/Password_Change',views.staff_password_change,name='staff_password_change'),



    # -------------------------------Zoho Modules section--------------------------------
       ## kesia loan account ##
    path('zohomodules/loan_account/loan_listing',views.loan_listing,name='loan_listing'),
    path('zohomodules/loan_account/add_loan',views.add_loan,name='add_loan'),
    path('zohomodules/loan_account/holder_dropdown',views.holder_dropdown,name='holder_dropdown'),
    path('zohomodules/loan_account/save_account_details',views.save_account_details,name='save_account_details'),
    path('zohomodules/loan_account/overview/<int:account_id>',views.overview,name='overview'),
    path('zohomodules/loan_account/transactoverview/<int:account_id>',views.transactoverview,name='transactoverview'),
    path('zohomodules/loan_account/statementoverview/<int:account_id>',views.statementoverview,name='statementoverview'),
    # path('zohomodules/loan_account/transaction/<int:account_id>',views.transaction,name='transaction'),
    path('zohomodules/loan_account/repayment_due_form/<int:account_id>',views.repayment_due_form,name='repayment_due_form'),
    path('zohomodules/loan_account/new_loan/<int:account_id>',views.new_loan,name='new_loan'),
    path('zohomodules/loan_account/update_status/<int:account_id>',views.update_status,name='update_status'),
    path('zohomodules/loan_account/edit_loanaccount/<int:account_id>',views.edit_loanaccount, name='edit_loanaccount'),
    path('zohomodules/loan_account/edit_loantable/<int:account_id>',views.edit_loantable, name='edit_loantable'),
    path('zohomodules/loan_account/edit_repayment/<int:repayment_id>',views.edit_repayment, name='edit_repayment'),
    path('zohomodules/loan_account/edit_additional_loan/<int:repayment_id>',views.edit_additional_loan, name='edit_additional_loan'),
    path('zohomodules/loan_account/share_email/<int:account_id>',views.share_email,name='share_email'),
    path('zohomodules/loan_account/adding_comment/<int:account_id>',views.adding_comment,name='adding_comment'),
    path('zohomodules/loan_account/delete_comment/<int:comment_id>/<int:account_id>',views.delete_comment,name='delete_comment'),
    path('zohomodules/loan_account/get_account_number/<int:account_id>', views.get_account_number, name='get_account_number'),
    path('zohomodules/loan_account/full_account_number/<int:bank_id>', views.full_account_number, name='full_account_number'),
    path('zohomodules/loan_account/delete_repaymenttable/<int:id>',views.delete_repaymenttable,name='delete_repaymenttable'),
    path('zohomodules/loan_account/delete_loan/<int:account_id>',views.delete_loan,name='delete_loan'),
   


  
    
]