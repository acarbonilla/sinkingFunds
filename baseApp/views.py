from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from baseApp.models import Contribution, ApplyLoanRequest, Message


# from baseApp.models import LoanGranted


def index(request):
    context = {}
    return render(request, 'baseApp/index.html', context)


@login_required(login_url='sflogin')
def contributionView(request):
    contribution = Contribution.objects.all().order_by("-id")
    q = request.GET.get('g') if request.GET.get('g') is not None else ''
    contribFilter = Contribution.objects.filter(
        Q(member__fName__icontains=q) |
        Q(member__lName__icontains=q)
        # Q(paidOn__contains=q)
    )

    context = {'contribution': contribution, 'contribFilter': contribFilter}
    return render(request, 'baseApp/contributionView.html', context)


@login_required(login_url='sflogin')
def grantedLoanAll(request):
    loanGranted = ApplyLoanRequest.objects.filter(status="Accepted").order_by("-id")
    context = {'loanGranted': loanGranted}
    return render(request, 'baseApp/grantedloanall.html', context)


@login_required(login_url='sflogin')
def pendingLoanAll(request):
    loanPending = ApplyLoanRequest.objects.filter(status="Pending").order_by("-id")
    context = {'loanPending': loanPending}
    return render(request, 'baseApp/pendingloanall.html', context)


@login_required(login_url='sflogin')
def declinedLoanAll(request):
    loanDeclined = ApplyLoanRequest.objects.filter(status="Declined").order_by("-id")
    context = {'loanDeclined': loanDeclined}
    return render(request, 'baseApp/declinedloanall.html', context)


@login_required(login_url='sflogin')
def declinedLoanAllDetails(request, pk):
    loan = ApplyLoanRequest.objects.get(id=pk)
    loanChat = loan.message_set.all()

    if request.method == 'POST':
        message = Message.objects.create(
            member=request.user,
            loan=loan,
            chat=request.POST.get('chat')
        )
        return redirect('declinedLoanAllDetails', pk=loan.id)

    context = {'loan': loan, 'loanChat': loanChat}
    return render(request, 'baseApp/message.html', context)


@login_required(login_url='sflogin')
def message(request):
    loan = ApplyLoanRequest.objects.all()

    context = {'loan': loan}
    return render(request, 'baseApp/messages.html', context)

