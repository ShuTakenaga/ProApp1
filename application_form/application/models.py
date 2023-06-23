from django.db import models

CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

# Create your models here.
class FirstModel(models.Model):
    grade = models.IntegerField()
    
    department =  models.CharField(
        max_length = 50,
        choices = CATEGORY
    )
    
    schoolnumber = models.IntegerField()
    classnumber = models.IntegerField()
    
    furigana = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    
    birthdate = models.DateField()
    
    age = models.IntegerField()
    
    address = models.CharField(max_length = 50)
    addressnumber = models.CharField(max_length = 50)
    mobilenumber = models.CharField(max_length = 50)
    
    promotion = models.BooleanField()
    
