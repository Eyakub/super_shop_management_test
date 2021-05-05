from django.db import models

# Create your models here.

class Category:
    ELECTRONIC_DEVICES = 'electronic_devices'
    FOOD = 'food'
    HOME_APPLIANCES = 'home_appliances'
    GROCERIES = 'groceries'
    MENS_FASHION = "mens_Fashion"
    WOMENS_FASHION = "women_fashion"

    category_list = [
        (ELECTRONIC_DEVICES, 'Electronic Devices'),
        (FOOD, 'Food'),
        (HOME_APPLIANCES, 'Home Appliances'),
        (GROCERIES, 'Groceries'),
        (MENS_FASHION, "Men's Fashion"),
        (WOMENS_FASHION, "Women's Fashion")
    ]


class OrderStatus:
    PENDING = 'pending'
    DELIVERED = 'delivered'

    order_status_list = [
        (PENDING, 'Pending'),
        (DELIVERED, 'Delivered'),
    ]


class Product(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    code = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=256, 
        choices=Category.category_list, default=Category.FOOD, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    current_stock = models.IntegerField()

    def __str__(self):
        return f"{self.name}-{self.category}"


class Order(models.Model):
    customer_name = models.CharField(max_length=256, null=True)
    customer_phone = models.CharField(max_length=256, null=True)
    customer_email = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=256, 
        choices=OrderStatus.order_status_list, default=OrderStatus.PENDING)
    total = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.status}-{self.total}"


class OrderLine(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    order = models.ForeignKey(Order, blank=True, null=True, 
        related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, 
        related_name="order_line", on_delete=models.SET_NULL)
    total_unit = models.IntegerField()
    total_price = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.name}-{self.total_unit}-{self.total_price}"
