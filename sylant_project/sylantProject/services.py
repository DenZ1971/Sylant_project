from django.http import Http404

from .models import Machine


class MachineObjectService:
    @staticmethod
    def get_object(user, machine_id):
        try:
            obj = Machine.objects.get(pk=machine_id)
        except Machine.DoesNotExist:
            raise Http404("Запрошенная машина не существует")

        if user.is_authenticated:
            if user.role == 'manager':
                return obj
            elif user.role == 'client' and obj.client == user.client:
                return obj
            elif user.role == 'service' and obj.service_company == user.service_organization:
                return obj
            else:
                raise Http404("Вы не имеете доступа к этой машине")
        else:
            return obj


class ObjectAuthorizationService:
    @staticmethod
    def get_object(user, model, object_id):
        try:
            obj = model.objects.get(pk=object_id)
        except model.DoesNotExist:
            raise Http404(f"Запрошенный объект не существует")

        if user.is_authenticated:
            if user.role == 'manager':
                return obj
            elif user.role == 'client' and obj.machine.client == user.client:
                return obj
            elif user.role == 'service' and obj.service_company == user.service_organization:
                return obj
            else:
                raise Http404("У вас нет доступа к этому объекту")
        else:
            return obj


class MachineQuerysetService:
    @staticmethod
    def get_machine_queryset(user):
        if user.role == 'manager':
            return Machine.objects.all()
        elif user.role == 'client':
            return Machine.objects.filter(client=user.client)
        elif user.role == 'service':
            return Machine.objects.filter(service_company=user.service_organization)
        return Machine.objects.none()


class QuerysetService:
    @staticmethod
    def filter_queryset_by_user_role(queryset, user):
        if user.role == 'client' and user.client:
            queryset = queryset.filter(machine__client=user.client)
        elif user.role == 'service' and user.service_organization:
            queryset = queryset.filter(service_company=user.service_organization)
        elif user.role == 'manager':
            pass
        else:
            queryset = queryset.none()
        return queryset
