from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Order
from .forms import OrderCreateForm, OrderEditForm
from customers.models import Customer

def home(request):
    context = {
        'orders': Order.objects.all()
    }
    return render(request, 'orders/home.html', context)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/home.html'
    context_object_name = 'orders'
    #ordering = ['get_state_urgency','-date_created']
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search'):
            qs = Order.objects.filter(title__contains=self.request.GET.get('search'))
        else:
            qs = Order.objects.all()
        self.paginate_by = self.request.GET.get('page_elem', 10)
        return sorted(qs, key= lambda t: (-t.get_state_urgency(), t.date_start))
        #return Order.objects.all().order_by(get_state_urgency, )

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search') or ''
        self.paginate_by = self.request.GET.get('page_elem', self.paginate_by)
        return context

    def form_valid(self, form, **kwargs):
        if self.request.is_ajax():
            print("ajax_request")
            context = self.get_context_data(**kwargs)
            return render(self.request, "order_results_partial.html", context)
        print("normal_request")
        return super(OrderListView, self).form_valid(form)
    
    def get_template_names(self):
        if self.request.is_ajax():
            return ['orders/order_results_partial.html']
        return super().get_template_names()

class CustomerOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/customer_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        customer = get_object_or_404(Customer, id=self.kwargs.get('pk'))
        qs = Order.objects.filter(customer=customer)
        return sorted(qs, key= lambda t: (-t.get_state_urgency(), t.date_start))

    def get_context_data(self, **kwargs):
        context = super(CustomerOrderListView, self).get_context_data(**kwargs)
        context['customer_id'] = self.kwargs.get('pk')
        #self.paginate_by = self.request.GET.get('page_elem', 5)
        return context

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        qs = Order.objects.filter(creator=user)
        return sorted(qs, key= lambda t: (-t.get_state_urgency(), t.date_start))

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

class OrderCreateView(LoginRequiredMixin, CreateView):
#    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_form.html'
    # model = Order
    # fields = ['title', 'content', 'customer', 'date_pickup', 'duration']
    success_url = reverse_lazy('orders-home')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.date_start = form.instance.get_startdate()
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Order
    form_class = OrderEditForm
    template_name = 'orders/order_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.date_start = form.instance.get_startdate()
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.creator
        
class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders-home')

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.creator
        