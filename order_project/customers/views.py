from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Customer
from .forms import CustomerCreateForm, CustomerEditForm, CustomerViewForm

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/home.html'
    context_object_name = 'customers'
    paginate_by = 10

class CustomerDetailView(LoginRequiredMixin, UpdateView): 
    model = Customer
    form_class = CustomerViewForm
    template_name = 'customers/customer_detail.html'

class CustomerUpdateView(LoginRequiredMixin, UpdateView): 
    model = Customer
    form_class = CustomerEditForm
    template_name = 'customers/customer_form.html'

class CustomerCreateView(LoginRequiredMixin, CreateView): 
    form_class = CustomerCreateForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customers-home')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customers-home')

@staff_member_required
def ajax_get_customer(request, pk):
    instance = get_object_or_404(Customer, id=pk)
    data = dict()
    data['result'] =  instance.__str__()
    return JsonResponse(data)

@staff_member_required
def ajax_search_customer(request, pk):
    q = request.GET.get('q', None)
    customers = Customer.objects.all().filter(title__startswith=q) if q else Customer.objects.all()
    customers = customers[:12]
    # customers = ProductTable(customers)
    # RequestConfig(request).configure(customers)
    data = dict()
    data['customers'] = customers
    return JsonResponse(data)