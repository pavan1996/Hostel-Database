from .models import Person
from django import forms
import django_filters

class PersonFilter(django_filters.FilterSet):
    person_id  		= django_filters.CharFilter(lookup_expr='icontains')
    first_name 		= django_filters.CharFilter(lookup_expr='icontains')
    date_of_birth	= django_filters.NumberFilter(name='date_of_birth', lookup_expr='year')
    person_type 	= django_filters.CharFilter(lookup_expr='icontains')
    middle_name		= django_filters.CharFilter(lookup_expr='icontains')
    last_name		= django_filters.CharFilter(lookup_expr='icontains')
    city			= django_filters.CharFilter(lookup_expr='icontains')
    state			= django_filters.CharFilter(lookup_expr='icontains')
    zipcode			= django_filters.CharFilter(lookup_expr='icontains')
    current_status	= django_filters.CharFilter(lookup_expr='icontains')
    mode_of_communication = django_filters.CharFilter(lookup_expr='icontains')
    reference_person      = django_filters.CharFilter(lookup_expr='icontains')
    period_of_stay_start  = django_filters.CharFilter(lookup_expr='icontains')
    period_of_stay_end    = django_filters.CharFilter(lookup_expr='icontains')
    period_of_stay_greater= django_filters.NumberFilter(name='period_of_stay_start', lookup_expr='gte')
    period_of_stay_less   = django_filters.NumberFilter(name='period_of_stay_end', lookup_expr='lte')
    class Meta:
        model = Person
        fields = ['person_id', 'first_name', 'zipcode','last_name' ,'middle_name','date_of_birth', 'person_type', 'city', 'state', 'current_status' ,'mode_of_communication', 'reference_person', 'period_of_stay_start', 'period_of_stay_end', 'period_of_stay_greater', 'period_of_stay_less'] 