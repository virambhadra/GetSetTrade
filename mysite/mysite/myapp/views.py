from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from  django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from matplotlib import pyplot as plt
import urllib,base64
import io

from fastquant import get_yahoo_data , get_stock_data
def home(request):
    count = User.objects.count()
    return render(request, 'home.html',{'count':count})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',{'form':form})

@login_required
def SMA(request):
    return render(request, 'secret_page.html')


def SMA_submit(request):
    symbol = request.POST['name']
    start_date = '-'.join(request.POST['sdate'].split('/')[::-1])
    end_date  = '-'.join(request.POST['ldate'].split('/')[::-1])
    print(symbol,start_date,end_date,sep='\n')
    #df = get_stock_data('AAPL', '2021-01-01', '2021-02-02')
    df = get_stock_data(symbol, start_date, end_date)
    ma30 = df.close.rolling(5).mean()
    close_ma30 = pd.concat([df.close, ma30], axis=1).dropna()
    close_ma30.columns = ['Closing Price', 'Simple Moving Average (30 day)']
    ma30.dropna()
    close_ma30.plot(figsize=(20, 6))
    plt.title("SMA", fontsize=20)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,'secret_page.html',{'data':uri})


def Backtest_sma(request):
    from fastquant import backtest
    import pandas as pd
    from matplotlib import pyplot as plt
    import urllib,base64
    import io
    from fastquant import get_yahoo_data , get_stock_data
    df = get_stock_data('AAPL', '2021-01-01', '2021-02-01')
    #%matplotlib
    backtest('smac', df, fast_period=15, slow_period=40)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,'secret_page.html',{'data1':uri})

class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'