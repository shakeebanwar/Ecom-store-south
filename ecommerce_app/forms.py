from django import forms
from .models import Order


class CartForm(forms.Form):
    quantity = forms.IntegerField(initial='1',min_value=1)
    product_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('paid',)

        def clean_agree(self):
            agree = self.cleaned_data.get('agree')
            if not agree:
                raise forms.ValidationError('This field is required')
            return agree


class DonationForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('paid',)

        def clean_agree(self):
            agree = self.cleaned_data.get('agree')
            if not agree:
                raise forms.ValidationError('This field is required')
            return agree