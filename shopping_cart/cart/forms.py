# -*- coding: utf-8 -*-

# Third
from wtforms import Form, StringField, IntegerField, FormField
from wtforms.validators import DataRequired, Optional


# Apps
from shopping_cart.messages import _MSG309
from .validate import min_qty


class ImageForm(Form):
    '''
    Validate image bject
    '''
    url = StringField('Url', [DataRequired(_MSG309)])
    title = StringField('Title', [DataRequired(_MSG309)])


class VariantForm(Form):
    '''
    Validate variant object
    '''
    key = StringField('Product', [DataRequired(_MSG309)])
    name = StringField('Name', [DataRequired(_MSG309)])
    price = IntegerField('Price', [Optional()], default=0)
    quantity = IntegerField('quantity', [DataRequired(_MSG309)])


class ItemForm(Form):
    '''
    Use this form to validate fields when create the supplier
    '''
    product_id = StringField('Product', [DataRequired(_MSG309)])
    seller_id = StringField('Seller', [DataRequired(_MSG309)])
    supplier_id = StringField('Supplier', [DataRequired(_MSG309)])
    name = StringField('Name', [DataRequired(_MSG309)])
    qty = IntegerField('Quantity', [Optional(), min_qty], default=1)
    price = IntegerField('Price', [DataRequired(_MSG309)])
    ship_flat_rate = IntegerField(
        'ship_flat_rate', [Optional(_MSG309)], default=0
    )
    shipping_fee = IntegerField(
        'shipping_fee', [Optional(_MSG309)], default=0
    )
    variant = FormField(VariantForm, [DataRequired()])
    image = FormField(ImageForm, [DataRequired()])


class SupplierForm(Form):
    '''
    Use this form to validate fields when create the supplier
    '''
    supplier_id = StringField('Supplier', [DataRequired(_MSG309)])
    ship_flat_rate = IntegerField(
        'Ship flat rate', [Optional(_MSG309)], default=0
    )
    shipping_fee = IntegerField(
        'Shipping fee', [Optional(_MSG309)], default=0
    )
    total = IntegerField(
        'Total', [Optional(_MSG309)], default=0
    )
    subtotal = IntegerField(
        'Sub total', [Optional(_MSG309)], default=0
    )
