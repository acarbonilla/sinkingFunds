from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Member(models.Model):
    uname = models.OneToOneField(User, on_delete=models.CASCADE)
    fName = models.CharField(max_length=50, verbose_name='First Name')
    lName = models.CharField(max_length=50, verbose_name='Last Name')
    joinOn = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.uname)


class Managers(models.Model):
    manager = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.manager.uname)


class Contribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.IntegerField(default=500.00)
    paidOn = models.DateField(auto_now_add=False)
    receivedBy = models.ForeignKey(Managers, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.paidOn)


class ApplyLoanRequest(models.Model):
    requestor = models.ForeignKey(Member, on_delete=models.CASCADE)
    desiredAmount = models.IntegerField(verbose_name="Amount")
    dateApplied = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Declined", "Declined")],
        default="Pending"
    )
    dateDecision = models.DateField(blank=True, null=True, verbose_name="Date Resolve")
    approver = models.ForeignKey(Managers, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.dateApplied)


class Payment(models.Model):
    loanAccount = models.ForeignKey(ApplyLoanRequest, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Amount", default=0.00)
    paidDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[("Repayment", "Repayment"), ("Paid", "Paid")],
        default="Repayment"
    )
    receivingBy = models.ForeignKey(Managers, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return str(self.loanAccount) + ' | ' + str(self.status)

    def as_mysql(self, compiler, connection, **extra_context):
        return super().as_sql(
            compiler,
            connection,
            function="CONCAT_WS",
            template="%(function)s('', %(expressions)s)",
            **extra_context
        )


class Message(models.Model):
    loan = models.ForeignKey(ApplyLoanRequest, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
