from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.db.models import Sum, FloatField, Count
from django.shortcuts import render, redirect
from baseApp.forms import ApplyLoanRequestForm, ApplyLoanRequestEditForm
from baseApp.models import ApplyLoanRequest, Member, Payment, Contribution


# from baseApp.models import ApplyLoanRequest, Member


@login_required(login_url='sflogin')
def member(request):
    members = Member.objects.all()
    loanGranted = ApplyLoanRequest.objects.all().order_by("-id")
    # Details for payment
    loanPayment = Payment.objects.all().order_by("-id")
    # Grouping for payment
    paymentGroup = Payment.objects.values('loanAccount__id', 'loanAccount__desiredAmount',
                                          'loanAccount__requestor__fName', 'loanAccount__requestor__lName',
                                          'loanAccount__requestor__uname__id') \
        .annotate(
        gcount=Sum('amount', output_field=FloatField())
    ).order_by("-loanAccount_id")

    # This is for Total Contribution query. Total # only.
    numContrib = Contribution.objects.filter(member__uname__id=request.user.id).count()

    # This is for Total Contribution total amount.
    contribAmount = Contribution.objects.filter(member__uname__id=request.user.id).aggregate(
        amount=Sum("amount")
    )

    # This is for Latest Date of Contribution query..
    # latestContrib = Contribution.objects.filter(member__uname__id=request.user.id)

    # This is for Status Accepted query. Total # only.
    accepted = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).filter(status="Accepted").count()

    # This is for Status Accepted query. Total # only.
    latestAccepted = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).filter(status="Accepted")\
        .aggregate(
            desired=Sum("desiredAmount"))

    # This is for Status Pending query. Total # only.
    pending = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).filter(status="Pending").count()

    # This is for Status Declined query. Total # only.
    declined = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).filter(status="Declined").count()

    context = {'members': members, 'loanGranted': loanGranted, 'loanPayment': loanPayment,
               'paymentGroup': paymentGroup, 'accepted': accepted, 'pending': pending, 'declined': declined,
               'numContrib': numContrib, 'contribAmount': contribAmount, 'latestAccepted': latestAccepted
               }
    return render(request, 'baseApp/member.html', context)


@login_required(login_url='sflogin')
def memberLoanTemplate(request):
    form = ApplyLoanRequestForm(request.user, request.POST)
    if form.is_valid():
        loan = form.save(commit=False)
        loan.user = request.user
        loan.save()
        return redirect('member')
    else:
        form = ApplyLoanRequestForm(request.user)
    context = {'form': form}
    return render(request, 'baseAppForms/memberLoanForm.html', context)


@login_required(login_url='sflogin')
def memberLoanTemplateEdit(request, pk):
    loan = ApplyLoanRequest.objects.get(id=pk)
    form = ApplyLoanRequestEditForm(request.user, request.POST, instance=loan)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.user = request.user
        edit.save()
        return redirect('paymentForm')
    else:
        form = ApplyLoanRequestEditForm(request.user, instance=loan)

    context = {'form': form}
    return render(request, 'baseAppForms/memberLoanFormEdit.html', context)


@login_required(login_url='sflogin')
def memberContrib(request):
    contribution = Contribution.objects.filter(member__uname__id=request.user.id).order_by("-id")
    context = {'contribution': contribution}
    return render(request, 'baseApp/membercontrib.html', context)


@login_required(login_url='sflogin')
def pendingDeclined(request):
    penclined = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).filter(status="Declined")\
        .order_by("-id")
    context = {'penclined': penclined}
    return render(request, 'baseApp/pendingdeclined.html', context)


@login_required(login_url='sflogin')
def grantedLoan(request):
    granted = ApplyLoanRequest.objects.filter(requestor__uname__id=request.user.id).order_by("-id")
    context = {'granted': granted}
    return render(request, 'baseApp/grantedloan.html', context)


@login_required(login_url='sflogin')
def loanActive(request):
    paymentGroup = Payment.objects.values('loanAccount__id', 'loanAccount__desiredAmount',
                                          'loanAccount__requestor__fName', 'loanAccount__requestor__lName',
                                          'loanAccount__requestor__uname__id') \
        .annotate(
        gcount=Sum('amount', output_field=FloatField())
    ).order_by("-loanAccount_id").filter(loanAccount__requestor__uname__id=request.user.id)
    context = {'paymentGroup': paymentGroup}
    return render(request, 'baseApp/loanactive.html', context)