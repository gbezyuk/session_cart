"""
Session based shopping cart
"""
from django.core.exceptions import ImproperlyConfigured

class CartItem(object):
    """
    Lightweight container for cart items
    """
    __slots__ = ('item', 'quantity',)

    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity and quantity or 0

    def __repr__(self):
        return 'CartItem(%r, %r)' % (self.item, self.quantity)

    def __cmp__(self, other):
        if isinstance(other, CartItem):
            return cmp(self.item, other.item)
        return cmp(self.item, other)

class Cart(list):
    """
    Handles a list of items stored in the session
    """
    model = None

    def __init__(self, request, name='cart'):
        super(Cart, self).__init__()
        self.request = request
        self.name = name
        if self.model is None:
            from django.db import models
            from django.conf import settings
            try:
                cart_app, cart_model = settings.CART_MODEL.split('.')
                Cart.model = models.get_model(cart_app, cart_model)
            except AttributeError:
                raise ImproperlyConfigured("%s isn't a valid Cart model." % settings.CART_MODEL)
        # Cart is stored as a list of ( item_id, quantity )
        for item, quantity in request.session.get(self.name, []):
            try:
                self.append(item, quantity)
            except self.model.DoesNotExist:
                pass

    def save(self):
        """
        Save this cart to the session
        """
        self.request.session[self.name] = tuple(
            (i.item.pk, i.quantity,)
            for i in self
        )

    def _get(self, item):
        """
        Ensure item is an instance of self.model
        """
        if not isinstance(item, self.model):
            return self.model._default_manager.get(pk=item)
        return item

    def append(self, item, quantity = 1):
        """
        Append some amount of item to cart
        """
        item = self._get(item)
        try:
            self[self.index(item)].quantity += quantity
        except ValueError:
            super(Cart, self).append(CartItem(item, quantity))

    def remove(self, item):
        """
        Remove single item from cart
        """
        super(Cart, self).remove(self._get(item))

    def empty(self):
        """
        Remove all items from cart
        """
        while len(self):
            self.pop()

    def __repr__( self ):
        return ','.join([repr(x) for x in self])