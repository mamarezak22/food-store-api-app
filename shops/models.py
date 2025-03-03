from django.db import models
from django.db.models import Sum,Avg
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from .uploads import store_picture_upload_to
from .managers import OpenStoreManager
from .categories import store_types

user = get_user_model()



class Store(models.Model):

    name = models.CharField(max_length = 50,db_index= True)
    working_hours = models.ForeignKey('WorkingHours',on_delete=models.PROTECT)
    city = models.ForeignKey('city',related_name='stores',on_delete=models.PROTECT)
    picture = models.ImageField(blank = True,upload_to=store_picture_upload_to)
    post_service_price = models.PositiveIntegerField(help_text = "in toman")
 # we can add longitude and latitude after ward for saving stores in map.
    objects = models.Manager()
    open_stores = OpenStoreManager()

    class Meta:
        db_table = 'stores'
        unique_togather = ['name','city']

    @property
    def is_store_open(self):
        start_time = self.working_hours.start_time
        end_time = self.working_hours.end_time
        range_work_hour = range(start_time,end_time)
        now_time = timezone.now()
        if now_time.year in range_work_hour:
            return True
        return False

    @property
    def is_post_free(self):
        if self.post_service_price == 0:
            return True
        return False
    @property
    def star(self):
       query = FoodComment.objects.filter(food__store = self).exclude(star = None).aggregate(avg_star = Avg('star'))
       avg_star = query['avg_star']
       return round(avg_star,2)



    def __str__(self):
        return self.name

class WorkingHours(models.Model):
    start_time = models.IntegerField(validators=[MaxValueValidator(24),MinValueValidator(0)])
    end_time = models.IntegerField(validators=[MaxValueValidator(24),MinValueValidator(0)])

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
    store = models.ForeignKey('Store',on_delete = models.CASCADE,releated_name = 'foods')
    category = models.ManyToManyField('category',related_name='foods')
    price = models.IntegerField('in toman')
    discount_rate = models.DecimalField(default = 0,max_digits=3,decimal_places=2)
    # like 0.9 for 90 percent.
    counts = models.IntegerField(default=0)
    sold_unit = models.IntegerField('count of that food that been saled',default=0)

    class Meta:
        unique_togather = ['name','store']

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
        avg_star = query['avg_star']
        return avg_star


    def __str__(self):
        return self.name

class Category(models.Model):
    parent = models.ForeignKey('self',related_name='sub_categories',on_delete=models.PROTECT,blank=True,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class FoodComment(models.Model):
    food = models.ForeignKey('Food',on_delete =models.CASCADE,related_name='comments')
    user = models.ForeignKey(user, on_delete=models.SET_NULL, related_name='user_food_comments')
    content = models.TextField()
    star = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], blank=True, null=True)
    class Meta:
        unique_togather = ['user','food']


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
        unique_togather = ['city','name']