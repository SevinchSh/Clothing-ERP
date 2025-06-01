from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erp_app.models import *
from decimal import Decimal
import random
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **options):
        self.stdout.write('Creating dummy data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (username: admin, password: admin123)')

        # Create categories
        categories_data = [
            {'name': 'Men', 'description': 'Men clothing'},
            {'name': 'Women', 'description': 'Women clothing'},
            {'name': 'Kids', 'description': 'Kids clothing'},
            {'name': 'Accessories', 'description': 'Fashion accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            {
                'name': 'Cotton T-Shirt',
                'sku': 'CT001',
                'category': 'Men',
                'price': Decimal('25.99'),
                'stock_quantity': 150,
                'size': 'M',
                'color': 'Blue',
                'fabric': 'cotton',
                'status': 'in_stock',
                'min_stock_level': 20
            },
            {
                'name': 'Denim Jeans',
                'sku': 'DJ002',
                'category': 'Women',
                'price': Decimal('79.99'),
                'stock_quantity': 8,
                'size': 'L',
                'color': 'Dark Blue',
                'fabric': 'denim',
                'status': 'low_stock',
                'min_stock_level': 15
            },
            {
                'name': 'Kids Hoodie',
                'sku': 'KH003',
                'category': 'Kids',
                'price': Decimal('35.99'),
                'stock_quantity': 0,
                'size': 'S',
                'color': 'Red',
                'fabric': 'cotton_blend',
                'status': 'out_of_stock',
                'min_stock_level': 10
            },
            {
                'name': 'Winter Jacket',
                'sku': 'WJ004',
                'category': 'Men',
                'price': Decimal('120.00'),
                'stock_quantity': 45,
                'size': 'L',
                'color': 'Black',
                'fabric': 'polyester',
                'status': 'in_stock',
                'min_stock_level': 10
            },
            {
                'name': 'Summer Dress',
                'sku': 'SD005',
                'category': 'Women',
                'price': Decimal('59.99'),
                'stock_quantity': 30,
                'size': 'M',
                'color': 'Yellow',
                'fabric': 'cotton',
                'status': 'in_stock',
                'min_stock_level': 5
            },
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'size': prod_data['size'],
                    'color': prod_data['color'],
                    'fabric': prod_data['fabric'],
                    'status': prod_data['status'],
                    'min_stock_level': prod_data['min_stock_level']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create customers
        customers_data = [
            {
                'customer_id': 'CUST001',
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+1-555-0123',
                'location': 'New York, NY',
                'segment': 'regular',
                'total_orders': 5,
                'total_spent': Decimal('450.75')
            },
            {
                'customer_id': 'CUST002',
                'name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '+1-555-0124',
                'location': 'Los Angeles, CA',
                'segment': 'vip',
                'total_orders': 12,
                'total_spent': Decimal('1250.99')
            },
            {
                'customer_id': 'CUST003',
                'name': 'Bob Johnson',
                'email': 'bob@example.com',
                'phone': '+1-555-0125',
                'location': 'Chicago, IL',
                'segment': 'new',
                'total_orders': 2,
                'total_spent': Decimal('125.50')
            },
            {
                'customer_id': 'CUST004',
                'name': 'Sarah Williams',
                'email': 'sarah@example.com',
                'phone': '+1-555-0126',
                'location': 'Miami, FL',
                'segment': 'regular',
                'total_orders': 7,
                'total_spent': Decimal('675.25')
            },
        ]

        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                customer_id=cust_data['customer_id'],
                defaults={
                    'name': cust_data['name'],
                    'email': cust_data['email'],
                    'phone': cust_data['phone'],
                    'location': cust_data['location'],
                    'segment': cust_data['segment'],
                    'total_orders': cust_data['total_orders'],
                    'total_spent': cust_data['total_spent']
                }
            )
            if created:
                self.stdout.write(f'Created customer: {customer.name}')

        # Create inventory records
        products = Product.objects.all()
        locations = ['Warehouse A', 'Warehouse B', 'Store Front']

        for product in products:
            for location in locations[:2]:  # Only create for 2 locations
                reserved = random.randint(0, 10)
                inventory, created = Inventory.objects.get_or_create(
                    product=product,
                    location=location,
                    defaults={
                        'quantity': product.stock_quantity,
                        'reserved': reserved,
                        'available': product.stock_quantity - reserved,
                        'min_level': product.min_stock_level
                    }
                )
                if created:
                    self.stdout.write(f'Created inventory: {product.name} at {location}')

        # Create orders
        customers = Customer.objects.all()
        products = Product.objects.all()

        order_statuses = ['pending', 'processing', 'shipped', 'delivered']

        for i in range(1, 6):
            customer = random.choice(customers)
            status = random.choice(order_statuses)

            order, created = Order.objects.get_or_create(
                order_id=f'ORD00{i}',
                defaults={
                    'customer': customer,
                    'total_amount': Decimal(random.uniform(50, 500)),
                    'status': status,
                    'created_at': timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                }
            )

            if created:
                # Create order items
                num_items = random.randint(1, 3)
                for _ in range(num_items):
                    product = random.choice(products)
                    quantity = random.randint(1, 5)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                self.stdout.write(f'Created order: {order.order_id} with {num_items} items')

        # Create notifications
        notifications_data = [
            {
                'title': 'Low Stock Alert',
                'message': 'Denim Jeans (DJ002) is running low in Warehouse B - only 6 units left',
                'notification_type': 'low_stock',
                'priority': 'high',
                'is_read': False,
                'created_at': timezone.now() - timezone.timedelta(minutes=47)
            },
            {
                'title': 'New Order Received',
                'message': 'Order #ORD005 received from John Smith - $125.99',
                'notification_type': 'new_order',
                'priority': 'medium',
                'is_read': False,
                'created_at': timezone.now() - timezone.timedelta(hours=2)
            },
            {
                'title': 'System Update',
                'message': 'System will be down for maintenance on Sunday at 2 AM',
                'notification_type': 'system',
                'priority': 'low',
                'is_read': True,
                'created_at': timezone.now() - timezone.timedelta(days=1)
            },
        ]

        for notif_data in notifications_data:
            notification, created = Notification.objects.get_or_create(
                title=notif_data['title'],
                defaults={
                    'message': notif_data['message'],
                    'notification_type': notif_data['notification_type'],
                    'priority': notif_data['priority'],
                    'is_read': notif_data['is_read'],
                    'created_at': notif_data['created_at']
                }
            )
            if created:
                self.stdout.write(f'Created notification: {notification.title}')

        # Create user profiles
        users_data = [
            {
                'username': 'manager',
                'email': 'manager@example.com',
                'password': 'manager123',
                'role': 'manager',
                'is_active': True
            },
            {
                'username': 'staff',
                'email': 'staff@example.com',
                'password': 'staff123',
                'role': 'warehouse_staff',
                'is_active': True
            }
        ]

        # Create admin profile if it doesn't exist
        admin_user = User.objects.get(username='admin')
        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'role': 'admin',
                'is_active': True,
                'last_login_time': timezone.now() - timezone.timedelta(minutes=48)
            }
        )

        # Create other users
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_active': user_data['is_active']
                }
            )

            if created:
                user.set_password(user_data['password'])
                user.save()

                UserProfile.objects.create(
                    user=user,
                    role=user_data['role'],
                    is_active=user_data['is_active'],
                    last_login_time=timezone.now() - timezone.timedelta(hours=random.randint(1, 24))
                )

                self.stdout.write(f'Created user: {user.username} with role {user_data["role"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with dummy data!'))