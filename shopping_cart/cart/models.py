# -*- coding: utf-8 -*-
from datetime import datetime


from mongoengine import IntField, EmbeddedDocument, BooleanField
from mongoengine import DynamicEmbeddedDocument, EmbeddedDocumentField
from mongoengine import EmbeddedDocumentListField
from mongoengine import StringField, DateTimeField

# Apps
from shopping_cart.db import db


class Image(EmbeddedDocument):
    '''
    Main image
    '''
    url = StringField(required=True)
    title = StringField(required=True)


class Variant(EmbeddedDocument):
    '''
    Variant
    '''
    key = StringField(required=True)
    name = StringField(required=True)
    price = IntField(default=0)
    quantity = IntField(default=0)


class Item(EmbeddedDocument):
    '''
    Info item
    '''
    key = StringField(required=True)
    product_id = StringField(required=True, default='')
    similar_product_id = StringField(default='')
    seller_id = StringField(required_id=True, default='')
    supplier_id = StringField(required=True, default='')
    qty = IntField(default=1)
    name = StringField(required=True, default='')
    discount_price = IntField(default=0)
    price = IntField(required=True, default=0)
    subtotal = IntField(default=0)
    total = IntField(default=0)
    variant = EmbeddedDocumentField(Variant, default=Variant)
    image = EmbeddedDocumentField(Image, default=Image)
    ship_flat_rate = IntField(default=0)
    shipping_fee = IntField(default=0)


class Supplier(DynamicEmbeddedDocument):
    '''
    Undefined number of suppliers that will be in this object
    '''
    items = EmbeddedDocumentListField(Item, default=[])


class Cart(db.Document):
    '''
    Users are Buyers or merchants
    '''
    meta = {'collection': 'carts'}

    user_id = StringField(default='')
    user_email = StringField(default='')
    qty = IntField(default=0)
    subtotal = IntField(default=0)
    total = IntField(default=0)
    shipping_total = IntField(default=0)
    expired = BooleanField(default=False)
    date_expired = DateTimeField(default=datetime.now)
    created = DateTimeField(default=datetime.now)
    updated = DateTimeField(default=datetime.now)

    suppliers = EmbeddedDocumentListField(Supplier, default=[])
