from django import forms
from .models import Account
    
CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

# Create your models here.
class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # if self.instance.user:
        #     # schoolnumber フィールドに初期値を設定
        #     if not self.instance.schoolnumber:
        #         self.fields['schoolnumber'].initial = self.instance.user.username     
                
    class Meta:
        model = Account
        fields = ('grade', 'department', 'classnumber', 'last_name_furigana', 'first_name_furigana', 'birthdate', 'age', 'address', 'addressnumber', 'mobilenumber', 'promotion')
