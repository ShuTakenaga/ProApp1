from django import forms
from .models import Account


CATEGORY = (('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科'))

# Create your models here.
class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        # super().__init__(*args, **kwargs)
        self.fields['grade'].widget.attrs['placeholder'] = '4'
        self.fields['last_name_furigana'].widget.attrs['placeholder'] = 'タナカ'
        self.fields['first_name_furigana'].widget.attrs['placeholder'] = 'タロウ'
        self.fields['addressnumber'].widget.attrs['placeholder'] = '1234567'
        self.fields['mobilenumber'].widget.attrs['placeholder'] = '08012345678'
        
        self.fields['promotion'].widget.attrs['class'] = ''
        
            
                
    class Meta:
        model = Account
        fields = ('grade', 'department', 'classnumber', 'last_name_furigana', 'first_name_furigana', 'birthdate', 'age', 'address', 'addressnumber', 'mobilenumber', 'promotion')
        widgets = {
            'birthdate': forms.NumberInput(attrs={
                "type": "date"
            })
        }
