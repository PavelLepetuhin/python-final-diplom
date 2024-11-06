from celery import Celery
from django.core.mail import EmailMessage
from .models import Product, ProductInfo, Parameter, ProductParameter, Shop, Category
import yaml
from urllib.request import urlopen

import logging

logger = logging.getLogger('celery')

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def send_email(subject, message, recipient_list):
    logger.debug('send_email')
    """
    A Celery task for sending emails.

    Args:
    subject (str): The subject of the email.
    message (str): The content of the email.
    recipient_list (list): A list of recipient email addresses.
    """
    email = EmailMessage(subject, message, to=recipient_list)
    email.send()

    logger.debug('send_email done')


@app.task
def do_import(url):
    logger.debug('do_import')
    """
    A Celery task for importing data from a specified URL.

    Args:
    url (str): The URL from which to import the data.
    """
    stream = urlopen(url)
    data = yaml.safe_load(stream)

    shop, _ = Shop.objects.get_or_create(name=data['shop'])
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)

    logger.debug('do_import done')
