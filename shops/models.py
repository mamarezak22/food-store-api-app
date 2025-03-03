from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from .uploads import store_picture_upload_to,food_picture_upload_to
from .managers import OpenStoreManager
from .categories import store_types

User = get_user_model()



class Store(models.Model):

    name = models.CharField(max_length = 50,db_index= True)
    store_type = models.CharField(max_length=15,choices=store_types)
    working_hours = models.ForeignKey('StoreWorkingHour',on_delete=models.PROTECT)
    city = models.ForeignKey('City',related_name='stores',on_delete=models.PROTECT)
    picture = models.ImageField(blank = True,upload_to=store_picture_upload_to)
    post_service_price = models.PositiveIntegerField(help_text = "in toman")
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default=True)
 # we can add longitude and latitude after ward for saving stores in map.
    objects = models.Manager()
    open_stores = OpenStoreManager()

    class Meta:
        db_table = 'stores'
        unique_together = ['name','city']

    def __str__(self):
        return self.name

    @property
    def is_store_open(self):
        return self.working_hours.start_time <= timezone.now().hour < self.working_hours.end_time

    @property
    def is_post_free(self):
        if self.post_service_price == 0:
            return True
        return False
    
    @property
    def star(self):
       query = FoodComment.objects.filter(food__store = self).exclude(star = None).aggregate(avg_star = Avg('star'))
       if query:
           avg_star = query['avg_star']
           return round(avg_star,2)



class StoreWorkingHour(models.Model):
    start_time = models.IntegerField(validators=[MaxValueValidator(23),MinValueValidator(0)])
    end_time = models.IntegerField(validators=[MaxValueValidator(23),MinValueValidator(0)])

    def clean(self):
        #this method calls when the data is validating and before saving.
        if self.start_time >= self.end_time:
            raise ValidationError({
                'start_time': "Start time must be before end time.",
                'end_time': "End time must be after start time.",
            })

    def save(self, *args, **kwargs):
        #do all the validation plus our validation and save.
        self.full_clean()
        super().save(*args, **kwargs)


class Food(models.Model):
    name = models.CharField(max_length= 50,db_index=True)
    description = models.TextField()
    image = models.ImageField(upload_to=food_picture_upload_to)
    store = models.ForeignKey('Store',on_delete = models.CASCADE,related_name = 'foods')
    category = models.ForeignKey('Category',related_name='foods',on_delete = models.PROTECT)
    price = models.PositiveIntegerField('in toman')
    discount_rate = models.DecimalField(default = 0,max_digits=3,decimal_places=2,validators=[MaxValueValidator(0.99),MinValueValidator(0)])
    # like 0.9 for 90 percent.
    counts = models.PositiveIntegerField(default=0)
    sold_unit = models.PositiveIntegerField('count of that food that been saled',default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name','store']

    @property
    def has_discount(self):
        if self.discount_rate :
            return True
        return False

    @property
    def is_available(self):
        if self.counts:
            return True
        return False

    @property
    def star(self):
        query = self.comments.exclude(star = None).aggregate(avg_star = Avg('star'))
        if query :
            avg_star = query['avg_star']
            return avg_star

    @property
    def final_price(self):
        return self.price - (self.price * self.discount_rate)


class Category(models.Model):
    parent = models.ForeignKey('self',related_name='sub_categories',on_delete=models.PROTECT,blank=True,null=True)
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ['parent','name']

    def __str__(self):
        return self.name



class FoodComment(models.Model):
    food = models.ForeignKey('Food',on_delete =models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_food_comments',null=True)
    content = models.TextField()
    star = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], blank=True, null=True)

    def __str__(self):
        return self.content

    class Meta:
        unique_together = ['user','food']


class City(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Region(models.Model):
    city = models.ForeignKey('City',on_delete=models.PROTECT,related_name='regions')
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['city','name']