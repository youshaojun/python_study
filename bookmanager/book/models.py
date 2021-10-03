from django.db import models


# Create your models here.

class Book(models.Model):
    url = models.CharField(max_length=500, default='')
    remark = models.CharField(max_length=2048, default='')
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_book'
        verbose_name = '热门图书'
