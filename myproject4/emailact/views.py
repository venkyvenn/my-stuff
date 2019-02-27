from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import Product,Stock
from .forms import SignUpForm
from django.http import HttpResponse
from .tokens import account_activation_token


@login_required
def home(request):
    if request.method=="GET":
        return render(request, 'home1.html')
    else:
        data=request.POST['drop1']
        if data=='pn':
            pnm=request.POST['dt']
            recs=Product.objects.filter(pname=pnm)
            return render(request,'display.html',{'records':recs})
        else:
            pi=int(request.POST['dt'])
            recs=Product.objects.filter(pid=pi)
            return render(request,'display.html',{'records':recs})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def search(request):
    if request.method=="GET":
        return render(request,"search.html")
    else:
        data=request.POST['drop1']
        if data=="pn":
            pnm=request.POST['dt']
            recs=Product.objects.filter(pname=pnm)
            return render(request,"display.html",{"records":recs})
        elif data=="pcst":
            pcst=float(request.POST['dt'])
            recs=Product.objects.filter(pcost=pcst)
            return render(request, "display.html", {"records": recs})
        else:
            pi=request.POST['dt']
            recs=Product.objects.filter(pid=pi)
            return render(request,"display.html",{"records":recs})
@login_required
def addcart(request):
    x=request.GET['pid']
    qt=Stock.objects.filters(prodid=x)
    qtt=0
    for p in qt:
        qtt=p
    qt==[q for q in range(1,qtt.tot_qty+1)]
    return render(request,'addcart.html',{'pid':x,'qtt':qt})


@login_required
def cart(request):
    dic={}
    for k,v in request.session.items():
        if k[0]!='_':
            dic[k]=v
    return render(request,"cart.html",{'k':dic})


def track(request):
    return HttpResponse("product will deliver soon")



@login_required
def cancel(request):
    return HttpResponse("order cancelled")




