
from django.urls import path
from .views import (
    MachineListView,
    MachineDetailView,
    MaintenanceListView,
    MaintenanceDetailView,
    ClaimListView,
    ClaimDetailView,
    MachineCreateView,
    MaintenanceCreateView,
    ClaimCreateView, UserCreateView, MachineSearchView, ReferenceListView, ReferenceUpdateView, ReferenceDeleteView,
    ReferenceCreateView, ReferenceEntityListView, ReferenceDetailView, MachineUpdateView, MachineDeleteView,
    MaintenanceUpdateView, MaintenanceDeleteView, ClaimUpdateView, ClaimDeleteView, UsersListView, ManagerView,
    UserDetailView, UserUpdateView, UserDeleteView
)

urlpatterns = [
    path('home/', MachineSearchView.as_view(), name='machine_search'),
    path('machines/', MachineListView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('machines/<int:pk>/edit/', MachineUpdateView.as_view(), name='machine_edit'),
    path('machines/<int:pk>/delete/', MachineDeleteView.as_view(), name='machine_delete'),
    path('machines/new/', MachineCreateView.as_view(), name='machine-create'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenance-list'),
    path('maintenances/<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance-detail'),
    path('maintenances/<int:pk>/edit/', MaintenanceUpdateView.as_view(), name='maintenance_edit'),
    path('maintenances/<int:pk>/delete/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('maintenances/new/', MaintenanceCreateView.as_view(), name='maintenance-create'),
    path('claims/', ClaimListView.as_view(), name='claim-list'),
    path('claims/<int:pk>/', ClaimDetailView.as_view(), name='claim-detail'),
    path('claims/new/', ClaimCreateView.as_view(), name='claim-create'),
    path('claims/<int:pk>/edit/', ClaimUpdateView.as_view(), name='claim_edit'),
    path('claims/<int:pk>/delete/', ClaimDeleteView.as_view(), name='claim_delete'),
    path('manager', ManagerView.as_view(), name='manager'),
    path('client/new/', UserCreateView.as_view(), name='user-create'),
    path('clients/', UsersListView.as_view(), name='users-list'),
    path('clients/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('clients/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('clients/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('reference/', ReferenceEntityListView.as_view(), name='reference_entity_list'),
    path('reference/<int:entity_id>/', ReferenceListView.as_view(), name='reference_list'),
    path('reference/detail/<int:pk>/', ReferenceDetailView.as_view(), name='reference_detail'),
    path('reference/<int:entity_id>/create/', ReferenceCreateView.as_view(), name='reference_create'),
    path('reference/update/<int:pk>/', ReferenceUpdateView.as_view(), name='reference_update'),
    path('reference/delete/<int:pk>/', ReferenceDeleteView.as_view(), name='reference_delete'),

]
