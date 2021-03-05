from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.IntegerField('ID')
    name = models.CharField('名前', max_length=255)
    is_waiting = models.BooleanField('来院受付済み', default=False)

    def __str__(self):
        return 'ID:{}  {}'.format(self.customer_id, self.name)
    
class Shouhin(models.Model):
    name = models.CharField('商品名', max_length=255)
    price = models.IntegerField('価格')

    def __str__(self):
        return '{}: {}円'.format(self.name, self.price)

class Accounting(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='顧客', on_delete=models.PROTECT)
    shouhin = models.ForeignKey(Shouhin, verbose_name='商品', on_delete=models.PROTECT)
    shouhin_number = models.IntegerField('個数', default=1)
    shouhin_total_price = models.IntegerField('合計')

    def save(self, *args, **kwargs):
        self.shouhin_total_price = self.shouhin.price * self.shouhin_number
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}さん: {}円'.format(self.customer.name, self.shouhin_total_price)
    