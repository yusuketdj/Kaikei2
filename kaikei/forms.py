from .models import Customer, Accounting
from django import forms

class SearchForm(forms.Form):
    customer_id = forms.IntegerField(
        initial='',
        label='ID',
        required=False,
    )
    name = forms.CharField(
        initial='',
        label='名前',
        required=False,
    )

class CustomerCreateForm(forms.ModelForm):

    class Meta:
        model = Customer
        exclude = (
            'is_waiting',
        )

class AccountingCreateForm(forms.ModelForm):

    class Meta:
        model = Accounting
        exclude = (
            'shouhin_total_price',
        )