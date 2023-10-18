from django.db import models
from django.contrib.auth.models import User

CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    grade = models.IntegerField(verbose_name='学年')
    
    department =  models.CharField(
        max_length = 50,
        choices = CATEGORY,
        verbose_name='学科'
    )
    
    schoolnumber = models.CharField(max_length = 10, verbose_name='学籍番号')
    classnumber = models.IntegerField(verbose_name ='クラス番号')
    
    last_name_furigana = models.CharField(max_length = 50, verbose_name='名字のふりがな')
    first_name_furigana = models.CharField(max_length = 50, verbose_name='名前のふりがな')
    
    
    birthdate = models.DateField(verbose_name='生年月日')
    
    age = models.IntegerField(verbose_name='年齢')
    
    address = models.CharField(max_length = 50, verbose_name='住所')
    addressnumber = models.IntegerField(verbose_name='郵便番号')
    mobilenumber = models.IntegerField(verbose_name='携帯電話番号')
    
    promotion = models.BooleanField(verbose_name='条件付き進級者かどうか')
    
    submitted = models.BooleanField(default=False)  # フォーム提出状態を管理
    
    def __str__(self):
        return self.schoolnumber
    # def __str__(self)により、管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義することができる
    
