from django.urls import path
from . import views
from . import managerView
from . import memberView

urlpatterns = [
    path('', views.index, name='index'),
    path('manager/', managerView.manager, name='manager'),
    path('member/', memberView.member, name='member'),
    path('contributionView/', views.contributionView, name='contributionView'),
    path('memberContrib/', memberView.memberContrib, name='memberContrib'),

    # Viewing Individual loan status
    path('pendingDeclined/', memberView.pendingDeclined, name='pendingDeclined'),
    path('grantedLoan/', memberView.grantedLoan, name='grantedLoan'),
    path('loanActive/', memberView.loanActive, name='loanActive'),

    # Viewing all Granted, Pending, Declined Loans

    path('grantedLoanAll/', views.grantedLoanAll, name='grantedLoanAll'),
    path('pendingLoanAll/', views.pendingLoanAll, name='pendingLoanAll'),
    path('declinedLoanAll/', views.declinedLoanAll, name='declinedLoanAll'),

    # messages
    path('message/<str:pk>/', views.message, name='message'),
    path('declinedLoanAllDetails/<str:pk>/', views.declinedLoanAllDetails, name='declinedLoanAllDetails'),

    # Form
    path('memberLoanTemplate/', memberView.memberLoanTemplate, name='memberLoanTemplate'),
    path('paymentForm/', managerView.paymentForm, name='paymentForm'),
    path('contributionForm/', managerView.contributionForm, name='contributionForm'),

    # Edit Form
    path('memberLoanTemplateEdit/<str:pk>/', memberView.memberLoanTemplateEdit, name='memberLoanTemplateEdit'),
]
