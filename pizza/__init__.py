from django.utils.translation import npgettext_lazy, pgettext_lazy



class OrderStatus:
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    ON_DELIVERY = "on_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


    CHOICES = [
        (DRAFT, pgettext_lazy('Status for a fully editable, not confirmed', 'Draft')),
        (CONFIRMED, pgettext_lazy('Status for an order is ready to start preparation', 'Confirmed')),
        (PREPARING, pgettext_lazy('Status for an order is preparing', 'Preparing')),
        (ON_DELIVERY, pgettext_lazy('Status for an order is delivering at the moment', 'On Delivery')),
        (DELIVERED, pgettext_lazy('Status for an order is delivered successfully', 'Delivered')),
        (CANCELLED, pgettext_lazy('Status for an order is cancelled', 'Cancelled'))
    ]