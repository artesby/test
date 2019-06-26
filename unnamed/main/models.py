from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    purch_sum = models.FloatField()
    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def tolist(self):
        return (self.id, self.name, self.surname,
            self.email, self.age, self.purch_sum)

class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    amount = models.IntegerField(default=0)
    weight = models.FloatField(default=0)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def tolist(self):
        return (self.id, self.name, self.price,
            self.amount, self.weight)

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purch_date = models.DateTimeField()
    discount = models.FloatField(default=0.)

    objects = models.Manager()


    def __str__(self):
        return str(self.id)

    def tolist(self):
        return (self.id, self.customer, self.item,
            self.purch_date, self.discount)
