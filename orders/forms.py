from django import forms


class OrderForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label='ФИО',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите ФИО'
        })
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите номер телефона'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите email'
        })
    )
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Введите адрес доставки',
            'rows': 3
        })
    )
    comment = forms.CharField(
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Комментарий к заказу (необязательно)',
            'rows': 3
        })
    )