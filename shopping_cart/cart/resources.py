# -*- coding:utf-8 -*-

# Python
from datetime import datetime
# Flask
from flask import request

# Apps
from shopping_cart.sentry import sentry
from shopping_cart.messages import _MSG104, _MSG300
from shopping_cart.responses import resp_already_exists, resp_exception
from shopping_cart.responses import resp_form_invalid
from .models import Cart as MCart, Supplier, Item
from .utils import create_cart, get_supplier_by_id, create_supplier
from .utils import get_product_by_id, create_product, calculate_product_price
from .utils import calculate_total_and_subtotal
from .forms import SupplierForm, ItemForm
from .serializers import cart_detail, supplier_detail

# Third

from flask_restful import Resource
from mongoengine.errors import NotUniqueError, ValidationError
from mongoengine.errors import MultipleObjectsReturned


class Cart(Resource):
    def post(self, *args, **kwargs):

        supplier, supplier_data, product, product_data = None, None, None, None
        data = None

        try:
            data = request.get_json()
        except Exception:
            pass

        if data:
            supplier_data = data.get('supplier', None)
            product_data = data.get('product', None)

        if supplier_data:
            supplier_form = SupplierForm(data=supplier_data)

            if not supplier_form.validate():
                return resp_form_invalid('Carts', supplier_form.errors)

            supplier = supplier_form.data

        if product_data:
            item_form = ItemForm(data=product_data)

            if not item_form.validate():
                return resp_form_invalid('Carts', item_form.errors)

            product = item_form.data

        cart = create_cart(supplier, product)

        if not isinstance(cart, MCart):
            return cart

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

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartDetail(Resource):
    def get(self, cart_id):

        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        subtotal, total = calculate_total_and_subtotal(cart.suppliers)
        cart.subtotal = subtotal
        cart.total = total

        # TODO: Serializer all objects
        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartAddProduct(Resource):
    def put(self, cart_id):
        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        # Serializer payload request

        supplier_payload, supplier_data = None, None
        product_payload, product_data = None, None
        supplier, product = None, None
        data = None

        try:
            data = request.get_json()
        except Exception:
            return resp_form_invalid('Carts', {'product': 'not empty'})

        if data:
            supplier_data = data.get('supplier', None)
            product_data = data.get('product', None)

        if supplier_data:
            supplier_form = SupplierForm(data=supplier_data)

            if not supplier_form.validate():
                return resp_form_invalid('Carts', supplier_form.errors)

            supplier_payload = supplier_form.data

        if product_data:
            item_form = ItemForm(data=product_data)

            if not item_form.validate():
                return resp_form_invalid('Carts', item_form.errors)

            product_payload = item_form.data

        # Object Supplier EmbbedDocument if not exists

        supplier = get_supplier_by_id(
            cart.suppliers, supplier_payload.get('supplier_id')
        )

        if supplier is None:
            # Create a supplier instance
            supplier = create_supplier(supplier_payload)
            # Add on suppliers list
            try:
                # TODO: Update document with atomic update
                cart.suppliers.append(supplier)

            except Exception as e:
                sentry.captureException()

                return resp_exception('Carts', description=e)

        elif not isinstance(supplier, Supplier):
            return supplier

        # Object Item Document

        product = get_product_by_id(
            supplier.items, product_payload.get('product_id')
        )

        if product is None:
            # Create product instance
            product = create_product(product_payload)
            # Add on product list
            try:
                # TODO: Verify if the product has in stock

                # TODO: Update document with atomic update
                supplier.items.append(product)

            except Exception as e:
                sentry.captureException()

                return resp_exception('Carts', description=e)

        elif not isinstance(product, Item):
            return product
        elif isinstance(product, Item):
            # TODO: Verify if the product has in stock

            # TODO: Update qty of the product or return an error
            product.qty += product_payload.get('qty')

        # TODO: Recalculate all the product prices

        subtotal, total = calculate_product_price(product)

        product.total = total
        product.subtotal = subtotal

        # TODO: recalculate the prices on each item
        # The supplier object has total and subtotal. This is the sum of
        # all items

        subtotal, total = calculate_total_and_subtotal(supplier.items)
        supplier.subtotal = subtotal
        supplier.total = total

        # TODO: recalculate the prices of cart
        # The cart has many suppliers. So is need to save the total and
        # subtotal on each supplier

        subtotal, total = calculate_total_and_subtotal(cart.suppliers)
        cart.subtotal = subtotal
        cart.total = total

        try:
            # TODO: Update document with atomic update
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

        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartRemoveProduct(Resource):
    def delete(self, cart_id):
        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        supplier_data, product_data = None, None
        data = None

        try:
            data = request.get_json()
        except Exception:
            return resp_form_invalid('Carts', {'product': 'not empty'})

        supplier_data = data.get('supplier', None)
        product_data = data.get('product', None)

        if supplier_data:
            supplier = get_supplier_by_id(
                cart.suppliers, supplier_data.get('supplier_id')
            )
        else:
            return {
                'status': 404,
                'resource': 'Cart',
                'message': _MSG104,
                'description': 'Este fornecedor não foi encontrado',
                'data': data
            }, 404, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}

        # Object Item Document

        if product_data:
            product = get_product_by_id(
                supplier.items, product_data.get('product_id')
            )
        else:
            return {
                'status': 404,
                'resource': 'Cart',
                'message': _MSG104,
                'description': 'Este produto não foi encontrado',
                'data': data
            }, 404, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}

        # TODO: With cart get product and do an unset atomic update
        # http://docs.mongoengine.org/guide/querying.html#atomic-updates

        # TODO: Recalculate all the product prices

        if not product:
            # TODO: Serializer all objects
            data = cart_detail(cart)

            for supplier in cart.suppliers:
                data['suppliers'].append(supplier_detail(supplier))

            return {
                'status': 404,
                'resource': 'Cart',
                'message': _MSG104,
                'description': 'Este produto não foi encontrado',
                'data': data
            }, 404, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}

        try:
            supplier.items.remove(product)

            if len(supplier.items) == 0:
                cart.suppliers.remove(supplier)
                supplier = None

        except Exception as e:
            # TODO: Serializer all objects
            data = cart_detail(cart)

            for supplier in cart.suppliers:
                data['suppliers'].append(supplier_detail(supplier))

            return {
                'status': 500,
                'resource': 'Cart',
                'message': _MSG104,
                'description': 'Ocorreu um ero ao remover o produto',
                'data': data
            }, 500, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}

        # TODO: recalculate the prices on each item
        # The supplier object has total and subtotal. This is the sum of
        # all items

        if supplier:
            subtotal, total = calculate_total_and_subtotal(supplier.items)
            supplier.subtotal = subtotal
            supplier.total = total

        # TODO: recalculate the prices of cart
        # The cart has many suppliers. So is need to save the total and
        # subtotal on each supplier

        subtotal, total = calculate_total_and_subtotal(cart.suppliers)
        cart.subtotal = subtotal
        cart.total = total

        try:
            # TODO: Update document with atomic update
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

        # TODO: Serializer all objects
        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartIncrementProduct(Resource):

    def put(self, cart_id):

        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        # TODO: Get and find the product_id

        # TODO: With cart get product and do an inc atomic update
        # http://docs.mongoengine.org/guide/querying.html#atomic-updates

        # TODO: Increment qty in all embbed documents

        # TODO: Recalculate all the prices

        # TODO: Serializer all objects
        # get_cart()

        try:
            # TODO: Update document with atomic update
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

        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartDecrementProduct(Resource):

    def put(self, cart_id):

        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        # TODO: Get and find the product_id

        # TODO: With cart get product and do an dec atomic update
        # http://docs.mongoengine.org/guide/querying.html#atomic-updates

        # TODO: Decrement qty in all embbed documents

        # TODO: Recalculate all the prices

        # TODO: Serializer all objects
        # get_cart()
        #
        try:
            # TODO: Update document with atomic update
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

        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}


class CartSetUser(Resource):

    def put(self, cart_id):

        try:
            cart = MCart.objects.get(id=cart_id)

        except NotUniqueError:
            sentry.captureException()

            return resp_already_exists('Carts', 'carrinho')

        except ValidationError as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except MultipleObjectsReturned as e:
            sentry.captureException()

            return resp_exception('Carts', msg=_MSG300, description=e)

        except Exception as e:
            sentry.captureException()

            return resp_exception('Carts', description=e)

        # TODO: Verify if user exists in app only admin has this access
        # Force to data is valid because we do not trust on any information
        # comes from client

        # TODO: With cart get product and do an set atomic update
        # http://docs.mongoengine.org/guide/querying.html#atomic-updates
        # Or we can user save method

        # TODO: Serializer all objects
        # get_cart()

        try:
            # TODO: Update document with atomic update
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

        data = cart_detail(cart)

        for supplier in cart.suppliers:
            data['suppliers'].append(supplier_detail(supplier))

        return {
            'status': 200,
            'resource': 'Cart',
            'message': _MSG104,
            'data': data
        }, 200, {'Set-Cookie': 'api-shopping-cart={}'.format(cart.id)}
