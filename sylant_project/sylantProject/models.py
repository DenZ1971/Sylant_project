from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class ReferenceEntity(models.Model):
    entityCategory = models.CharField(max_length=100)

    def __str__(self):
        return self.entityCategory


class Reference(models.Model):
    entity = models.ForeignKey(ReferenceEntity, related_name='entity', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('service', 'Сервисная организация'),
        ('manager', 'Менеджер'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Роль")
    client = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_clients', verbose_name="Клиент")
    service_organization = models.ForeignKey(Reference, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_service_organization', verbose_name="Сервисная организация")
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Уникальное имя для обратной связи
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username


class Machine(models.Model):
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Серийный номер")
    model = models.ForeignKey(Reference, related_name='machines', on_delete=models.CASCADE, verbose_name="Модель")
    engine_model = models.ForeignKey(Reference, related_name='engine_models', on_delete=models.CASCADE, verbose_name="Модель двигателя")
    engine_serial_number = models.CharField(max_length=100, verbose_name="Серийный номер двигателя")
    transmission_model = models.ForeignKey(Reference, related_name='transmission_models', on_delete=models.CASCADE, verbose_name="Модель трансмисии")
    transmission_serial_number = models.CharField(max_length=100, verbose_name="Серийный номер трансмиссии")
    drive_axle_model = models.ForeignKey(Reference, related_name='drive_axle_models', on_delete=models.CASCADE, verbose_name="Модель ведущего моста")
    drive_axle_serial_number = models.CharField(max_length=100, verbose_name="Серийный номер ведущего моста")
    steering_axle_model = models.ForeignKey(Reference, related_name='steering_axle_models', on_delete=models.CASCADE, verbose_name="Модель управляемого моста")
    steering_axle_serial_number = models.CharField(max_length=100, verbose_name="Серийный номер управляемого моста")
    delivery_contract = models.CharField(max_length=200, verbose_name="Договор поставки")
    shipment_date = models.DateField(verbose_name="Дата отгрузки")
    consignee = models.CharField(max_length=200, verbose_name="Грузопролучатель")
    delivery_address = models.CharField(max_length=300, verbose_name="Адрес доставки")
    configuration = models.TextField(verbose_name="Комплектация")
    client = models.ForeignKey(Reference, related_name='client_machines', on_delete=models.CASCADE, verbose_name="Клиент")
    service_company = models.ForeignKey(Reference, related_name='service_machines', on_delete=models.CASCADE, verbose_name="Сервисная компания")

    def __str__(self):
        return self.serial_number


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(Reference, related_name='maintenance_types', on_delete=models.CASCADE, verbose_name="Тип ТО")
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    machine_hours = models.PositiveIntegerField(verbose_name="Наработка")
    order_number = models.CharField(max_length=100, verbose_name="Номер заказ-наряда")
    order_date = models.DateField(verbose_name="Дата заказ-наряда")
    company = models.ForeignKey(Reference, related_name='maintenance_companies', on_delete=models.CASCADE, verbose_name="Организация проводившая ТО")
    machine = models.ForeignKey(Machine, related_name='maintenances', on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(Reference, related_name='maintenance_service_companies', on_delete=models.CASCADE, verbose_name="Сервисная компания")


class Claim(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    machine_hours = models.PositiveIntegerField(verbose_name="Наработка машины")
    failure_unit = models.ForeignKey(Reference, related_name='failure_units', on_delete=models.CASCADE, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(Reference, related_name='recovery_methods', on_delete=models.CASCADE, verbose_name="Метод восстановления")
    spare_parts = models.TextField(verbose_name="Используемые запасные части")
    recovery_date = models.DateField(verbose_name="Дата восстановления")
    downtime = models.PositiveIntegerField(verbose_name="Время простоя")
    machine = models.ForeignKey(Machine, related_name='claims', on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(Reference, related_name='claim_service_companies', on_delete=models.CASCADE, verbose_name="Сервисная компания")

    def save(self, *args, **kwargs):
        self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)