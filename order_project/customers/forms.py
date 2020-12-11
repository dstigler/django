from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit

from .models import Customer

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = ''
        self.helper.field_class = ''
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0 '),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Field('company_name', css_class="form-group col-md-6 mb-0 "),
            Row(
                Column('country', css_class='form-group col-md-2 mb-0 '),
                Column('postal_code', css_class='form-group col-md-1 mb-0'),
                Column('city', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Field('address', css_class="form-group col-md-6 mb-0 "),
            Row(
                Column('phone_number', css_class='form-group col-md-3 mb-0 '),
                Column('email', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Speichern', css_class="mb-5 form-group")
        )

class ReadonlyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ReadonlyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.field_class = 'ml-5'
        self.helper.label_class = 'ml-5'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0 '),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Field('company_name', css_class="form-group col-md-6 mb-0 "),
            Row(
                Column('country', css_class='form-group col-md-2 mb-0 '),
                Column('postal_code', css_class='form-group col-md-1 mb-0'),
                Column('city', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Field('address', css_class="form-group col-md-6 mb-0 "),
            Row(
                Column('phone_number', css_class='form-group col-md-3 mb-0 '),
                Column('email', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            )
        )

class CustomerCreateForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerEditForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerViewForm(ReadonlyForm, forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'