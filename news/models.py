from django.db import models
from django.contrib.auth.models import User 
from django.db.models import Avg,Count
from django.forms import ModelForm,TextInput,Textarea 
from django.urls import reverse
from django.utils.safestring import mark_safe 
from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from django.forms import TextInput, EmailInput,FileInput, Select 
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)# create table Category with title(varchar=255) 
    slug = models.SlugField(null=False,unique=True)
    create_at = models.DateTimeField(auto_now_add=True) #
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title 
    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.title})

class News(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True)
    description = models.TextField(max_length=500,blank=True)
    keywords = models.CharField(max_length=255,blank=True)
    slug = models.SlugField(null=False,unique=True)
    image = models.ImageField(blank=True,upload_to='images/')
    author = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})
    def image_tag(self):
        return mark_safe('<img src="{}" height="50">'.format(self.image.url))
    image_tag.short_description = 'Image'

    def avaregereview(self):#nechi baho qo'yilganligi umumiy qilib ko'rsatilsin 
        reviews = Comment.objects.filter(news=self,status='True').aggregate(avarage=Avg('rate'))#aggregatlar 
        avg = 0 
        if reviews["avarage"] is not None:# 3 4 + 3  umumiy o'rta rating holati kelib chiqadi
            avg = float(reviews["avarage"])
        return avg 
    def countreview(self):#nechta odam user comment qoldirganligi hisoblanadi
        reviews = Comment.objects.filter(news=self,status='True').aggregate(count=Count('id'))
        cnt = 0 
        if reviews["count"] is not None:#kimdir komment qoldirgan bo'lsa hisob yursin
            cnt = int(reviews["count"])
        return cnt 

class Comment(models.Model):
    STATUS = (
        ('True','Mavjud'),
        ('False','Mavjud emas'),
    ) 
    news = models.ForeignKey(News,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=55,blank=True)
    comment = models.CharField(max_length=255,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='True')
    create_at = models.DateTimeField(auto_now_add=True) 
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject 
class CommentForm(ModelForm):
    class Meta:
        model = Comment 
        fields = ['subject','comment','rate']   

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(blank=True,max_length=20)
    image = models.ImageField(blank=True,upload_to='images/users/')

    def __str__(self):
        return self.user.username 
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + '['+self.user.username + ']'
    def image_tag(self):
        return mark_safe('<img src="{}" height="50">'.format(self.image.url))
    image_tag.short_description = 'Image'

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label='User Name:')
    email = forms.EmailField(max_length=200,label='Email:')
    first_name = forms.CharField(max_length=100,help_text='First Name',label='First Name')
    last_name = forms.CharField(max_length=100,help_text='Last Name',label='Last Name')
    class Meta:
        model = User 
        fields = ('username','email','first_name','last_name','password1','password2')

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User 
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username':TextInput(attrs={'class':'input','placeholder':'username'}),
            'email':EmailInput(attrs={'class':'input','placeholder':'email'}),
            'first_name':TextInput(attrs={'class':'input','placeholder':'first_name'}),
            'last_name':TextInput(attrs={'class':'input','placeholder':'last_name'}),
        }
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ('phone','image')
        widgets = {
            'phone':TextInput(attrs={'class':'input','placeholder':'phone'}),
            'image':FileInput(attrs={'class':'input','placeholder':'image'}),
        }


    



