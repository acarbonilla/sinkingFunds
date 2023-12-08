from django import forms

# from django.contrib.auth.models import User

from baseApp.models import ApplyLoanRequest, Member, Payment, Contribution, Managers


class ContributionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)
        self.fields['paidOn'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
            }
        )
        self.fields['receivedBy'].queryset = Managers.objects.filter(manager__uname__id=user.id)

    class Meta:
        model = Contribution
        fields = '__all__'


class ApplyLoanRequestForm(forms.ModelForm):
    class Meta:
        model = ApplyLoanRequest
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(ApplyLoanRequestForm, self).__init__(*args, **kwargs)
        self.fields['requestor'].queryset = Member.objects.filter(uname=user.id)
        self.fields['approver'].queryset = Managers.objects.filter(manager__uname__id=user.id)


# for updating and granting the loan "ApplyLoanRequestForm
class ApplyLoanRequestEditForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(ApplyLoanRequestEditForm, self).__init__(*args, **kwargs)
        self.fields['dateDecision'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
            }
        )
        self.fields['approver'].queryset = Managers.objects.filter(manager__uname__id=user.id)

    class Meta:
        model = ApplyLoanRequest
        fields = '__all__'


# For payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['loanAccount'].queryset = ApplyLoanRequest.objects.filter(status="Accepted").order_by("-id")
        self.fields['receivingBy'].queryset = Managers.objects.filter(manager__uname__id=user.id)
