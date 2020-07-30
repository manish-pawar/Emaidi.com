from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import WorkerForm, CustomerForm, OrderForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, customer_only
from django.contrib.auth.models import Group
from datetime import datetime, timezone

# Create your views here.


@unauthenticated_user
def registerUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'eb/register.html', context)


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'eb/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@customer_only
def home(request):
    return render(request, 'eb/home.html')


def avails(w):
    p = w.period_work

    now = datetime.now(timezone.utc)
    delta = now - w.date_created
    difw = delta.days
    if p == '1 month' and difw > 29:
        return True

    elif p == '6 month' and difw > 181:
        return True

    elif p == '1 year' and difw > 364:
        return True

    elif p == '15 days' and difw > 14:
        return True

    elif p == '1 day trial' and difw > 0:
        return True

    else:
        return False


def maidavail(cuus):
    worker = Worker.objects.all()
    workers = []
    loca = cuus.customer.city

    for work in worker:
        if work.city == loca:
            workers.append(work)
    worker2 = []
    w = []
    for worker1 in workers:
        w = worker1.order_set.all()
        if len(w) == 0:
            worker2.append(worker1)
        else:
            z = w.order_by('-id')[0]
            if avails(z):
                worker2.append(worker1)
    return worker2


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    uses = request.user
    if uses.customer.city is None:

        messages.warning(request, 'Before you are going to book please enter your details so'
                                  ' that we can find Maids that are nearer to you. ')
        return redirect('u-acc')
    else:
        worker = uses.customer.order_set.all()
        print(worker)
        counta = worker.count()
        worker3 = maidavail(uses)

        coun = len(worker3)
        if len(worker) == 0:
            maids = False
            context = {'shown': 'Not yet booked any Maid ', 'available': coun, 'counts': counta, 'maid': maids}
        else:
            maids = True
            lister = worker.order_by('-id')[0]

            kam = lister.worker
            ah = avails(lister)
            if ah:
                context = {'workers': True, 'counts': counta, 'available': coun, 'maid': maids}
            else:
                context = {'worker': kam, 'counts': counta, 'available': coun, 'maid': maids}

    return render(request, 'eb/userpage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def historyl(request):
    uses = request.user
    worker = uses.customer.order_set.all().order_by('-id')

    context = {'worker': worker}

    return render(request, 'eb/historypage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def maid(request):
    cuus = request.user
    if cuus.customer.city is None:

        messages.warning(request, 'Before you are going to book please enter your details so'
                                  ' that we can find Maids that are nearer to you. ')
        return redirect('u-acc')
    else:
        wo = []

        worker2 = maidavail(cuus)
        cuus1 = cuus.customer.order_set.all()

        if len(cuus1) == 0:
            context = {'workers': worker2}
        else:
            cuus2 = cuus1.order_by('-id')[0]

            a = avails(cuus2)
            if a:
                books = False
                context = {'workers': worker2, 'maid': books}

            else:
                books = True

                worker3 = []
                wils = cuus.customer.wishlist_set.all()
                for i in wils:
                    worker3.append(i.worker.id)

                if len(worker3) == 0:
                     context = {'workers': worker2, 'maid': books}
                else:
                     context = {'workers': worker2, 'wishlist': worker3, 'maid': books}


        if len(worker2) == 0:

            messages.warning(request, 'Sorry But no one is there in your village from our Emaid section ')

    return render(request, 'eb/maid.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountu(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}

    return render(request, 'eb/useracc.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def book(request, id):
    if request.method == 'POST':
        customer = request.user.customer
        worker = Worker.objects.get(id=id)
        period = request.POST.get('period')
        order = Order(customer=customer, worker=worker, period_work=period)
        order.save()
        messages.success(request, 'Successfuly booked maid!!!')
        return redirect('user-page')
    context = {'id': id}
    return render(request, 'eb/book.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def details(request, id):
    worke = Worker.objects.get(id=id)
    context = {'worker': worke}
    return render(request, 'eb/details.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def wishlistli(request):
    user = request.user
    wishli = user.customer.wishlist_set.all()
    cuus1 = user.customer.order_set.all()
    if len(cuus1) == 0:
        messages.success(request, 'Sorry you havent book any maid . Book your first maid to wishlist maid.')
        return redirect('user-page')

    else:
        cuus2 = cuus1.order_by('-id')[0]

        a = avails(cuus2)
        if a:
            books = False
            context = {'listw': wishli, 'maid': books}

        else:
            books = True
            context = {'listw': wishli, 'maid': books}

    return render(request, 'eb/wishlist.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def wishlistl(request):
    if request.method == 'GET':
        user = request.user
        wish_id = request.GET['wish_id']
        wishlist = Worker.objects.get(id=wish_id)  # getting the liked posts
        m = Wishlist(customer=user.customer, worker=wishlist)

        m.save()
        return HttpResponse("Success!")  # Sending an success response
    else:
        return HttpResponse("Request method is not a GET")


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def surity(request):
    return render(request, 'eb/sure.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def workerr(request):
    customer = request.user.customer
    user = request.user
    b = Customer.objects.get(name=customer.name)
    b.delete()
    group = Group.objects.get(name='customer')
    user.groups.remove(group)
    Worker.objects.create(user=user, name=user.username, )
    group1 = Group.objects.get(name='maid')
    user.groups.add(group1)

    return render(request, 'eb/work.html')


@login_required(login_url='login')
def home1(request):
    user = request.user
    curren = user.worker.order_set.all()
    firs = curren.order_by('-id')[0]
    histy = curren.order_by('-id')
    now = datetime.now(timezone.utc)

    delta = now - user.worker.date_created
    difw = delta.days

    context = {'first': firs, 'history': histy,'exper': difw}
    return render(request, 'eb/maidhome.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['maid'])
def board(request):
    return render(request, 'eb/board.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['maid'])
def accountm(request):
    worker = request.user.worker
    form = WorkerForm(instance=worker)
    if request.method == 'POST':
        form = WorkerForm(request.POST, request.FILES, instance=worker)
        if form.is_valid():
            form.save()
    context = {'form': form}

    return render(request, 'eb/maidacc.html', context)