from django.db import models
from django.contrib.auth.models import User, AbstractUser


CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    grade = models.IntegerField()
    
    department =  models.CharField(
        max_length = 50,
        choices = CATEGORY
    )
    
    schoolnumber = models.CharField(max_length = 10)
    classnumber = models.IntegerField()
    
    first_name_furigana = models.CharField(max_length = 50)
    last_name_furigana = models.CharField(max_length = 50)
    
    birthdate = models.DateField()
    
    age = models.IntegerField()
    
    address = models.CharField(max_length = 50)
    addressnumber = models.IntegerField()
    mobilenumber = models.IntegerField()
    
    promotion = models.BooleanField()
    
    def __str__(self):
        return self.schoolnumber
    # def __str__(self)により、管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義することができる
    
