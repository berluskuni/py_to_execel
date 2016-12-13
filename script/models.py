from django.db import models

# Create your models here.


class Product(models.Model):
    class Meta:
        ordering = ['number_catalog']
        verbose_name = u'Номер в каталоге'
        verbose_name_plural = u'Номера в каталоге'

    number_catalog = models.CharField(max_length=120, verbose_name=u'Номер в каталоге', unique=True)
    name_detail = models.CharField(max_length=120, verbose_name=u'Название детали', default='')
    brand = models.CharField(max_length=120, verbose_name=u'Бренд производителя')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Цена товара')
    time_shipping = models.CharField(max_length=120, verbose_name=u'Время доставки')

    def __str__(self):
        return self.number_catalog
