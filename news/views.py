from django.shortcuts import render,HttpResponse #print 
from news.models import * 
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import PasswordChangeForm 
from django.http import HttpResponse,HttpResponseRedirect 

# Create your views here.

def index(request):
    category = Category.objects.all()
    news_slider = News.objects.all().order_by('id')[:4]
    news_latest = News.objects.all().order_by('-id')[:4]
    news_picked = News.objects.all().order_by('?')[:4]
    page = "home"
    context = {
        'category':category,
        'news_slider':news_slider,
        'news_latest':news_latest,
        'news_picked':news_picked,
        'page':page,

    }
    return render(request,'index.html',context)
@login_required(login_url='/login')
def user_index(request):
    category = Category.objects.all()
    current_user = request.user 
    profile = UserProfile.objects.get(user_id=current_user.id) 
    context = {'category':category,'profile':profile}
    return render(request,'user_index.html',context)

def login_form(request):
    if request.method == 'POST':#
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:#bo'sh emas mavjud degani
            login(request,user)
            current_user = request.user 
            userprofile = UserProfile.objects.get(user_id=current_user.id) 
            request.session['userimage']=userprofile.image.url 
            return HttpResponseRedirect('/')#127.0.0.1:8000/login
        else:#user yo'q bo'lsa
            messages.warning(request,"Login Error! User Name or Password is incorrect!")
            return HttpResponseRedirect('/login') 
    category = Category.objects.all() 
    context = {'category':category}
    return render(request,'login_form.html',context)

def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():#validatsiya - kiritilayotgan ma'lumotni tekshirib borish
            form.save()#registratsiyadan o'tayotgan payt kiritilayotgan ma'lumotlar saqlanib tursin
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1') 
            user = authenticate(username=username,password=password) 
            login(request,user) 
            current_user = request.user 
            data = UserProfile()
            data.user_id = current_user.id 
            data.image = "/images/users/user.png"
            data.save() 
            messages.success(request,'Your account has been created!')
            return HttpResponseRedirect('/') 
        else:
            messages.warning(reqeust,form.errors)
            return HttpResponseRedirect('/signup')
    form = SignUpForm() 
    category = Category.objects.all()
    context = {'category':category,'form':form}
    return render(request,'signup_form.html',context)
def logout_func(request):
    logout(request) 
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def user_update(request):
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST,instance=request.user) 
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save() 
            profile_form.save() 
            messages.success(request,'Your account has been updated!') 
            return HttpResponseRedirect('/user_index')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) 
        context = {
            'category':category,
            'user_form':user_form,
            'profile_form':profile_form,
            
        } 
        return render(request,'user_update.html',context)
@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save() 
            update_session_auth_hash(request,user) #admin123 adminaka123 ansjkdb1u2e01hcpiqunc1g827dnh@&^!^@*^12vg
            messages.success(request,'Your password was succesfully updated!')
            return HttpResponseRedirect('/user_index')
        else:
            messages.error(request,'Please correct the error below . <br>'+str(form.errors))# eski parol: admin123 yangi parol: adminaka123 takrorlash: adminaka12
            return HttpResponseRedirect('user_password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
    return render(request,'user_password.html',{'form':form,'category':category})

def user_comments(request):
    current_user = request.user 
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'comments':comments,
    }
    return render(request,'user_comments.html',context)
@login_required(login_url='/login')
def user_deletecomment(request,id):
    current_user = request.user 
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.success(request,'Comment deleted!')
    return HttpResponseRedirect('/user_comments')#127.0.0.1:8000/user_comments

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')#yangilik page yangilik qismi
    if request.method == 'POST':#formada ma'lumot post bo'lishi kerak get emas
        form = CommentForm(request.POST)#CommentFormni chaqiramiz 
        if form.is_valid():#formani ma'lumotlarini tekshirib boramiz
            data = Comment()#kiritilgan ma'lumotlarni Comment databasega biriktiramiz yoki qo'shilish(Input)
            data.subject = form.cleaned_data['subject']#nima mazmunda kommentariya qoldirmoqchi (Yangilik mazmunli ekan)
            data.comment = form.cleaned_data['comment']#tekst qismi (yangilikni o'qib tam qanaqadir mazza qildim)
            data.rate = form.cleaned_data['rate']#yangilikka nisbatan baho
           # data.ip = request.META.get()#mijoz ip addressi 
            data.news_id = id #yangilik id si(chunki qaysi yangilikka nisbatan qoldirilayotgani aniq bo'lishi kerak)
            current_user = request.user #foydalanuvchi kim ekanlig
            data.user_id = current_user.id #foydalanuvchi id si
            data.save()#saqlash holati
            messages.success(request,"Sizning kommentariyangiz yuborildi, qiziqish uchun rahmat!")
            return HttpResponseRedirect(url)
        return HttpResponseRedirect(url)

def category_news(request,id,slug):
    category = Category.objects.all()#menuda barcha categorylarni ko'rsatsin
    catdata = Category.objects.get(pk=id)#aynan qaysi category bo'lsa faqat shunga murojaat qilsin
    news = News.objects.filter(category_id=id)#category asosida yangiliklarni taxlab bersin
    context = {
        'category':category,
        'catdata':catdata,
        'news':news,
    }
    return render(request,'category_news.html',context)

def news_detail(request,id,slug):
    category = Category.objects.all()
    news = News.objects.get(pk=id)
    comments = Comment.objects.filter(news_id=id,status='True')
    context = {
        'category':category,
        'news':news,
        'comments':comments,
    }
    return render(request,'news_detail.html',context)













        





    
