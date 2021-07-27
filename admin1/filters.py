import django_filters
from django import forms
from django.forms.widgets import TextInput
from django_filters import *
from user.models import *


class OrderFilter(django_filters.FilterSet):
    price_less_than = NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order Price less than'}),
        label='Order Price less than Equal to ', field_name='o_amount', lookup_expr='lte')
    price_greater_than = NumberFilter(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Order price  grater than'}),
        label='Order Price greater than Equal to ', field_name='o_amount', lookup_expr='gte')
    date_after = DateTimeFilter(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY'}),
        label='Date After ', field_name='created_at', lookup_expr='gte')
    date_before = DateTimeFilter(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YYYY'}),
        label='Date Before ', field_name='created_at', lookup_expr='lte')
    order_status = CharFilter(
        widget=TextInput(attrs=({'class': 'form-control', 'placeholder': 'Paid/pending'})),
        label='Order Status', field_name='status', lookup_expr='icontains')

    class Meta:
        model = order_data
        fields = ['o_amount', 'created_at', 'status']
