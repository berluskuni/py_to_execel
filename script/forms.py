__author__ = 'berluskuni'
from django import forms


class NumberCatalogInput(forms.Form):
    catalog_number = forms.CharField(max_length=1200, label='catalog_number')
