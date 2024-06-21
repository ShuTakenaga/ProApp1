from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account, Company, Application
from .forms import AccountForm, CompanySearchForm, ApplicationForm, EditAccountForm, EditApplicationForm
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, EmptyPage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from django.templatetags.static import static
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from io import BytesIO
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Q

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
    
@login_required
def edit_account(request):
    if Account.objects.filter(user=request.user).exists():
        user = request.user

        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=user.account)

            if form.is_valid():
                form.save()
                messages.success(request, 'アカウント情報が正常に更新されました。')
                return redirect('information')
            else:
                messages.error(request, 'フォーム内のエラーを修正してください。')
        else:
            form = EditAccountForm(instance=user.account)

        return render(request, 'edit_account.html', {'form': form})
    else:
        return redirect('accountcreate')

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
                company_name = row['会社名'].replace('\n', '').replace('\r', '')
                
                Company.objects.create(
                    number=convert_to_int(row['求人番号']),
                    name=company_name,
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

@login_required
def company(request, num=1):
    if Account.objects.filter(user=request.user).exists():
        # Get the search keyword from the request
        search_keyword = request.GET.get('search_keyword', '')
        
        user_department = request.user.account.department
        
        
        # If there's a search query, filter the data
        if search_keyword:
            if user_department == 'ME':
                data = Company.objects.filter(Q(ALL=True)| Q(ME=True) )
                data = data.filter(number__icontains=search_keyword) | data.filter(name__icontains=search_keyword)
            if user_department == 'CS':
                data = Company.objects.filter(Q(ALL=True)| Q(CS=True) )
                data = data.filter(number__icontains=search_keyword) | data.filter(name__icontains=search_keyword)
        else:
            if user_department == 'AD':
                data = Company.objects.filter(Q(AD__isnull=False) | Q(ALL__isnull=False))
            elif user_department == 'EE':
                data = Company.objects.filter(Q(EE__isnull=False) | Q(ALL__isnull=False))
            elif user_department == 'ME':
                data = Company.objects.filter(Q(ME__isnull=False) | Q(ALL__isnull=False))
            elif user_department == 'CS':
                data = Company.objects.filter(Q(CS__isnull=False) | Q(ALL__isnull=False))
            elif user_department == 'AC':
                data = Company.objects.filter(Q(AC__isnull=False))
            # If no search query, display all data

        # Pagination logic remains the same
        page = Paginator(data, 50)
        
        params = {
            'data': page.get_page(num)  # Always display the first page initially
        }
        
        return render(request, 'company.html', params)
    else:
        return redirect('accountcreate')
    
@login_required
def application_create(request, company_name):
    if request.user.account.promotion == True:
        return redirect('edit_account')
    else:
        if Account.objects.filter(user=request.user).exists():
            # company = get_object_or_404(Company, name=company_name)
            companies = Company.objects.filter(name=company_name)

            if companies.exists():
                company = companies.first()  # 例: 最初のオブジェクトを取得
            else:
                # オブジェクトが存在しない場合の処理
                return redirect('comapny')


            # 既存の申請書を取得
            existing_application = Application.objects.filter(user=request.user, company=company).first()

            if existing_application:
                # 既に申請している場合、申請書の詳細画面にリダイレクト
                return redirect('application_detail', pk=existing_application.pk)

            if request.method == 'POST':
                form = ApplicationForm(request.POST)

                user = request.user

                if form.is_valid():
                    application = form.save(commit=False)
                    application.user = user
                    application.company = company  # companyを使用
                    application.save()
                    return redirect('application_detail', pk=application.pk)
            else:
                if company.qualified == '推薦':
                    form = ApplicationForm(initial={
                        'submit_company': company.name,
                        'submit_address': company.prefecture + company.address,
                        'submit_tel': company.tel,
                        'qualified': True,
                    })  # 初期値としてcompany.nameを設定
                else:
                    form = ApplicationForm(initial={
                        'submit_company': company.name,
                        'submit_address': company.prefecture + company.address,
                        'submit_tel': company.tel,
                    })  # 初期値としてcompany.nameを設定

            return render(request, 'application_create.html', {'form': form})
        else:
            return redirect('accountcreate')
    
@login_required
def edit_application(request, pk):
    application = get_object_or_404(Application, pk=pk)

    # 編集権限の確認
    if application.user != request.user:
        return redirect('application_list')  # ログインユーザーと申請のユーザーが一致しない場合はリダイレクト

    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'edit_application.html', {'form': form})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    user = request.user
    
    # 編集権限の確認
    if application.user != request.user:
        return redirect('application_list')  # ログインユーザーと申請のユーザーが一致しない場合はリダイレクト

    context = {
        'user': user,
        'application': application,
    }

    return render(request, 'application_detail.html', context)

def generate_pdf(request, pk):
    application = get_object_or_404(Application, pk=pk)
    user = request.user

    # Load the existing PDF template
    template_path = 'application/static/pdf/test.pdf'

    template_pdf = PdfReader(template_path)

    # Create a new PDF to write the result
    result_pdf = PdfWriter()

    # Add the existing template pages to the result PDF
    for page in template_pdf.pages:
        result_pdf.add_page(page)

    # font_path = 'application/static/fonts/ipaexm.ttf'

    # PDFにフォントを登録
    # pdfmetrics.registerFont(TTFont('ipa', 'application/static/fonts/ipaexm.ttf'))
    
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))


    # Create a canvas to draw on the result PDF
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    can.setFont('HeiseiMin-W3', 10)
    can.drawString(125, 715, user.account.last_name_furigana + '     ' + user.account.first_name_furigana)
    can.drawString(84, 729, f'{user.account.grade}')
    
    can.drawString(245, 729, f'{user.account.classnumber}')
    can.drawString(375, 729, f'{user.account.schoolnumber}')
    
    can.drawString(132, 659, str(user.account.addressnumber)[0:3] + '    ' + str(user.account.addressnumber)[3:])
    
    can.drawString(132, 578, str(application.submit_address_number)[0:3] + '    ' + str(application.submit_address_number)[3:])
    
    can.setFont('HeiseiMin-W3', 12)

    # Draw your data on the canvas
    can.drawString(416, 780, str(application.created_at)[0:4] +'    ' + str(application.created_at)[5:7] + '    ' + str(application.created_at)[8:10])
    
    if user.account.department == 'AD':
        can.drawString(114, 728, '○')
        
    if user.account.department == 'EE':
        can.drawString(136, 728, '○')
        
    if user.account.department == 'ME':
        can.drawString(158, 728, '○')
        
    if user.account.department == 'CS':
        can.drawString(179, 728, '○')
    
    if user.account.department == 'AC':
        can.drawString(201, 728, '○')
    
    can.drawString(125, 670, str(user.account.birthdate)[0:4] + '            ' + str(user.account.birthdate)[5:7] + '           ' + str(user.account.birthdate)[8:])
    can.drawString(276, 670, f'{user.account.age}')
    can.drawString(125, 642, f'{user.account.address}')
    can.drawString(125, 620, '0' + str(user.account.mobilenumber))
    
    can.drawString(200, 590, f'{application.submit_company}')
    can.drawString(125, 561, f'{application.submit_address}')
    can.drawString(125, 540, f'{application.submit_tel}')
    
    can.drawString(199, 392, str(application.deadline)[5:7] + '       ' + str(application.deadline)[8:])
    
    
    
    can.setFont('HeiseiMin-W3', 17)

    can.drawString(125, 688, user.last_name + '     ' + user.first_name)
    
    can.drawString(274, 511, '○')
    
    can.drawString(287, 482, '○')
    
    can.setFont('HeiseiMin-W3', 20)
    if application.qualified == True:
        can.drawString(74, 587, '○')
    else:
        can.drawString(122, 587, '○')
        
    can.setFont('HeiseiMin-W3', 10)
    
    graduation_certificate = application.graduation_certificate if application.graduation_certificate is not None else 0
    expected_graduation_certificate = application.expected_graduation_certificate if application.expected_graduation_certificate is not None else 0
    transcript_main = application.transcript_main if application.transcript_main is not None else 0
    transcript_major = application.transcript_major if application.transcript_major is not None else 0
    health_form = application.health_form if application.health_form is not None else 0
    recommendation_president = application.recommendation_president if application.recommendation_president is not None else 0
    recommendation_department = application.recommendation_department if application.recommendation_department is not None else 0
    survey = application.survey if application.survey is not None else 0
    unit_certificate = application.unit_certificate if application.unit_certificate is not None else 0
    syllabus = application.syllabus if application.syllabus is not None else 0
    # 他の変数も同様に処理

    can.drawString(358, 339, str(graduation_certificate) + '                            ' + str(graduation_certificate * 600))
    can.drawString(358, 327, str(expected_graduation_certificate) + '                            ' + str(expected_graduation_certificate * 600))
    can.drawString(358, 315, str(transcript_main) + '                            ' + str(transcript_main * 1000))
    can.drawString(358, 303, str(transcript_major) + '                            ' + str(transcript_major * 1000))
    can.drawString(358, 290, str(health_form) + '                            ' + str(health_form * 500))
    can.drawString(358, 278, str(recommendation_president) + '                            ' + str(recommendation_president * 1000))
    can.drawString(358, 265, str(recommendation_department) + '                            ' + str(recommendation_department * 0))
    can.drawString(358, 252, str(survey) + '                            ' + str(survey * 2000))
    can.drawString(358, 238, str(unit_certificate) + '                            ' + str(unit_certificate * 500))
    can.drawString(358, 224, str(syllabus) + '                            ' + str(syllabus * 500))
    
    sum = graduation_certificate + expected_graduation_certificate + transcript_main + transcript_major + health_form + recommendation_president + recommendation_department + survey + unit_certificate + syllabus

    sum_price = graduation_certificate * 600 + expected_graduation_certificate * 600 + transcript_main * 1000 + transcript_major * 1000 + health_form * 500 + recommendation_president * 1000 + recommendation_department * 0 + survey * 2000 + unit_certificate * 600 + syllabus * 2000

    
    can.drawString(358, 161, str(sum) + '                            ' + str(sum_price))
    
    can.save()

    # Move the BytesIO position to the beginning
    packet.seek(0)

    # Create a new PDF reader for the canvas content
    new_pdf = PdfReader(packet)

    # Merge the canvas content with the existing pages
    for page_num in range(len(result_pdf.pages)):
        page = result_pdf.pages[page_num]
        page.merge_page(new_pdf.pages[page_num])

    # Create a response with the merged PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="application_{pk}.pdf"'
    result_pdf.write(response)

    return response

@login_required
def application_list(request):
    user = request.user
    # ログインユーザーに関連する申請書の一覧を取得
    applications = Application.objects.filter(user=user)
    
    params = {
        'applications': applications,
    }

    return render(request, 'application_list.html', params)
