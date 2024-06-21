from django.db import models
from django.contrib.auth.models import User
from datetime import date

CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

GRADE_CHOICES = (
        (1, '1年'),
        (2, '2年'),
        (3, '3年'),
        (4, '4年'),
        (5, '5年'),
)

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    grade = models.PositiveIntegerField(
        choices = GRADE_CHOICES,
        verbose_name='学年'
    )
    
    department =  models.CharField(
        max_length = 50,
        choices = CATEGORY,
        verbose_name='学科'
    )
    
    schoolnumber = models.CharField(max_length = 10, verbose_name='学籍番号')
    classnumber = models.IntegerField(verbose_name ='クラス番号')
    
    last_name_furigana = models.CharField(max_length = 50, verbose_name='名字のフリガナ')
    first_name_furigana = models.CharField(max_length = 50, verbose_name='名前のフリガナ')
    
    birthdate = models.DateField(verbose_name='生年月日')
    
    age = models.IntegerField(verbose_name='年齢')
    
    address = models.CharField(max_length = 50, verbose_name='住所')
    addressnumber = models.IntegerField(verbose_name='郵便番号')
    mobilenumber = models.IntegerField(verbose_name='携帯電話番号')
    
    parent = models.BooleanField(default=False, verbose_name='保護者の了承')
    promotion = models.BooleanField(default=False, verbose_name='条件付き進級者')
    
    submitted = models.BooleanField(default=False)  # フォーム提出状態を管理
    
    def save(self, *args, **kwargs):
        # 生年月日から年齢を計算
        if self.birthdate:
            today = date.today()
            age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
            self.age = age

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.schoolnumber
    # def __str__(self)により、管理画面に表示されるモデル内のデータ（レコード）を判別するための、名前（文字列）を定義することができる
    
    
    
class Company(models.Model):
    number = models.IntegerField(verbose_name='求人番号')
    name = models.CharField(max_length=100, verbose_name='会社名')
    AD = models.IntegerField(null=True, blank=True)
    EE = models.IntegerField(null=True, blank=True)
    ME = models.IntegerField(null=True, blank=True)
    CS = models.IntegerField(null=True, blank=True)
    ALL = models.IntegerField(null=True, blank=True)
    AC = models.IntegerField(null=True, blank=True)
    prefecture = models.CharField(max_length=100, verbose_name='都道府県')
    address = models.CharField(max_length=100, verbose_name='住所') 
    tel = models.CharField(max_length=100, verbose_name='電話番号')
    PIC = models.CharField(max_length=100, verbose_name='担当')
    workplace = models.CharField(max_length=100, verbose_name='勤務地')
    qualified = models.CharField(max_length=100, verbose_name='推薦・自由')
    method = models.CharField(max_length=100, verbose_name='応募方法')
    selection_day = models.CharField(max_length=100, verbose_name='選考日')
    naming = models.CharField(max_length=100, verbose_name='呼称')
    money = models.CharField(max_length=100, verbose_name='資本金')
    employee = models.CharField(max_length=100, verbose_name='従業員数')
    type = models.CharField(max_length=100, verbose_name='業種')
    detail = models.CharField(max_length=100, verbose_name='事業内容')
    occupation = models.CharField(max_length=100, verbose_name='職種')
    web = models.CharField(max_length=100, verbose_name='ホームページ')
    mail = models.CharField(max_length=100, verbose_name='メールアドレス')
    graduated = models.CharField(max_length=100, verbose_name='既卒', null=True, blank=True)
    disabled = models.CharField(max_length=100, verbose_name='障害者採用', null=True, blank=True)
    PDF = models.CharField(max_length=100)
    date = models.DateField(verbose_name='日付')
    
    def __str__(self):
        return self.name

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, null = True, blank = True)
    
    created_at = models.DateTimeField('登録日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    # qualified = models.CharField(max_length=100, verbose_name='推薦・自由')
    qualified = models.BooleanField(verbose_name='推薦')
    
    submit_company = models.CharField(max_length=100, verbose_name='提出先名(会社名)')
    submit_address_number = models.CharField(max_length=100, verbose_name='提出先郵便番号')
    submit_address = models.CharField(max_length=100, verbose_name='提出先住所')
    submit_tel = models.CharField(max_length=100, verbose_name='提出先電話番号')
    
    # student_condition = models.BooleanField(verbose_name='学生部条件')
    student_condition_date = models.DateField(verbose_name='学生部条件解除日', null=True, blank=True)
    edicational_condition = models.BooleanField(verbose_name='教務部条件', null=True, blank=True)
    edicational_condition_date = models.DateField(verbose_name='教務部条件解除日', null=True, blank=True)
    
    procedure_pay = models.BooleanField(verbose_name='認定試験料支払い', null=True, blank=True)
    procedure_contract = models.BooleanField(verbose_name='誓約書提出', null=True, blank=True)
    
    deadline = models.DateField(verbose_name='企業への提出期日', null=True, blank=True)
    
    graduation_certificate = models.IntegerField(verbose_name='卒業・修了証明書', null=True, blank=True)
    expected_graduation_certificate = models.IntegerField(verbose_name='卒業・修了(見込)証明書', null=True, blank=True)
    
    transcript_main = models.IntegerField(verbose_name='成績証明書(本科)', null=True, blank=True)
    transcript_major = models.IntegerField(verbose_name='成績証明書(専攻科)', null=True, blank=True)
    
    health_form = models.IntegerField(verbose_name='健康診断票写', null=True, blank=True)
    
    recommendation_president = models.IntegerField(verbose_name='推薦書(学校長)', null=True, blank=True)
    recommendation_department = models.IntegerField(verbose_name='推薦書(学科長)', null=True, blank=True)
    
    survey = models.IntegerField(verbose_name='健康診断票写', null=True, blank=True)
    unit_certificate = models.IntegerField(verbose_name='単位取得証明書', null=True, blank=True)
    syllabus = models.IntegerField(verbose_name='シラバス', null=True, blank=True)
    
    def __str__(self):
        return str(self.user) + ' ' + self.submit_company
