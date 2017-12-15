# -*- coding: utf-8 -*-


def cart_detail(cart):
    '''
    Return cart data
    '''
    # TODO valid cart param

    data = {
        'id': '{}'.format(cart.id),
        'user_id': cart.user_id,
        'user_email': cart.user_email,
        'qty': cart.qty,
        'subtotal': cart.subtotal,
        'total': cart.total,
        'shipping_total': cart.shipping_total,
        'suppliers': []
    }

    return data


def supplier_detail(supplier):
    '''
    Return supplier data
    '''
    # TODO valid supplier param

    sup = {
        'id': '{}'.format(supplier.supplier_id),
        'ship_flat_rate': supplier.ship_flat_rate,
        'shipping_fee': supplier.shipping_fee,
        'subtotal': supplier.subtotal,
        'total': supplier.total,
        'items': []
    }

    for item in supplier.items:
        sup['items'].append(product_detail(item))

    return sup


def product_detail(product):
    '''
    Return item data
    '''
    item = {
        'product_id': product.product_id,
        'similar_product_id': product.similar_product_id,
        'seller_id': product.seller_id,
        'supplier_id': product.supplier_id,
        'qty': product.qty,
        'name': product.name,
        'discount_price': product.discount_price,
        'price': product.price,
        'subtotal': product.subtotal,
        'total': product.total,
        'ship_flat_rate': product.ship_flat_rate,
        'shipping_fee': product.shipping_fee
    }

    if product.variant:
        item['variant'] = variant_detail(product.variant)
    else:
        item['variant'] = {}

    if product.image:
        item['image'] = image_detail(product.image)
    else:
        item['image'] = {}

    return item


def variant_detail(data):
    '''
    Return dict of Variant Model
    '''
    return {
        'key': data.key,
        'name': data.name,
        'price': data.price,
        'quantity': data.quantity
    }


def image_detail(data):
    '''
    return dict of Image
    '''
    return {
        'url': data.url,
        'title': data.title
    }
