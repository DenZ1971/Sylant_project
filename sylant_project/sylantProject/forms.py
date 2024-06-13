from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Machine, Maintenance, Claim, Reference


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Reference.objects.filter(entity__entityCategory='Модель техники')
        self.fields['engine_model'].queryset = Reference.objects.filter(entity__entityCategory='Модель двигателя')
        self.fields['transmission_model'].queryset = Reference.objects.filter(entity__entityCategory='Модель трансмиссии')
        self.fields['drive_axle_model'].queryset = Reference.objects.filter(entity__entityCategory='Модель ведущего моста')
        self.fields['steering_axle_model'].queryset = Reference.objects.filter(entity__entityCategory='Модель управляемого моста')
        self.fields['client'].queryset = Reference.objects.filter(entity__entityCategory='Клиент')
        self.fields['service_company'].queryset = Reference.objects.filter(entity__entityCategory='Сервисная компания')


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'maintenance_type',
            'maintenance_date',
            'machine_hours',
            'order_number',
            'order_date',
            'company',
            'machine'
        ]

        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['maintenance_type'].queryset = Reference.objects.filter(entity__entityCategory='Вид ТО')
        self.fields['company'].queryset = Reference.objects.filter(entity__entityCategory='Организация проводившая ТО')

        if user:
            if user.role == 'manager':
                self.fields['machine'].queryset = Machine.objects.all()
            elif user.role == 'client':
                self.fields['machine'].queryset = Machine.objects.filter(client=user.client)
            elif user.role == 'service':
                self.fields['machine'].queryset = Machine.objects.filter(service_company=user.service_organization)
            else:
                self.fields['machine'].queryset = Machine.objects.none()


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'failure_date',
            'machine_hours',
            'failure_unit',
            'failure_description',
            'recovery_method',
            'spare_parts',
            'recovery_date',
            'downtime',
            'machine'
        ]
        widgets = {
            'failure_date': forms.DateInput(attrs={'type': 'date'}),
            'recovery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['failure_unit'].queryset = Reference.objects.filter(entity__entityCategory='Узел отказа')
        self.fields['recovery_method'].queryset = Reference.objects.filter(entity__entityCategory='Метод восстановления')

        if user:
            if user.role == 'manager':
                self.fields['machine'].queryset = Machine.objects.all()
            elif user.role == 'client':
                self.fields['machine'].queryset = Machine.objects.filter(client=user.client)
            elif user.role == 'service':
                self.fields['machine'].queryset = Machine.objects.filter(service_company=user.service_organization)
            else:
                self.fields['machine'].queryset = Machine.objects.none()

class MachineSearchForm(forms.Form):
    serial_number = forms.CharField(label='Заводской номер машины', max_length=100, widget=forms.TextInput(attrs={'type': 'search'}))

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['name', 'description']

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Введите тот же пароль, что и выше, для проверки.",
    )
    role = forms.ChoiceField(
        label="Роль",
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    client = forms.ModelChoiceField(
        label="Клиент",
        queryset=Reference.objects.filter(entity__entityCategory='Клиент'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    service_organization = forms.ModelChoiceField(
        label="Сервисная организация",
        queryset=Reference.objects.filter(entity__entityCategory='Сервисная компания'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'client', 'service_organization')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        help_texts = {
            'username': 'Обязательно. Не более 150 символов. Только буквы, цифры и @/./+/-/_.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'