from django.contrib import admin
from .models import (
    Passenger,
    KSRTCRoute,
    KSRTCStation,
    Restaurant,
    MenuItem,
    Order,
    OrderMenuItem,
    Payment,
    Refund,
    Review,
    PreOrderSchedule,
    GPSSession,
    ChatMessage,
)

admin.site.register(Passenger)
admin.site.register(KSRTCRoute)
admin.site.register(KSRTCStation)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderMenuItem)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Review)
admin.site.register(PreOrderSchedule)
admin.site.register(GPSSession)
admin.site.register(ChatMessage)
