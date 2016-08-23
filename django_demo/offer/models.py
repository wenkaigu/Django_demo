from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class Candidate(models.Model):

    name = models.CharField(max_length=200)

    email = models.EmailField()

    def validate_mobile(value):
        phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153',
                       '156', '158', '159', '170', '183', '182', '185', '186', '188', '189']
        if len(value) == 11 and value.isdigit() and value[:3] in phoneprefix :
            pass
        else:
            raise ValidationError(
                _('%(value)s is not a valid mobile number'),
                params={'value': value},
            )
    mobile = models.CharField(max_length=11,validators=[validate_mobile])


    GRADES_CHOICES = (
        ('BPO1', 'BPO1'),
        ('BPO2', 'BPO2'),
        ('BPO3', 'BPO3'),
        ('BPO4', 'BPO4'),
        ('BPO5', 'BPO5'),
        ('BPO6', 'BPO6'),
        ('BPO7', 'BPO7'),
        ('BPO8', 'BPO8'),
        ('Y', 'Y'),
        ('C1Y', 'C1Y'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3A', 'C3A'),
        ('C3B', 'C3B'),
        ('C4', 'C4'),
        ('C5', 'C5'),
    )
    grade = models.CharField(max_length=4, choices=GRADES_CHOICES)

    LOCATION_CHOICES = (
        ('SH', 'Shanghai'),
        ('HZ', 'Hangzhou'),
        ('TJ', 'Tianjian'),
        ('DL', 'Dalian'),
        ('BJ', 'Beijing'),
        ('SZ', 'Shenzhen'),
    )

    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)

    additional_location = models.CharField(max_length=200, blank=True)

    PROBATION_CHOICES = (
        ('0', 'No Probation'),
        ('3', '3 Month Probation'),
        ('6', '6 Month Probation'),
    )
    probation = models.CharField(max_length=1, choices=PROBATION_CHOICES)

    salary = models.IntegerField()

    var_pay = models.IntegerField()

    create_date = models.DateField()

    account = models.CharField(max_length=200)

    offer_number = models.CharField(max_length=20)

    recruiter = models.ForeignKey(User)

    offer_date = models.DateField(default=None, null=True, blank=True)

    offer_generated = models.BooleanField(default=False)

    offer_signed = models.BooleanField(default=False)

    def __str__(self):
        return self.name





