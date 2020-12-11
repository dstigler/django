from django import forms
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field
from django.contrib.admin.widgets import AdminSplitDateTime
import datetime
from .models import Order
from customers.models import Customer

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class OrderCreateForm(BaseForm, forms.ModelForm):
    # date_pickup = forms.DateTimeField(initial=timezone.now())#forms.DateInput(attrs={'type':'date'}, format='%d.%m.%Y')format="%d %b %Y %H:%M:%S %Z")
    date_pickup = forms.SplitDateTimeField(initial=timezone.now(),widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'}, date_format='%Y-%m-%d', time_attrs={'type':'time'}, time_format='%H:%M'))
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label="-----", required=False)

    class Meta:
        model = Order
        fields = ['title', 'content', 'customer', 'date_pickup', 'duration', 'state']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3 create-label'
        self.helper.label_class = 'ml-5'
        self.helper.field_class = 'ml-5'
        self.helper.layout = Layout(
            Field('title', css_class="form-group col-md-9 mb-0 "),
            Field('content', css_class="form-group col-md-9 mb-0 "),
            Row(
                Column('customer', css_class='form-group col-md-3 mb-0 '),
                Column('date_pickup', css_class='form-group col-md-3 mb-0'),
                Column('duration', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Field('state', css_class="form-group col-md-1 mb-0 "),
            Submit('submit', 'Speichern', css_class="ml-5 mb-5 form-group")
        )

class OrderEditForm(BaseForm, forms.ModelForm):
    # date_pickup = forms.DateField()
    date_pickup = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_attrs={'type':'date'}, date_format='%Y-%m-%d', time_attrs={'type':'time'}, time_format='%H:%M'))
    #duration = forms.DurationField(format="%DD %hh")
    
    # duration_days = forms.IntegerField(min_value=0, initial=0)
    # duration_hours = forms.IntegerField(max_value=7, min_value=0, initial=0)
    # #new_duration = forms.MultiValueField((duration_days, duration_hours), require_all_fields=False)
    forms.DurationField
    class Meta:
        model = Order
        fields = ['title', 'content', 'customer', 'date_pickup', 'duration', 'state']

    def __init__(self, *args, **kwargs):
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'ml-5'
        self.helper.field_class = 'ml-5'
        
        self.helper.layout = Layout(
            Field('title', css_class="form-group col-md-9 mb-0"),
            Field('content', css_class="form-group col-md-9 mb-0"),
            Row(
                Column('customer', css_class='form-group col-md-3 mb-0'),
                Column('date_pickup', css_class='form-group col-md-3 mb-0'),
                Column('duration', css_class='form-group col-md-3 mb-0'),
                # Row(
                #     Column('duration_days', css_class='col-4'),
                #     Column('duration_hours', css_class='col-4'),
                #     #Column('new_duration', css_class='col-4'),
                #     css_class='form-row'
                # ),
                css_class='form-row'
            ),
            Field('state', css_class="form-group col-md-1 mb-0 "),
            Submit('submit', 'Speichern', css_class="ml-5 mb-5")
        )
