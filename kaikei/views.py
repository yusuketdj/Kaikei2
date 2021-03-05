from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q
from .models import Customer, Accounting
from .forms import SearchForm, CustomerCreateForm, AccountingCreateForm
# Create your views here.

def loginfunc(request):
    if request.method == 'POST':
        #フォームで記入した名前とパスワードを変数に代入する
        username = request.POST['username']
        password = request.POST['password']
        #usernameとpasswordの組み合わせを個々の認証バックエンドに対して問い合わせ、認証バックエンドで認証情報が有効とされれば、Userオブジェクトを返す。
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #あるユーザーのログインをさせる。ユーザーのセッション中でのIDを保持する。
            login(request, user)
            return redirect('kaikei:top')
        else:
            return redirect(request, 'kaikei/login.html')
    return render(request, 'kaikei/login.html')

def logoutfunc(request):
    logout(request)
    return redirect('kaikei:login')

def top(request):
    context = {
        'waitingcustomer_list': Customer.objects.filter(is_waiting=True)
    }
    return render(request, 'kaikei/top.html', context)

class IndexView(generic.ListView):

    paginate_by = 5
    template_name = 'kaikei/index.html'
    model = Customer

    #セッションに検索フォームの値を渡す
    def post(self, request, *args, **kwargs):

        #postした内容をそれぞれ、form_value変数（リスト型）に代入
        form_value = [
            self.request.POST.get('customer_id', None),
            self.request.POST.get('name', None),
        ]
        #request.sessionはおそらく辞書型であり、'form_value'キーに対応するvalueとして、form_valueを代入する。
        request.session['form_value'] = form_value

        #requestの情報を辞書型のデータで取得する。
        #copy()メソッドでrequest.GETの値渡しをする。
        self.request.GET = self.request.GET.copy()
        #.clearでリストの全ての要素を削除する。
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    #セッションから検索フォームの値を取得して、検索フォームの初期値としてセットする。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = ''
        name = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            customer_id = form_value[0]
            name = form_value[1]

        default_data = {
            'customer_id': customer_id,
            'name': name,
        }

        test_form = SearchForm(initial=default_data)
        context['test_form'] = test_form

        return context

    #セッションから取得した検索フォームの値に応じてクエリ発行を行う。
    def get_queryset(self):

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            customer_id = form_value[0]
            name = form_value[1]

            condition_customer_id = Q()
            condition_name = Q()

            if len(customer_id) != 0 and customer_id[0]:
                condition_customer_id = Q(customer_id__icontains=customer_id)
            if len(name) != 0 and name[0]:
                condition_name = Q(name__icontains=name)

            return Customer.objects.select_related().filter(condition_customer_id & condition_name)
        else:
            return Customer.objects.none()

def change_waiting(request, num):
    obj = Customer.objects.get(customer_id=num)
    obj.is_waiting = not obj.is_waiting
    obj.save()
    return redirect('kaikei:top')

class CustomerCreate(generic.CreateView):
    model = Customer
    form_class = CustomerCreateForm
    success_url = reverse_lazy('kaikei:top')

def accounting(request, num):
    customer = Customer.objects.get(customer_id=num)
    form = AccountingCreateForm(request.POST or None, initial={'customer': customer})
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('kaikei:accounting_result')

    context = {
        'customer': customer,
        'form': form,
    }
    return render(request, 'kaikei/accounting_form.html', context)

def accounting_result(request):
    accounting = Accounting.objects.last()
    customer = accounting.customer
    customer.is_waiting = not customer.is_waiting
    customer.save()
    context = {
        'accounting': accounting
    }
    return render(request, 'kaikei/accounting_result.html', context)

#フォームに入力されたデータをDBに保存する関数。
def accounting_send(request):
    form = AccountingCreateForm(request.POST)
    form.save()
    return redirect('kaikei:top')