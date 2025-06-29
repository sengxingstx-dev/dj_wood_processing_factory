from django.db import models

from accounts.models import Account, Client, Employee
from common.models import BaseModel
from core.utils import wood_inventory_storage


class WoodInventory(BaseModel):
    WOOD_TYPE_CHOICES = [
        ("ໄມ້ສັກ", "ໄມ່ສັກ"),
        ("ໄມ້ດູ່", "ໄມ້ດູ່"),
        ("ໄມ້ປັກເກ້", "ໄມ້ປັກເກ້"),
        ("ໄມ້ບົວ", "ໄມ້ບົວ"),
    ]

    GRADE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    ]

    STATUS_CHOICES = [
        ("Available", "ຫວ່າງ"),
        ("Reserved", "ຈອງ"),
        ("Processed", "ດຳເນິນການແລ້ວ"),
    ]

    image = models.ImageField(upload_to=wood_inventory_storage, null=True, blank=True)
    wood_type = models.CharField(max_length=50, choices=WOOD_TYPE_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)  # Cost per unit
    source = models.CharField(max_length=100)  # Supplier or origin
    arrival_date = models.DateField()  # Stock arrival date
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.wood_type} - {self.grade} - {self.status}"


class ProcessingUnit(BaseModel):
    STATUS_CHOICES = [
        ("Active", "ໃຊ້ງານ"),
        ("Maintenance", "ບຳລຸງຮັກສາ"),
        ("Idle", "ບໍໄດ້ໃຊ້ງານ"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name}"


class ProductionLog(BaseModel):
    STATUS_CHOICES = [
        ("Completed", "ສຳເລັດແລ້ວ"),
        ("In-Progress", "ກຳລັງດຳເນີນການ"),
        ("Faulty", "ລົ້ມເຫຼວ"),
    ]

    wood_inventory = models.ForeignKey(
        "WoodInventory", on_delete=models.CASCADE, related_name="production_logs_wood_inventory"
    )
    quantity_processed = models.IntegerField(default=0)
    processing_unit = models.ForeignKey(
        "ProcessingUnit", on_delete=models.CASCADE, related_name="production_logs_processing_unit"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, related_name="production_logs_emp"
    )
    processing_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True, null=True)  # Additional notes

    def __str__(self):
        return f"Log {self.id} - {self.status}"


class Machinery(BaseModel):
    STATUS_CHOICES = [
        ("Operational", "ພ້ອມໃຊ້ງານ"),
        ("Maintenance", "ບຳລຸງຮັກສາ"),
        ("Non-functional", "ໃຊ້ງານບໍໄດ້"),
    ]

    name = models.CharField(max_length=100)
    processing_unit = models.ForeignKey(
        "ProcessingUnit", on_delete=models.CASCADE, related_name="machineries"
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    purchase_date = models.DateField()
    last_maintenance_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Order(BaseModel):
    class OrderStatus(models.TextChoices):
        PENDING = "pending"
        COMPLETED = "completed"
        CANCELLED = "cancelled"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Cash"
        TRANSFERRED = "transferred", "Transferred"

    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="user_orders",
        null=True,
        blank=True,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="client_orders",
        null=True,
        blank=True,
    )
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.order_number}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    wood_inventory = models.ForeignKey(WoodInventory, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"{self.order} ordered for {self.wood_inventory}"
