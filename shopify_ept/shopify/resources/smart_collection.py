from ..base import ShopifyResource
from ...shopify import mixins
from ... import shopify

class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):

    def products(self):
        return shopify.Product.find(collection_id=self.id)
