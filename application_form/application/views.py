from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.generic import CreateView

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import context, loader
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Account, Company
from .forms import AccountForm, CompanySearchForm

from django.contrib.auth.models import User

from django.contrib import messages

import pandas as pd

from django.core.files.storage import FileSystemStorage

from django.db.utils import IntegrityError

from django.core.paginator import Paginator, EmptyPage

def is_superuser(user):
    return user.is_superuser

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    user = request.user
    
    params = {
        'user' : user
    }
    
    return render(request, 'home.html', params)
    
@login_required
def account_create(request):
    # データベースに Account レコードが存在するかチェック
    if Account.objects.filter(user=request.user).exists():
        # データが登録されている場合、別のページにリダイレクト
        return redirect('/')  # リダイレクト先のURLを設定
    
    form_class = AccountForm
    
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        
        user = request.user
        
        account = account_form.save(commit=False)
        account.user = user
        
        account.submitted = True  # フォームが提出されたことをマーク
        
         # ここで schoolnumber フィールドに値を設定
        account.schoolnumber = user.username

        account.save()  # データベースに保存

        # messages.success(request, 'アカウント作成が完了しました。')
        # return render(request, 'information.html')
        return redirect('information')
    
    else:
        form = AccountForm()
    
    params = {
        'form' : form
    }
    
    return render(request, 'accountcreate.html', params)

@login_required
def information(request):
    if Account.objects.filter(user=request.user).exists():
        # データが登録されている場合、別のページにリダイレクト
        user = request.user
    
        params = {
            'user' : user
        }

        return render(request, 'information.html', params)
    else:
        return redirect('accountcreate')  # リダイレクト先のURLを設定
    
    

@user_passes_test(is_superuser)
def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file, skiprows=2)  # 4行目からデータを読み込む

            # 空白文字列をNoneに変換するヘルパー関数
            def convert_to_int(value):
                if isinstance(value, str) and value.strip() == '':
                    return None
                return int(value) if not pd.isna(value) else None
            
            try:
                # データベースのデータを全て削除（リフレッシュ）
                Company.objects.all().delete()
            except IntegrityError:
                # 例外処理: データの保存時に一意制約違反が発生した場合
                # 既に同じ求人番号のデータが存在している可能性があるため、スキップする
                pass

            for _, row in df.iterrows():
                Company.objects.create(
                    number=convert_to_int(row['求人番号']),
                    name=row['会社名'],
                    AD=convert_to_int(row['AD']),
                    EE=convert_to_int(row['EE']),
                    ME=convert_to_int(row['ME']),
                    CS=convert_to_int(row['CS']),
                    ALL=convert_to_int(row['全']),
                    AC=convert_to_int(row['AC']),
                    prefecture=row['都道府県'],
                    address=row['住所'],
                    tel=row['℡'],
                    PIC=row['担当'],
                    workplace=row['勤務地'],
                    qualified=row['推薦/自由'],
                    method=row['応募方法'],
                    selection_day=row['選考日'],
                    naming=row['呼称'],
                    money=row['資本金'],
                    employee=row['従業員(人)'],
                    type=row['業種'],
                    detail=row['事業内容'],
                    occupation=row['職種'],
                    web=row['ﾎｰﾑﾍﾟｰｼﾞ'],
                    mail=row['メールアドレス'],
                    graduated=row['既卒'],
                    disabled=row['障がい者\n採用'],
                    PDF=row['PDF'],
                    date=row['日付']
                )

            return redirect('company')
    return render(request, 'upload_excel.html')



# @user_passes_test(is_superuser)
# def upload_excel(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         excel_file = request.FILES['excel_file']
#         fs = FileSystemStorage()
#         filename = fs.save(excel_file.name, excel_file)
#         file_url = fs.url(filename)

#         # データベースにExcelデータを保存するコード
#         data = pd.read_excel(excel_file, header=2)  # 3行目をヘッダー行としない

#         def nan_to_none(value):
#             return None if pd.isna(value) else value

#         def convert_to_int(value):
#             if pd.notna(value):
#                 try:
#                     return int(value)
#                 except (ValueError, TypeError):
#                     return None
#             return None

#         for index, row in data.iterrows():
#             try:
#                 company = Company(
#                     number=convert_to_int(row.get('求人番号')),
#                     name=row.get('会社名'),
#                     AD=convert_to_int(row.get('AD')),
#                     EE=convert_to_int(row.get('EE')),
#                     ME=convert_to_int(row.get('ME')),
#                     CS=convert_to_int(row.get('CS')),
#                     ALL=convert_to_int(row.get('全')),
#                     AC=convert_to_int(row.get('AC')),
#                     prefecture=row.get('都道府県'),
#                     address=row.get('住所'),
#                     tel=convert_to_int(row.get('℡')),
#                     PIC=row.get('担当'),
#                     workplace=row.get('勤務地'),
#                     qualified=row.get('推薦/自由'),
#                     method=row.get('応募方法'),
#                     selection_day=row.get('選考日'),
#                     naming=row.get('呼称'),
#                     money=row.get('資本金'),
#                     employee=convert_to_int(row.get('従業員(人)')),
#                     type=row.get('業種'),
#                     detail=row.get('事業内容'),
#                     occupation=row.get('職種'),
#                     web=row.get('ﾎｰﾠﾍﾟｰｼﾞ'),
#                     mail=row.get('メールアドレス'),
#                     date=row.get('日付'),
#                 )
#                 company.save()
#             except IntegrityError:
#                 # 例外処理: データの保存時に一意制約違反が発生した場合
#                 # 既に同じ求人番号のデータが存在している可能性があるため、スキップする
#                 continue

#         return render(request, 'upload_excel.html', {'file_url': file_url})

#     return render(request, 'upload_excel.html')

@login_required
def company(request, num=1):
    # Get the search keyword from the request
    search_keyword = request.GET.get('search_keyword', '')

    # If there's a search query, filter the data
    if search_keyword:
        data = Company.objects.filter(number__icontains=search_keyword) | Company.objects.filter(name__icontains=search_keyword)
    else:
        # If no search query, display all data
        data = Company.objects.all()

    # Pagination logic remains the same
    page = Paginator(data, 50)
    
    # try:
    #     # Try to get the requested page number
    #     current_page = page.page(num)
    # except EmptyPage:
    #     # If the requested page is out of range, redirect to the last page
    #     return redirect('company', num=page.num_pages)

    # params = {
    #     'data': current_page,
    #     'search_keyword': search_keyword,  # Pass the search keyword to the template
    # }
    
    params = {
        'data': page.get_page(num)  # Always display the first page initially
    }
    
    return render(request, 'company.html', params)