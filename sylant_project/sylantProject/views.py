
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .services import ObjectAuthorizationService, MachineObjectService, MachineQuerysetService, QuerysetService
from .mixin import ManagerRequiredMixin, ClientServiceManagerRequiredMixin, ManagerServiceRequiredMixin
from .forms import MachineForm, CustomUserCreationForm, MachineSearchForm, MaintenanceForm, ClaimForm, ReferenceForm
from .filters import MachineFilter, MaintenanceFilter, ClaimFilter
from .models import Machine, Maintenance, Claim, CustomUser, ReferenceEntity, Reference


class HomeView(TemplateView):
    template_name = 'home.html'


class MachineListView(LoginRequiredMixin, FilterView):
    model = Machine
    template_name = 'machine_list.html'
    context_object_name = 'machines'
    filterset_class = MachineFilter
    ordering = ['-shipment_date']

    def get_queryset(self):
        user = self.request.user
        return MachineQuerysetService.get_machine_queryset(user)

    def get(self, request, *args, **kwargs):
        if request.GET.get('filter') == 'reset':
            return redirect('machine-list')
        return super().get(request, *args, **kwargs)


class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machine_detail.html'
    context_object_name = 'machine'

    def get_object(self, queryset=None):
        user = self.request.user
        machine_id = self.kwargs['pk']
        return MachineObjectService.get_object(user, machine_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machine = context['machine']

        if self.request.user.is_authenticated:
            fields = [
                ('Зав. № машины', machine.serial_number, None),
                ('Модель техники', machine.model, None),
                ('Модель двигателя', machine.engine_model.name, machine.engine_model.description),
                ('Зав. № двигателя', machine.engine_serial_number, None),
                ('Модель трансмиссии', machine.transmission_model.name, machine.transmission_model.description),
                ('Зав. № трансмиссии', machine.transmission_serial_number, None),
                ('Модель ведущего моста', machine.drive_axle_model, None),
                ('Зав. № ведущего моста', machine.drive_axle_serial_number, None),
                ('Модель управляемого моста', machine.steering_axle_model, None),
                ('Зав. № управляемого моста', machine.steering_axle_serial_number, None),
                ('Договор поставки №, дата', machine.delivery_contract, None),
                ('Дата отгрузки с завода', machine.shipment_date, None),
                ('Грузополучатель (конечный потребитель)', machine.consignee, None),
                ('Адрес поставки (эксплуатации)', machine.delivery_address, None),
                ('Комплектация (доп. опции)', machine.configuration, None),
                ('Клиент', machine.client, None),
                ('Сервисная компания', machine.service_company, None),
            ]

            if self.request.user.role == 'manager':
                context['is_manager'] = True

        else:
            fields = [
                ('Зав. № машины', machine.serial_number, None),
                ('Модель техники', machine.model, None),
                ('Модель двигателя', machine.engine_model.name, machine.engine_model.description),
                ('Зав. № двигателя', machine.engine_serial_number, None),
                ('Модель трансмиссии', machine.transmission_model.name, machine.transmission_model.description),
                ('Зав. № трансмиссии', machine.transmission_serial_number, None),
                ('Модель ведущего моста', machine.drive_axle_model, None),
                ('Зав. № ведущего моста', machine.drive_axle_serial_number, None),
                ('Модель управляемого моста', machine.steering_axle_model, None),
                ('Зав. № управляемого моста', machine.steering_axle_serial_number, None),
            ]

        context['fields'] = fields

        if self.request.user.is_authenticated:
            context['back_to_list_url'] = reverse('machine-list')
        else:
            context['back_to_search_url'] = reverse('machine_search')

        return context


class MachineCreateView(ManagerRequiredMixin, LoginRequiredMixin, CreateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machine_form.html'
    success_url = reverse_lazy('machine-list')


class MachineUpdateView(ManagerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machine_update.html'

    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.pk})


class MachineDeleteView(ManagerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Machine
    success_url = reverse_lazy('machine-list')


class MaintenanceListView(LoginRequiredMixin, FilterView):
    model = Maintenance
    template_name = 'maintenance_list.html'
    context_object_name = 'maintenances'
    filterset_class = MaintenanceFilter
    ordering = ['-maintenance_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return QuerysetService.filter_queryset_by_user_role(queryset, user)

    def get(self, request, *args, **kwargs):
        if request.GET.get('filter') == 'reset':
            return redirect('maintenance-list')
        return super().get(request, *args, **kwargs)


class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'maintenance_detail.html'
    context_object_name = 'maintenance'

    def get_object(self, queryset=None):
        user = self.request.user
        maintenance_id = self.kwargs['pk']
        return ObjectAuthorizationService.get_object(user, Maintenance, maintenance_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance = context['maintenance']

        fields = [
            ('Тип ТО', maintenance.maintenance_type.name, maintenance.maintenance_type.description),
            ('Дата ТО', maintenance.maintenance_date, None),
            ('Наработка машины', maintenance.machine_hours, None),
            ('Номер заказа', maintenance.order_number, None),
            ('Дата заказа', maintenance.order_date, None),
            ('Компания', maintenance.company.name, maintenance.company.description),
            ('Машина', maintenance.machine.serial_number, None),
            ('Сервисная компания', maintenance.service_company.name, None),
        ]

        if self.request.user.role == 'manager':
            context['is_manager'] = True

        context['fields'] = fields
        context['back_to_list_url'] = reverse('maintenance-list')
        return context


class MaintenanceCreateView(ClientServiceManagerRequiredMixin, LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_form.html'
    success_url = reverse_lazy('maintenance-list')
    roles = ['client', 'service', 'manager']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        machine = form.cleaned_data.get('machine')
        if machine:
            print(f'Selected machine: {machine}')
            form.instance.service_company = machine.service_company
            print(f'Set service company: {form.instance.service_company}')
        else:
            form.add_error('machine', 'Machine is required')
            return self.form_invalid(form)
        return super().form_valid(form)


class MaintenanceUpdateView(ClientServiceManagerRequiredMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_update.html'

    def get_success_url(self):
        return reverse_lazy('maintenance-detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MaintenanceDeleteView(ManagerRequiredMixin, DeleteView):
    model = Maintenance
    success_url = reverse_lazy('maintenance-list')


class ClaimListView(LoginRequiredMixin, FilterView):
    model = Claim
    template_name = 'claim_list.html'
    context_object_name = 'claims'
    filterset_class = ClaimFilter
    ordering = ['-failure_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return QuerysetService.filter_queryset_by_user_role(queryset, user)

    def get(self, request, *args, **kwargs):
        if request.GET.get('filter') == 'reset':
            return redirect('claim-list')
        return super().get(request, *args, **kwargs)


class ClaimDetailView(LoginRequiredMixin, DetailView):
    model = Claim
    template_name = 'claim_detail.html'
    context_object_name = 'claim'

    def get_object(self, queryset=None):
        user = self.request.user
        claim_id = self.kwargs['pk']
        return ObjectAuthorizationService.get_object(user, Claim, claim_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        claim = context['claim']

        fields = [
            ('Дата отказа', claim.failure_date, None),
            ('Наработка машины', claim.machine_hours, None),
            ('Узел отказа', claim.failure_unit.name, claim.failure_unit.description),
            ('Описание отказа', claim.failure_description, None),
            ('Способ восстановления', claim.recovery_method.name, claim.recovery_method.description),
            ('Запчасти', claim.spare_parts, None),
            ('Дата восстановления', claim.recovery_date, None),
            ('Время простоя (дни)', claim.downtime, None),
            ('Машина', claim.machine.serial_number, None),
            ('Сервисная компания', claim.service_company.name, None),
        ]

        context['fields'] = fields
        context['back_to_list_url'] = reverse('claim-list')

        return context


class ClaimCreateView(ManagerServiceRequiredMixin, LoginRequiredMixin, CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'claim_form.html'
    success_url = reverse_lazy('claim-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        machine = form.cleaned_data.get('machine')
        if machine:
            print(f'Selected machine: {machine}')
            form.instance.service_company = machine.service_company
            print(f'Set service company: {form.instance.service_company}')
        else:
            form.add_error('machine', 'Machine is required')
            return self.form_invalid(form)
        return super().form_valid(form)


class ClaimUpdateView(ManagerServiceRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'claim_update.html'

    def get_success_url(self):
        return reverse_lazy('claim-detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClaimDeleteView(ManagerRequiredMixin, DeleteView):
    model = Claim
    success_url = reverse_lazy('claim-list')


class ManagerView(LoginRequiredMixin, TemplateView):
    template_name = 'manager.html'


class UserCreateView(ManagerRequiredMixin, LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('users-list')


class UsersListView(ManagerRequiredMixin, LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_user_url'] = reverse_lazy('user-create')
        return context


class UserDetailView(ManagerRequiredMixin, LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(CustomUser, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        organization = None
        if user.role == 'client':
            organization = user.client
        elif user.role == 'service':
            organization = user.service_organization

        fields = [
            ('Имя', user.first_name),
            ('Фамилия', user.last_name),
            ('Email', user.email),
            ('Username', user.username),
            ('Роль', user.role),
            ('Организация', organization),
        ]

        context['fields'] = fields
        context['back_to_list_url'] = reverse('users-list')
        return context


class UserUpdateView(ManagerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user_update.html'

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.object.pk})


class UserDeleteView(ManagerRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('users-list')


class MachineSearchView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        form = MachineSearchForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MachineSearchForm(request.POST)
        if form.is_valid():
            serial_number = form.cleaned_data['serial_number']
            try:
                machine = Machine.objects.get(serial_number=serial_number)
                return redirect('machine-detail', pk=machine.pk)
            except Machine.DoesNotExist:
                form.add_error('serial_number', 'Машина с таким заводским номером не найдена')
        return render(request, self.template_name, {'form': form})


class ReferenceEntityListView(ManagerRequiredMixin, ListView):
    model = ReferenceEntity
    template_name = 'reference_entity_list.html'
    context_object_name = 'entities'


class ReferenceListView(ManagerRequiredMixin, ListView):
    model = Reference
    template_name = 'reference_list.html'
    context_object_name = 'references'

    def get_queryset(self):
        self.entity = get_object_or_404(ReferenceEntity, pk=self.kwargs['entity_id'])
        return Reference.objects.filter(entity=self.entity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = self.entity
        return context


class ReferenceDetailView(ManagerRequiredMixin, DetailView):
    model = Reference
    template_name = 'reference_detail.html'
    context_object_name = 'reference'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = self.object.entity
        return context


class ReferenceCreateView(ManagerRequiredMixin, CreateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'reference_create.html'

    def form_valid(self, form):
        form.instance.entity = get_object_or_404(ReferenceEntity, pk=self.kwargs['entity_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reference_list', kwargs={'entity_id': self.kwargs['entity_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity_id'] = self.kwargs['entity_id']
        return context


class ReferenceUpdateView(ManagerRequiredMixin, UpdateView):
    model = Reference
    form_class = ReferenceForm
    template_name = 'reference_update.html'

    def get_success_url(self):
        return reverse_lazy('reference_list', kwargs={'entity_id': self.object.entity.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class ReferenceDeleteView(View):
    def post(self, request, pk):
        reference = get_object_or_404(Reference, pk=pk)
        entity_id = reference.entity.id
        reference.delete()
        return redirect('reference_list', entity_id=entity_id)

