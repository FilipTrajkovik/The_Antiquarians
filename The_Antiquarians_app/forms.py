from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from The_Antiquarians_app.models import Product

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Product
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control mb-3"

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']