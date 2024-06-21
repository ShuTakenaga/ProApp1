from django import forms
from .models import Account, Application


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
        
        self.fields['parent'].widget.attrs['class'] = ''
        self.fields['promotion'].widget.attrs['class'] = ''

    class Meta:
        model = Account
        fields = ('grade', 'department', 'classnumber', 'last_name_furigana', 'first_name_furigana', 'birthdate', 'address', 'addressnumber', 'mobilenumber', 'parent', 'promotion')
        widgets = {
            'birthdate': forms.NumberInput(attrs={
                "type": "date"
            }), 
            'parent': forms.CheckboxInput(attrs={'required': 'required'}),
        }
        
class EditAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
            self.fields['promotion'].widget.attrs['class'] = ''
            
    class Meta:
        model = Account
        fields = ['grade', 'classnumber', 'address', 'addressnumber', 'mobilenumber', 'promotion']

class CompanySearchForm(forms.Form):
    search_keyword = forms.CharField(label = 'Search', max_length=100, required=False)
    
class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        # super().__init__(*args, **kwargs)
        # self.fields['grade'].widget.attrs['placeholder'] = '4'
        # self.fields['last_name_furigana'].widget.attrs['placeholder'] = 'タナカ'
        # self.fields['first_name_furigana'].widget.attrs['placeholder'] = 'タロウ'
        # self.fields['addressnumber'].widget.attrs['placeholder'] = '1234567'
        # self.fields['mobilenumber'].widget.attrs['placeholder'] = '08012345678'
        
        self.fields['qualified'].widget.attrs['class'] = ''
        # self.fields['student_condition'].widget.attrs['class'] = ''
        # self.fields['edicational_condition'].widget.attrs['class'] = ''
        # self.fields['procedure_pay'].widget.attrs['class'] = ''
        # self.fields['procedure_contract'].widget.attrs['class'] = ''
        

    class Meta:
        model = Application
        fields = ('qualified', 'submit_company', 'submit_tel', 'submit_address', 'submit_address_number' ,'deadline', 'graduation_certificate', 'expected_graduation_certificate', 'transcript_main', 'transcript_major', 'health_form', 'recommendation_president', 'recommendation_department', 'survey', 'unit_certificate', 'syllabus')
        
        # 'student_condition_date', 'edicational_condition', 'edicational_condition_date', 'procedure_pay', 'procedure_contract', 
        
        widgets = {
            # 'student_condition_date': forms.NumberInput(attrs={
            #     "type": "date"
            # }),
            # 'edicational_condition_date': forms.NumberInput(attrs={
            #     "type": "date"
            # }),
            'deadline': forms.NumberInput(attrs={
                "type": "date",
                'required': 'required',
            }),
        }
        
class EditApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditApplicationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['qualified'].widget.attrs['class'] = ''
        
    class Meta:
        model = Application
        fields = ['submit_company', 'submit_address_number', 'submit_address', 'submit_tel', 'deadline', 'qualified', 'graduation_certificate', 'expected_graduation_certificate', 'transcript_main', 'transcript_major', 'health_form', 'recommendation_president', 'recommendation_department', 'survey', 'unit_certificate', 'syllabus']

        widgets = {
            # 'student_condition_date': forms.NumberInput(attrs={
            #     "type": "date"
            # }),
            # 'edicational_condition_date': forms.NumberInput(attrs={
            #     "type": "date"
            # }),
            'deadline': forms.NumberInput(attrs={
                "type": "date",
                'required': 'required',
            }),
        }
        

