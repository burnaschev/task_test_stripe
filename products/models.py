from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, "blank": True}


class Currency(models.TextChoices):
    USD = 'USD', _('USD')
    RUB = 'RUB', _('RUB')


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD, verbose_name='валюта')

    def __str__(self):
        return f'{self.name} = {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Discount(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма')

    def __str__(self):
        return f'{self.name}/ {self.amount}'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ставка')

    def __str__(self):
        return f'{self.name}/ {self.rate}'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='orders', verbose_name='продукт')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, **NULLABLE, verbose_name='скидка')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, **NULLABLE, verbose_name='налог')
    total_amount = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='общая сумма')
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.USD, verbose_name='валюта')

    def calculate_total_amount(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total -= self.discount.amount
        if self.tax:
            total *= (1 + self.tax.rate / 100)
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
