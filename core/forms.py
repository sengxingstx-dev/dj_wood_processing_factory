from django import forms

from accounts.models import Client, Employee
from core.models import (
    Machinery,
    Order,
    OrderDetail,
    ProcessingUnit,
    ProductionLog,
    WoodInventory,
)

# from django.contrib.auth.forms import UserCreationForm


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=False)
    contact_number = forms.CharField(max_length=15, required=False)
    date_hired = forms.DateField(required=False)

    class Meta:
        model = Employee
        fields = ["name", "contact_number", "date_hired"]


class ClientForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=False)
    contact_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Client
        fields = ["name", "contact_number", "address"]


class WoodInventoryForm(forms.ModelForm):
    class Meta:
        model = WoodInventory
        fields = [
            "image",
            "wood_type",
            "grade",
            "quantity",
            "unit_price",
            "source",
            "arrival_date",
            "status",
        ]


class ProcessingUnitForm(forms.ModelForm):
    class Meta:
        model = ProcessingUnit
        fields = [
            "name",
            "description",
            "capacity",
            "status",
        ]


class ProductionLogForm(forms.ModelForm):
    class Meta:
        model = ProductionLog
        fields = [
            "wood_inventory",
            "quantity_processed",
            "processing_unit",
            "employee",
            "processing_date",
            "status",
            "remarks",
        ]


class MachineryForm(forms.ModelForm):
    class Meta:
        model = Machinery
        fields = [
            "name",
            "processing_unit",
            "description",
            "status",
            "purchase_date",
            "last_maintenance_date",
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "client",
            "payment_method",
            "description",
        ]


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ["wood_inventory", "qty", "price_per_unit"]
