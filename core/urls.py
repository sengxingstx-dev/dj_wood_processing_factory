from django.conf.urls import handler404
from django.urls import include, path

from . import views as core_views

handler404 = core_views.custom_404_view

urlpatterns = [
    path("", core_views.home, name="home"),
    path("about/", core_views.about, name="about"),
    path("contact/", core_views.contact, name="contact"),
    # Dashboard
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("dashboard/profile", core_views.manage_profile, name="manage-profile"),
    path("dashboard/manage-users/", core_views.manage_users, name="manage-users"),
    path("dashboard/manage-users/delete/<int:pk>/", core_views.delete_user, name="delete-user"),
    # Employees
    path("dashboard/manage-employees/", core_views.manage_employees, name="manage-employees"),
    path(
        "dashboard/manage-employees/edit/<int:pk>/", core_views.edit_employee, name="edit-employee"
    ),
    path(
        "dashboard/manage-employees/delete/<int:pk>/",
        core_views.delete_employee,
        name="delete-employee",
    ),
    # Clients
    path("dashboard/manage-clients/", core_views.manage_clients, name="manage-clients"),
    path("dashboard/manage-clients/edit/<int:pk>/", core_views.edit_client, name="edit-client"),
    path(
        "dashboard/manage-clients/delete/<int:pk>/",
        core_views.delete_client,
        name="delete-client",
    ),
    # Wood inventories
    path(
        "dashboard/manage-wood-inventories/",
        core_views.manage_wood_inventories,
        name="manage-wood-inventories",
    ),
    path(
        "dashboard/manage-wood-inventories/edit/<int:pk>/",
        core_views.edit_wood_inventory,
        name="edit-wood-inventory",
    ),
    path(
        "dashboard/manage-wood-inventories/delete/<int:pk>/",
        core_views.delete_wood_inventory,
        name="delete-wood-inventory",
    ),
    # Processing Units
    path(
        "dashboard/manage-processing-units/",
        core_views.manage_processing_units,
        name="manage-processing-units",
    ),
    path(
        "dashboard/manage-processing-units/edit/<int:pk>/",
        core_views.edit_processing_unit,
        name="edit-processing-unit",
    ),
    path(
        "dashboard/manage-processing-units/delete/<int:pk>/",
        core_views.delete_processing_unit,
        name="delete-processing-unit",
    ),
    # Production Logs
    path(
        "dashboard/manage-production-logs/",
        core_views.manage_production_logs,
        name="manage-production-logs",
    ),
    path(
        "dashboard/manage-production-log/edit/<int:pk>/",
        core_views.edit_production_log,
        name="edit-production-log",
    ),
    path(
        "dashboard/manage-production-log/delete/<int:pk>/",
        core_views.delete_production_log,
        name="delete-production-log",
    ),
    # Machineries
    path(
        "dashboard/manage-machineries/",
        core_views.manage_machineries,
        name="manage-machineries",
    ),
    path(
        "dashboard/manage-machineries/edit/<int:pk>/",
        core_views.edit_machinery,
        name="edit-machinery",
    ),
    path(
        "dashboard/manage-machineries/delete/<int:pk>/",
        core_views.delete_machinery,
        name="delete-machinery",
    ),
    # Orders
    path("manage-orders/", core_views.manage_orders, name="manage-orders"),
    path("orders/view/<int:pk>/", core_views.view_order, name="view-order"),
    path("edit-order/<int:pk>/", core_views.edit_order, name="edit-order"),
    path("delete-order/<int:pk>/", core_views.delete_order, name="delete-order"),
    path(
        "generate-order-pdf/<int:order_id>/",
        core_views.generate_order_pdf,
        name="generate_order_pdf",
    ),
    #
    path("dashboard/manage-products/", core_views.manage_products, name="manage-products"),
    path("accounts/", include("accounts.urls")),
]
