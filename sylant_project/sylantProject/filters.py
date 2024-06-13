import django_filters
from .models import Machine, Maintenance, Claim, Reference


class MachineFilter(django_filters.FilterSet):
    model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Модель техники'),
        field_name='model',
        label='Модель техники'
    )
    engine_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Модель двигателя'),
        field_name='engine_model',
        label='Модель двигателя'
    )
    transmission_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Модель трансмиссии'),
        field_name='transmission_model',
        label='Модель трансмиссии'
    )
    drive_axle_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Модель ведущего моста'),
        field_name='drive_axle_model',
        label='Модель ведущего моста'
    )
    steering_axle_model = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Модель управляемого моста'),
        field_name='steering_axle_model',
        label='Модель управляемого моста'
    )

    class Meta:
        model = Machine
        fields = ['model', 'engine_model', 'transmission_model', 'drive_axle_model', 'steering_axle_model']


class MaintenanceFilter(django_filters.FilterSet):
    maintenance_type = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Вид ТО'),
        field_name='maintenance_type',
        label='Тип ТО'
    )

    service_company = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Сервисная компания'),
        field_name='service_company',
        label='Сервисная компания'
    )
    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'machine__serial_number', 'service_company']


class ClaimFilter(django_filters.FilterSet):
    failure_unit = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Узел отказа'),
        field_name='failure_unit',
        label='Узел отказа'
    )

    recovery_method = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Метод восстановления'),
        field_name='recovery_method',
        label='Метод восстановления'
    )

    service_company = django_filters.ModelChoiceFilter(
        queryset=Reference.objects.filter(entity__entityCategory='Сервисная компания'),
        field_name='service_company',
        label='Сервисная компания'
    )

    class Meta:
        model = Claim
        fields = ['failure_unit', 'recovery_method', 'service_company']