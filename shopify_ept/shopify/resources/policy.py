from ..base import ShopifyResource
from ...shopify import mixins
from ... import shopify

class Policy(ShopifyResource, mixins.Metafields, mixins.Events):
  pass
