# -*- coding: utf-8 -*-

# Python
from functools import reduce
from datetime import datetime

# Third
from mongoengine.errors import NotUniqueError, ValidationError
from mongoengine.errors import MultipleObjectsReturned, DoesNotExist


# Apps
from shopping_cart.sentry import sentry
from shopping_cart.messages import _MSG300
from shopping_cart.responses import resp_already_exists, resp_exception
from .models import Cart, Supplier, Variant, Image, Item


def create_cart(suppliers=None, products=None):
    '''
    Create cart with suppliers and products data if exists
    '''
    cart = Cart()

    if suppliers is None and products is None:
        return cart.save()

    supplier = create_supplier(suppliers)

    if supplier and products:
        try:
            product = create_product(products)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        subtotal, total = calculate_product_price(product)
        product.total = total
        product.subtotal = subtotal

        supplier.items.append(product)

    try:
        cart.suppliers.append(supplier)

    except Exception as e:
        sentry.captureException()

        return resp_exception('Carts', description=e)

    subtotal, total = calculate_total_and_subtotal(supplier.items)
    supplier.subtotal = subtotal
    supplier.total = total

    subtotal, total = calculate_total_and_subtotal(cart.suppliers)
    cart.subtotal = subtotal
    cart.total = total

    try:
        cart.updated = datetime.now()
        cart.save()

    except NotUniqueError:
        sentry.captureException()

        return resp_already_exists('Carts', 'carrinho')

    except ValidationError as e:
        sentry.captureException()

        return resp_exception('Carts', msg=_MSG300, description=e)

    except Exception as e:
        sentry.captureException()

        return resp_exception('Carts', description=e)

    return cart


def merge_carts():
    '''
    Merge de carrinho de compras caso existam compradores iguais user_id
    '''
    pass


def create_supplier(supplier):
    '''
    Adiciona o fornecedor
    '''
    if supplier:
        sup = Supplier(**supplier)
    else:
        sup = None

    return sup


def create_variant(data):
    '''
    Adiciona a variacao escolhida no produto
    '''
    try:
        variant = Variant(**data)
    except Exception as e:
        raise e

    return variant


def create_image(data):
    '''
    Adiciona a variacao escolhida no produto
    '''
    try:
        image = Image(**data)
    except Exception as e:
        raise e

    return image


def create_sellkey(product, variant):
    '''
    SellKey {Product Id}-{Seller Id}-{Supplier Id};{qty};{price};{subtotal};{total};{Shipping Rate};{shipping Fee}-{Variant Key}-{Variant Name} # noqa
    '''
    return '{}-{}-{}-{};{};{};{};{};{}-{}-{}'.format(
        product.product_id,
        product.seller_id,
        product.supplier_id,
        product.qty,
        product.price,
        product.subtotal,
        product.total,
        product.ship_flat_rate,
        product.shipping_fee,
        variant.key,
        variant.name
    )


def create_product(item):
    '''
    Adiciona produto no carrinho
    '''

    # TODO: Tratar variacao

    if 'variant' in item:
        try:
            variant = create_variant(item.get('variant', None))
        except Exception as e:
            raise e

    # TODO: Tratar Image

    if 'image' in item:
        try:
            image = create_image(item.get('image', None))
        except Exception as e:
            raise e

    # TODO: Criar Produto

    del item['image']
    del item['variant']

    try:
        product = Item(variant=variant, image=image, **item)
        product.key = create_sellkey(product, variant)
    except Exception as e:
        raise e

    return product


def get_supplier_by_id(suppliers, id):
    '''
    Return a supplier by id
    '''

    try:
        return suppliers.get(supplier_id=id)

    except NotUniqueError:
        sentry.captureException()

        return resp_already_exists('Carts', 'carrinho')

    except DoesNotExist:
        return None

    except ValidationError as e:
        sentry.captureException()

        return resp_exception('Carts', msg=_MSG300, description=e)

    except MultipleObjectsReturned as e:
        sentry.captureException()

        return resp_exception('Carts', msg=_MSG300, description=e)

    except Exception as e:
        sentry.captureException()

        return resp_exception('Carts', description=e)


def get_product_by_id(items, id):
    '''
    Return a supplier by id
    '''

    try:
        return items.get(product_id=id)

    except NotUniqueError:
        sentry.captureException()

        return resp_already_exists('Carts', 'carrinho')

    except DoesNotExist:
        return None

    except ValidationError as e:
        sentry.captureException()

        return resp_exception('Carts', msg=_MSG300, description=e)

    except MultipleObjectsReturned as e:
        sentry.captureException()

        return resp_exception('Carts', msg=_MSG300, description=e)

    except Exception as e:
        sentry.captureException()

        return resp_exception('Carts', description=e)


def calculate_product_price(product):
    '''
    Calculo do preços de cada item
    '''
    if product.qty <= 0:
        raise ValueError('A quantidade não pode ser menor que zero.')

    subtotal = product.qty * product.price
    total = subtotal - product.discount_price

    if product.ship_flat_rate:
        total -= product.shipping_fee

    return subtotal, total


def calculate_total_and_subtotal(model):
    '''
    TODO: refact with calculate_supplier_total_and_subtotal
    Calculate Total
    '''
    subtotal, total = 0, 0

    if len(model) > 1:
        subtotal = reduce(
            lambda x, y: x.subtotal + y.subtotal, model
        )
    elif len(model) == 1:
        subtotal = model[0].subtotal
    else:
        subtotal = 0

    if len(model) > 1:
        total = reduce(
            lambda x, y: x.total + y.total, model
        )
    elif len(model) == 1:
        total = model[0].total
    else:
        total = 0

    return subtotal, total
