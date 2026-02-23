from django.db import models

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class KSRTCRoute(models.Model):
    route_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return self.route_name


class KSRTCStation(models.Model):
    station_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    route = models.ForeignKey(KSRTCRoute, on_delete=models.CASCADE, related_name="stations")

    def __str__(self):
        return self.station_name


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    approval_status = models.BooleanField(default=False)
    station = models.ForeignKey(KSRTCStation, on_delete=models.CASCADE, related_name="restaurants")

    def __str__(self):
        return self.restaurant_name
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.IntegerField()  # in minutes
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.item_name


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PLACED', 'Placed'),
        ('ACCEPTED', 'Accepted'),
        ('PREPARING', 'Preparing'),
        ('READY', 'Ready'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="orders")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="orders")
    station = models.ForeignKey(KSRTCStation, on_delete=models.CASCADE, related_name="orders")
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PLACED')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id}"


class OrderMenuItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.item_name} x {self.quantity}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('WALLET', 'Wallet'),
    ]

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=30)
    payment_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class Refund(models.Model):
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_status = models.CharField(max_length=30)
    refund_time = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="refunds")

    def __str__(self):
        return f"Refund #{self.id}"


class Review(models.Model):
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="reviews")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"Review #{self.id}"


class PreOrderSchedule(models.Model):
    scheduled_order_time = models.DateTimeField()
    estimated_arrival_time = models.DateTimeField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="preorder_schedules")

    def __str__(self):
        return f"PreOrder for Order #{self.order.id}"


class GPSSession(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="gps_sessions")

    def __str__(self):
        return f"GPS Session for Order #{self.order.id}"


class ChatMessage(models.Model):
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_type = models.CharField(max_length=20)  # 'PASSENGER' or 'RESTAURANT'
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="chat_messages")

    def __str__(self):
        return f"Message #{self.id}"
