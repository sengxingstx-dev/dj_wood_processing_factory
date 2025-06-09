import random

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from faker import Faker

from accounts.models import Account, Client, Employee
from common.utils import generate_unique_identifier
from core.models import (
    Machinery,
    Order,
    OrderDetail,
    ProcessingUnit,
    ProductionLog,
    WoodInventory,
)

fake = Faker()


class Command(BaseCommand):
    help = "Seeds the database with initial data for the Wood Processing Factory"

    def handle(self, *args, **options):
        self.stdout.write("Starting to seed data...")

        # Clean up existing data (optional, but good for repeatable seeding)
        self.stdout.write("Deleting existing data...")
        OrderDetail.objects.all().delete()
        Order.objects.all().delete()
        ProductionLog.objects.all().delete()
        Machinery.objects.all().delete()
        ProcessingUnit.objects.all().delete()
        WoodInventory.objects.all().delete()
        Employee.objects.all().delete()
        Client.objects.all().delete()
        Account.objects.filter(
            is_superuser=False
        ).delete()  # Keep superuser if exists, or create one
        self.stdout.write("Existing data deleted.")

        # --- Create Accounts ---
        self.stdout.write("Creating Accounts...")
        admin_user, created = Account.objects.get_or_create(
            email="admin@gmail.com",
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "password": make_password("passwd1234"),
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_user.email}"))
        else:
            admin_user.set_password("passwd1234")  # Ensure password is set if user already exists
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(
                self.style.WARNING(
                    f"Admin user {admin_user.email} already exists. Password reset and permissions ensured."
                )
            )

        users = []
        for i in range(10):
            user = Account.objects.create(
                email=fake.unique.email(),
                password=make_password("passwd1234"),
                is_active=random.choice([True, True, False]),
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"{len(users)} regular users created."))

        # --- Create Employees ---
        self.stdout.write("Creating Employees...")
        employees = []
        for i in range(5):
            employee_user = users.pop() if users else None  # Assign a user if available
            employee = Employee.objects.create(
                name=fake.name(),
                contact_number=fake.phone_number()[:20],
                date_hired=fake.date_between(start_date="-3y", end_date="today"),
                user=employee_user,
            )
            employees.append(employee)
        self.stdout.write(self.style.SUCCESS(f"{len(employees)} employees created."))

        # --- Create Clients ---
        self.stdout.write("Creating Clients...")
        clients = []
        for i in range(8):
            # client_user = users.pop() if users else None  # Assign a user if available
            client = Client.objects.create(
                name=fake.company() if random.choice([True, False]) else fake.name(),
                contact_number=fake.phone_number()[:20],
                address=fake.address(),
                # user=client_user,
            )
            clients.append(client)
        self.stdout.write(self.style.SUCCESS(f"{len(clients)} clients created."))

        # --- Create Wood Inventories ---
        self.stdout.write("Creating Wood Inventories...")
        wood_inventories = []
        for _ in range(20):
            wood = WoodInventory.objects.create(
                wood_type=random.choice([choice[0] for choice in WoodInventory.WOOD_TYPE_CHOICES]),
                grade=random.choice([choice[0] for choice in WoodInventory.GRADE_CHOICES]),
                # quantity=round(random.uniform(5.0, 100.0), 2), # with decimal points
                quantity=round(random.randint(5, 100)),
                unit_price=round(random.uniform(500000, 5000000), 2),
                source=fake.company(),
                arrival_date=fake.date_between(start_date="-1y", end_date="today"),
                status=random.choice([choice[0] for choice in WoodInventory.STATUS_CHOICES]),
                # image: We'll leave this blank for simplicity
            )
            wood_inventories.append(wood)
        self.stdout.write(self.style.SUCCESS(f"{len(wood_inventories)} wood inventories created."))

        # --- Create Processing Units ---
        self.stdout.write("Creating Processing Units...")
        processing_units = []
        unit_names = [
            "Sawmill A",
            "Dry Kiln 1",
            "Sanding Station",
            "Assembly Line Alpha",
            "Finishing Bay",
        ]
        for name in unit_names:
            unit = ProcessingUnit.objects.create(
                name=name,
                description=fake.sentence(nb_words=10),
                # capacity=round(random.uniform(10.0, 50.0), 2),  # e.g., m³ per day
                capacity=round(random.randint(5, 100)),  # e.g., m³ per day
                status=random.choice([choice[0] for choice in ProcessingUnit.STATUS_CHOICES]),
            )
            processing_units.append(unit)
        self.stdout.write(self.style.SUCCESS(f"{len(processing_units)} processing units created."))

        # --- Create Machineries ---
        self.stdout.write("Creating Machineries...")
        machineries = []
        if processing_units:
            for i in range(10):
                purchase_date = fake.date_between(start_date="-5y", end_date="-6m")
                machinery = Machinery.objects.create(
                    name=f"{random.choice(['Band Saw', 'Planer', 'Sander', 'CNC Router', 'Lathe'])} #{i+1}",
                    processing_unit=random.choice(processing_units),
                    description=fake.sentence(nb_words=8),
                    status=random.choice([choice[0] for choice in Machinery.STATUS_CHOICES]),
                    purchase_date=purchase_date,
                    last_maintenance_date=(
                        fake.date_between(start_date=purchase_date, end_date="today")
                        if random.choice([True, False])
                        else None
                    ),
                )
                machineries.append(machinery)
        self.stdout.write(self.style.SUCCESS(f"{len(machineries)} machineries created."))

        # --- Create Production Logs ---
        self.stdout.write("Creating Production Logs...")
        production_logs = []
        if wood_inventories and processing_units and employees:
            for _ in range(15):
                wood_item = random.choice(wood_inventories)
                if wood_item.quantity > 1:  # Ensure there's wood to process
                    qty_processed = round(random.uniform(0.5, min(wood_item.quantity, 5.0)), 2)
                    log = ProductionLog.objects.create(
                        wood_inventory=wood_item,
                        quantity_processed=qty_processed,
                        processing_unit=random.choice(processing_units),
                        employee=random.choice(employees),
                        processing_date=fake.date_between(start_date="-6m", end_date="today"),
                        status=random.choice(
                            [choice[0] for choice in ProductionLog.STATUS_CHOICES]
                        ),
                        remarks=fake.sentence() if random.choice([True, False]) else "",
                    )
                    production_logs.append(log)
                    # Update wood inventory
                    wood_item.quantity -= qty_processed
                    if wood_item.quantity <= 0:
                        wood_item.status = "Processed"
                    wood_item.save()
        self.stdout.write(self.style.SUCCESS(f"{len(production_logs)} production logs created."))

        # --- Create Orders and OrderDetails ---
        self.stdout.write("Creating Orders and OrderDetails...")
        orders_created = []
        if clients and wood_inventories:
            all_users_with_profile = Account.objects.filter(
                Q(employee_profile__isnull=False) | Q(client_profile__isnull=False)
            ).distinct()

            for i in range(10):  # Create 10 orders
                order_client = random.choice(clients)
                order_user = (
                    random.choice(all_users_with_profile) if all_users_with_profile else admin_user
                )

                order_date_obj = timezone.make_aware(
                    fake.date_time_between(start_date="-3m", end_date="now")
                )

                order = Order.objects.create(
                    order_number=f'ORD-{order_date_obj.strftime("%Y%m%d")}-{generate_unique_identifier()}',
                    user=order_user,
                    client=order_client,
                    order_date=order_date_obj,
                    status=random.choice([choice[0] for choice in Order.OrderStatus.choices]),
                    payment_method=random.choice(
                        [choice[0] for choice in Order.PaymentMethod.choices]
                    ),
                    description=fake.sentence(nb_words=5) if random.choice([True, False]) else "",
                )

                total_order_cost = 0
                num_order_items = random.randint(1, 3)

                available_woods_for_order = [
                    w for w in wood_inventories if w.quantity > 0.1 and w.status == "Available"
                ]

                for _ in range(num_order_items):
                    if not available_woods_for_order:
                        break

                    wood_for_detail = random.choice(available_woods_for_order)

                    if wood_for_detail.quantity > 0.1:
                        qty_ordered = random.randint(
                            1, int(min(wood_for_detail.quantity, 5))
                        )  # Order between 1 and 5, or available stock
                        price_per_unit = wood_for_detail.unit_price  # Use current unit price
                        total_price = qty_ordered * price_per_unit

                        OrderDetail.objects.create(
                            order=order,
                            wood_inventory=wood_for_detail,
                            qty=qty_ordered,
                            price_per_unit=price_per_unit,
                            total_price=total_price,
                        )
                        total_order_cost += total_price

                        # Update wood inventory
                        wood_for_detail.quantity -= qty_ordered
                        if wood_for_detail.quantity <= 0:
                            wood_for_detail.status = (
                                "Reserved"  # Or "Processed" if order is completed
                            )
                        wood_for_detail.save()

                        # Remove wood if depleted or update its entry in available_woods_for_order
                        if wood_for_detail.quantity <= 0.1:
                            available_woods_for_order = [
                                w
                                for w in available_woods_for_order
                                if w.id != wood_for_detail.id or w.quantity > 0.1
                            ]

                order.total_cost = total_order_cost
                order.save()
                orders_created.append(order)
        self.stdout.write(self.style.SUCCESS(f"{len(orders_created)} orders with details created."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
