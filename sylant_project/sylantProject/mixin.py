from django.http import HttpResponseForbidden, Http404


class RoleRequiredMixin:

    @staticmethod
    def test_func(user, allowed_roles):
        return user.role in allowed_roles

    def dispatch(self, request, *args, **kwargs):
        allowed_roles = getattr(self, 'allowed_roles', [])
        if request.user.is_authenticated:
            if not self.test_func(request.user, allowed_roles):
                return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['manager']


class ManagerServiceRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['manager', 'service']


class ClientServiceManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['client', 'service', 'manager']


class RoleBasedObjectMixin:
    def get_role_based_object(self, obj):
        user = self.request.user
        if user.role == 'manager':
            return obj
        elif user.role == 'client' and obj.machine.client == user.client:
            return obj
        elif user.role == 'service' and obj.service_company == user.service_organization:
            return obj
        else:
            raise Http404("Вы не имеете доступа к этой информации")
