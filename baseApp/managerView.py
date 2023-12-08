from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date

from baseApp.forms import PaymentForm, ContributionForm
from baseApp.models import Contribution, ApplyLoanRequest, Payment


@login_required(login_url='sflogin')
def manager(request):
    # For Payment
    payment = Payment.objects.all()
    payments = 0
    for x in payment:
        payments += x.amount

    # For contribution
    contrib = Contribution.objects.all()
    contribCount = 0
    contribAmount = 0
    for x in contrib:
        contribCount += 1
        contribAmount += x.amount

    # Loan Accepted
    loanAccepted = ApplyLoanRequest.objects.filter(status="Accepted")
    remAmount = 0
    for x in loanAccepted:
        remAmount += x.desiredAmount

    # Calculating the reserved Amount
    reservedAmount = float(contribAmount) * 0.10

    # Calculating the loanable amount
    loanableAmount = float(contribAmount + payments) - (float(remAmount) + reservedAmount)
    remAmounts = remAmount - payments
    # remAmounts = loanableAmount - float(remAmounts1)

    # ApplyLoanRequest Showing List of Borrowers and amount to borrowed
    lgList = ApplyLoanRequest.objects.all().order_by('-id')

    # Aggregate and annotate
    ann = ApplyLoanRequest.objects.aggregate(
        loan_total=Sum('desiredAmount', output_field=FloatField(), distinct=True),
        # loan_paid=Sum('payment__amount', output_field=FloatField()),
        balance=Sum('desiredAmount', output_field=FloatField(), distinct=True) - Sum('payment__amount',
                                                                                     output_field=FloatField(),
                                                                                     distinct=True)
    )

    # Group by
    paymentGroup = Payment.objects.values('loanAccount__id', 'loanAccount__desiredAmount',
                                          'loanAccount__requestor__fName', 'loanAccount__requestor__lName') \
        .annotate(
        gcount=Sum('amount', output_field=FloatField())
    ).order_by()

    context = {'contribCount': contribCount, 'contribAmount': contribAmount, 'reservedAmount': reservedAmount,
               'loanableAmount': loanableAmount, 'lgList': lgList, 'remAmounts': remAmounts, 'payment': payment,
               'ann': ann, 'paymentGroup': paymentGroup}
    return render(request, 'baseApp/manager.html', context)


@login_required(login_url='sflogin')
def contributionForm(request):
    contribution = Contribution.objects.all().filter(paidOn=date.today()).order_by("-id")
    form = ContributionForm(request.user, request.POST)
    if form.is_valid():
        contrib = form.save(commit=False)
        contrib.user = request.user
        contrib.save()
        return redirect('contributionForm')
    else:
        form = ContributionForm(request.user)

    context = {'form': form, 'contribution': contribution}
    return render(request, 'baseAppForms/contributionForm.html', context)


@login_required(login_url='sflogin')
def paymentForm(request):
    # Group by
    paymentGroup = Payment.objects.values('loanAccount__id', 'loanAccount__desiredAmount',
                                          'loanAccount__requestor__fName', 'loanAccount__requestor__lName') \
        .annotate(
        gcount=Sum('amount', output_field=FloatField())
    ).order_by()

    # This is to show the latest accepted and can pay zero amount.
    latestAccepted = ApplyLoanRequest.objects.filter(status="Accepted").latest("id")

    accepted = ApplyLoanRequest.objects.all()

    form = PaymentForm(request.user, request.POST)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.user = request.user
        payment.save()
        return redirect('manager')
    else:
        form = PaymentForm(request.user)

    context = {'form': form, 'accepted': accepted, 'paymentGroup': paymentGroup,
               'latestAccepted': latestAccepted}
    return render(request, 'baseAppForms/paymentForm.html', context)



