from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='')
    subcategory = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default='')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default='')
    phone = models.CharField(max_length=70, default='')
    desc = models.TextField(max_length=500, default='')

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=4000)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=80)
    zip_code = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class OderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default='')
    update_desc = models.CharField(max_length=500)
    timeStmp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:8] + "..."

