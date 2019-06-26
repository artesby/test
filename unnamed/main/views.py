from django.apps import apps
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .forms import FieldForm, FilterForm, OrderForm
from .utils import write_to_excel
from . import models
from . import fake_data

SELECT_ALL_FIELDS = '0'
NO_FILTER = '0'

ORDERS = (
    (NO_FILTER, 'None'),
    ('dsc', 'desc'),
    ('asc', 'asc'),
)

FILTERS = (
    (NO_FILTER, 'None'),
    ('exact', 'exact'),
    ('contains', 'contains'),
    ('gt', 'greater'),
    ('gte', 'greater\eq'),
    ('lt', 'less'),
    ('lte', 'less\eq'),
    ('startswith', 'startswith'),
    ('endswith', 'endswith'),
)

DISPLAY_ORDER = ('purchase', 'item', 'customer')

def index(request):

    template = loader.get_template('index.html')

    if 'fields' in cache:
        fields = cache.get('fields')
    else:
        fields_purchase = [f.name for f in models.Purchase._meta.fields]
        fields_item = [f.name for f in models.Item._meta.fields]
        fields_customer = [f.name for f in models.Customer._meta.fields]
        fields = {
            'purchase': fields_purchase,
            'item': fields_item,
            'customer': fields_customer,
        }
        cache.set('fields', fields, None)

    columns = []
    columns.extend([f for f in fields['purchase']])
    columns.extend(['item__' + f for f in fields['item']])
    columns.extend(['customer__' + f for f in fields['customer']])

    select_fields_choices = list(zip(
        columns, [key + " " + f for key in DISPLAY_ORDER for f in fields[key]]
    ))

    if request.method == 'POST':

        fields_display = cache.get('fields_display', {})
        query = cache.get('query_filtered', cache.get('query'))

        select_form = FieldForm(
            request.POST,
            choices=select_fields_choices + [(SELECT_ALL_FIELDS, 'all')]
        )

        if select_form.is_valid():
            fields_checked = select_form.cleaned_data['fields']
            print(fields_checked)
            if SELECT_ALL_FIELDS in fields_checked:
                fields_display = fields
            else:
                for key in fields:
                    fields_display[key] = []
                for f in fields_checked:
                    if '__' not in f:
                        fields_display['purchase'].append(f)
                    elif f.startswith('cust'):
                        fields_display['customer'].append(f.split("__")[-1])
                    else:
                        fields_display['item'].append(f.split('__')[-1])

        cache.set('fields_display', fields_display, None)

        filter_form = FilterForm(
            request.POST,
            filter_type=FILTERS,
            filter_column=select_fields_choices
        )

        if filter_form.is_valid():
            filter_type = filter_form.cleaned_data['filter_type']
            filter_column = filter_form.cleaned_data['filter_column']
            filter_value = filter_form.cleaned_data['value']
            filter_params = {
                "__".join((filter_column, filter_type)) : filter_value
            }
            print(filter_params)
            if filter_type != NO_FILTER:
                query = query.filter(**filter_params)

        order_form = OrderForm(
            request.POST, 
            order_type=ORDERS,
            order_column=select_fields_choices
        )

        if order_form.is_valid():
            order_type = order_form.cleaned_data['order_type']
            column = order_form.cleaned_data['order_column']
            if order_type != NO_FILTER:
                if order_type == 'asc':
                    query = query.order_by(column)
                else:
                    query = query.order_by('-'+column)

        cache.set('query_filtered', query, None)

        context = {
            'table': query,
            'fields': fields_display,
            'form': select_form,
            'order_form': order_form,
            'export_filtered': True,
            'filter_form': filter_form,
        }
        return HttpResponse(template.render(context, request))

    else:

        query = models.Purchase.objects.prefetch_related('customer', 'item')

        cache.set('query', query, None)

        cache.delete('query_filtered')
        cache.delete('fields_display')

        select_form = FieldForm(
            choices=select_fields_choices + [(SELECT_ALL_FIELDS, 'all')]
        )

        order_form = OrderForm(
            order_type=ORDERS,
            order_column=select_fields_choices
        )

        filter_form = FilterForm(
            filter_type=FILTERS,
            filter_column=select_fields_choices
        )

        context = {
            'table': query,
            'fields': fields,
            'form': select_form,
            'order_form': order_form,
            'filter_form': filter_form,
        }
        return HttpResponse(template.render(context, request))

def export(request):
    return write_to_excel(cache.get('fields'), cache.get('query'))

def export_filtered(request):
    return write_to_excel(cache.get('fields_display'), cache.get('query_filtered'))

def clear(request):

    models.Customer.objects.all().delete()
    models.Item.objects.all().delete()
    return redirect('index')

def generate(request):

    for _ in range(100):
        name, surname, email, age, purch_sum = fake_data.gen_customer()
        u = models.Customer(
            name=name,
            surname=surname,
            email=email,
            age=age,
            purch_sum=purch_sum,
        )
        u.save()

    for _ in range(200):
        name, price, amount, weight = fake_data.gen_item()
        i = models.Item(
            name=name,
            price=price,
            amount=amount,
            weight=weight,
        )
        i.save()

    items = models.Item.objects.all()
    customers = models.Customer.objects.all()

    for _ in range(50):
        customer, item, purch_date, discount = fake_data.gen_purchase(
            customers, items
        )
        p = models.Purchase(
            customer=customer,
            item=item,
            purch_date=purch_date,
            discount=discount,
        )
        p.save()

    return redirect('index')