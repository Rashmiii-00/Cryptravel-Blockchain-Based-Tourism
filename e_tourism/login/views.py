from bitcoin import *
from django.template.context_processors import csrf
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from datetime import datetime

import bs4
import requests
import ast
# Create your views here.
from hashlib import sha256

def updatehash(*args):
    hashing_text=""
    h=sha256()
    for arg in args:
        hashing_text+=str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Block():
    data = None
    hash = None
    nonce=0
    previous_hash="0"*64

    def __init__(self,data,number=0):
        self.data=data
        self.number=number

    def hash(self):
        return updatehash(
            self.previous_hash,
            self.number,
            self.data,
            self.nonce
        )

    def __str__(self):
        # return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
        #     self.number,
        #     self.hash(),
        #     self.previous_hash,
        #     self.data,
        #     self.nonce
        # ))
        return str({'Block#': self.number, 'Hash': self.hash(), 'Previous Hash': self.previous_hash, 'Data': self.data, 'Nonce': self.nonce})
        


class Blockchain():
    difficulty= 4

    def __init__(self):
        self.chain=[]
    
    def add(self,block):
        self.chain.append(block)

    def remove(self,block):
        self.chain.remove(block)

    def mine(self,block):
        try:
            block.previous_hash=self.chain[-1].hash()
        except IndexError:
            pass
        while True:
            if block.hash()[:self.difficulty]=='0'*self.difficulty:
                self.add(block);break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1,len(self.chain)):
            _previous=self.chain[i].previous_hash
            _current=self.chain[i-1].hash()
            if _current!= _previous or _current[:self.difficulty] != "0"*self.difficulty:
                return False
        return True
def blockchain(request):
    if request.user.is_authenticated:
        username = request.user.username
        transact = Transaction.objects.filter(name=username)
        # print(transact)
        pkey = request.session.get('publicKey')
        blockchain= Blockchain()
        database = []
        for x in transact:
            database.append({'amount': x.amount, 'category': x.category})
            # insert = Block_Chain(name=username, public_key=pkey, address=request.user.first_name, category=x.category,amount=x.amount, )
        num=0
        for data in database:
            num+=1
            blockchain.mine(Block(data,num))

        print(blockchain.isValid())
        for i in blockchain.chain:
            print(type(i))

    context = {'block': blockchain.chain}
    return render(request,'login/blockchain.html',context)

@login_required(login_url='login')
def transaction(request):
    if request.user.is_authenticated:
        username = request.user.username
        transact = Transaction.objects.filter(name=username)
        trans = transact[0]
        pkey = request.session.get('publicKey')
        context ={'transact': transact, 'trans':trans, 'pkey': pkey}
        return render(request,'login/transaction.html',context)
    context ={}
    return render(request,'login/transaction.html',context)

@login_required(login_url='login')
def homepage(request):
    packages = Package.objects.all()
    domestic = Package.objects.filter(category='Domestic')
    domesticplaces = Place.objects.filter(package__in= domestic)
    international = Package.objects.filter(category='International')
    internationalplaces = Place.objects.filter(package__in= international)
    tagcards = Tag.objects.all()
    context = {'domestic':domestic,'international':international,'domesticplaces':domesticplaces,'internationalplaces':internationalplaces,'tagcards':tagcards,'packages': packages}
    return render(request,'login/homepage.html',context)

@login_required(login_url='login')
def iternary(request,name):
    package = Package.objects.get(name=name)
    if request.user.is_authenticated:
        username = request.user.username
        wallet = Wallet.objects.get(name=username)
        if request.method=="POST":
            data = request.POST
            month = data['monsel']
            request.session['selected_month'] = month
            packprice = package.price
            userbal = wallet.balance
            if userbal >= packprice:
                return redirect(to='bookNow')
            else:
                return redirect(to='buyCoin')
    months = package.months.all()
    places = Place.objects.filter(package=package)
    count = places.count()
    days = Day.objects.filter(package=package).order_by('dayno')
    request.session['key'] = name
    context = {'package':package,'places':places,'count':count,'days':days,'months':months,'wallet':wallet}
    return render(request,'login/iternary.html',context)

@login_required(login_url='login')
def tagPackage(request,tagname):
    tag = Tag.objects.get(name=tagname)
    filterpackages = Package.objects.filter(tags=tag)
    context = {'tag':tag,'filterpackages':filterpackages}
    return render(request,'login/tagPackages.html',context)

def register_page(request):
    detail = Details()
    private_key = random_key()
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    detail.private_key = private_key
    detail.public_key = public_key
    detail.address = address
    request.session['publicKey'] = public_key
    

    form = CreateUserForm()
    if request.method == "POST":
        # form = CreateUserForm(request.POST)
        # if form.is_valid():
        #     form.save()
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        private_key = request.POST['private_key']
        public_key = request.POST['public_key']
        address = request.POST['address']
        
        if password1==password2:       
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1, last_name=private_key, first_name=address)
                user.save();
                print('User Created')
            # username = form.cleaned_data['username']
            insert = Wallet(name=username)
            insert.save()
            return redirect('login')
    context = {'form': form, 'detail':detail}
    return render(request, 'login/register.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # pkey = request.session.get('publicKey')
        # request.session['publicKey'] = pkey
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
            return redirect(to='register')
    context = {}
    return render(request, 'login/login.html', context)

@login_required(login_url='login')
def contact(request):
    context ={}
    return render(request,'login/contact.html',context)



@login_required(login_url='login')
def leftovercoins(request):
    if request.user.is_authenticated:
        username = request.user.username
        wallet = Wallet.objects.get(name=username)
        userbal = wallet.balance
        pkey = request.session.get('publicKey')
        print(pkey)
        if userbal != 0:
            if request.method == "POST":
                wallet.balance = 0
                wallet.save()
                transact = Transaction(name=username, public_key = pkey, address=request.user.first_name, category='Left Over Coins', amount=userbal)
                transact.save()
                messages.success(request, 'Coins Transferred!')
                return redirect(to= 'home')
        context ={'userbal':userbal, 'pkey': pkey}
        return render(request,'login/leftovercoins.html',context)
    context ={}
    return render(request, 'login/leftovercoins.html', context)

@login_required(login_url='login')
def tracking(request):
    if request.user.is_authenticated:
        username = request.user.username
        booked = Bookedtrip.objects.filter(name=username)
        now = datetime.now()
        current_month = now.strftime('%B')
        for trip in booked:
            if trip.month == current_month:
                pack = Package.objects.get(name=trip)
                places = Place.objects.filter(package=pack)
                clicks = places[::-1][0]
                context = {'places':places,'clicks':clicks}
                if request.method == "POST":
                    month = request.session.get('selected_month')
                    prev = Prevtrip(name=username, pname=pack, month=month, price=pack.price, pack_pic = pack.package_pic)
                    prev.save()
                    Bookedtrip.objects.get(month=trip.month, name=username).delete()
                    return redirect(to='home')
                return render(request,'login/tracking.html',context)
        context ={}
        return render(request, 'login/tracking.html', context)

# @login_required(login_url='login')
# def getQR(request):
#     data = json.loads(request.body)
#     print(data['id'])

@login_required(login_url='login')
def buyCoin(request):
    pname = request.session.get('key')
    pack = Package.objects.get(name=pname)
    if request.user.is_authenticated:
        username = request.user.username
        wallet = Wallet.objects.get(name=username)
        pkey = request.session.get('publicKey')
        userbal = wallet.balance
        preamt = (pack.price - userbal)*1000
        amt = pack.price - userbal
        wallet.balance = 0
        wallet.save()
        transact = Transaction(name=username, public_key = pkey, address=request.user.first_name, category='Coins Bought for Package Booking', amount=amt)
        transact.save()
    context = {'pack': pack,'userbal':userbal,'preamt':preamt, 'pkey': pkey}
    return render(request,'login/buycoins.html',context)

@login_required(login_url='login')
def buyExtraCoins(request):
    #pname = request.session.get('key')
    #pack = Package.objects.get(name=pname)
    if request.user.is_authenticated:
        username = request.user.username
        wallet = Wallet.objects.get(name=username)
        userbal = wallet.balance
        pkey = request.session.get('publicKey')
        if request.method == "POST":
            data = request.POST
            amt = data['amount']
            addbal = userbal + int(amt)
            update = Wallet.objects.get(name=username)
            update.balance = addbal
            update.save()
            transact = Transaction(name=username, public_key = pkey, address=request.user.first_name, category='Coins Bought During Trip', amount=amt)
            transact.save()
            messages.success(request, 'Coins Added!')
            return redirect(to='home')
    userbal = wallet.balance
    context = {'userbal': userbal, 'pkey': pkey}
    return render(request, 'login/buyextracoins.html', context)

@login_required(login_url='login')
def paymentSuccess(request):
    pname = request.session.get('key')
    month = request.session.get('selected_month')
    if request.user.is_authenticated:
        username = request.user.username
    booked = Package.objects.get(name=pname)
    bookked = Bookedtrip(name=username,pname=pname,month=month,price=booked.price)
    bookked.save()
    context ={'booked':booked,'month':month}
    return render(request,'login/paymentSucessful.html',context)

@login_required(login_url='login')
def bookNow(request):
    pname = request.session.get('key')
    pack = Package.objects.get(name=pname)
    if request.user.is_authenticated:
        username = request.user.username
        userbal = Wallet.objects.get(name=username).balance
        if request.method == "POST":
            packprice = pack.price
            rembal = userbal - packprice
            update = Wallet.objects.get(name=username)
            update.balance = rembal
            update.save()
            return redirect(to='paymentSuccess')
    userbal = Wallet.objects.get(name=username).balance
    context ={'pname':pname,'pack':pack,'userbal':userbal}
    return render(request,'login/booknow.html',context)

@login_required(login_url='login')
def prevTrip(request):
    if request.user.is_authenticated:
        username = request.user.username
        prev = Prevtrip.objects.filter(name=username)
        count = len(prev)
        book = Bookedtrip.objects.filter(name=username)
        bookcount = len(book)
        context = {'username':username,'count':count,'bookcount':bookcount}
        return render(request,'login/mytrips.html',context)
    context = {}
    return render(request, 'login/mytrips.html', context)

@login_required(login_url='login')
def previousTrips(request):
    if request.user.is_authenticated:
        username = request.user.username
        prev = Prevtrip.objects.filter(name=username)
        # print(prev)
    context = {'prev':prev}
    return render(request, 'login/previousTrips.html', context)

@login_required(login_url='login')
def futureTrips(request):
    if request.user.is_authenticated:
        username = request.user.username
        book = Bookedtrip.objects.filter(name=username)
        print(book)
        # print(prev)
    context = {'book':book}
    return render(request, 'login/futureTrips.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


