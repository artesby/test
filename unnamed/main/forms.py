from django import forms
from django.apps import apps


class FieldForm(forms.Form):

    fields = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        c = kwargs.pop('choices')
        super(FieldForm, self).__init__(*args, **kwargs)
        self.fields['fields'].choices = c
        print(self.fields['fields'].widget)


class FilterForm(forms.Form):
    filter_type = forms.ChoiceField()
    filter_column = forms.ChoiceField()
    value = forms.CharField(
        widget=forms.TextInput(attrs={'size':'4', 'class':'inputText'}),
        required=False
    )
    def __init__(self, *args, **kwargs):
        ft = kwargs.pop('filter_type')
        fc = kwargs.pop('filter_column')
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['filter_type'].choices = ft
        self.fields['filter_column'].choices = fc


class OrderForm(forms.Form):

    order_type = forms.ChoiceField()
    order_column = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        ot = kwargs.pop('order_type')
        oc = kwargs.pop('order_column')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_column'].choices = oc
        self.fields['order_type'].choices = ot
