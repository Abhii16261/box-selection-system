from django.db import models


class Product(models.Model):
    """A physical product that can be ordered."""
    name = models.CharField(max_length=255)
    length_cm = models.DecimalField(max_digits=6, decimal_places=2)
    width_cm = models.DecimalField(max_digits=6, decimal_places=2)
    height_cm = models.DecimalField(max_digits=6, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def volume_cm3(self):
        return self.length_cm * self.width_cm * self.height_cm


class Box(models.Model):
    """A shipping box the warehouse can pack an order into."""
    name = models.CharField(max_length=255)
    internal_length_cm = models.DecimalField(max_digits=6, decimal_places=2)
    internal_width_cm = models.DecimalField(max_digits=6, decimal_places=2)
    internal_height_cm = models.DecimalField(max_digits=6, decimal_places=2)
    max_weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    @property
    def volume_cm3(self):
        return self.internal_length_cm * self.internal_width_cm * self.internal_height_cm


class Order(models.Model):
    """A customer order — a collection of products to be shipped together."""
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderItem")

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """A line item: how many of a given product are in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"