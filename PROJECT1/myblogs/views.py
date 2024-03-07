from itertools import product
from tokenize import Comment
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from.forms import Blog_Form
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Blog_post, blog_category, contact_info, Subscription
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from.forms import CommentForm
# Create your views here.
def home(request):
    # return HttpResponse('<h1>this is the home page</h1>')
    #fetch the data from db
    x=blog_category.objects.all()
    # print (x)
    return render(request, 'myblogs/home.html',{"category":x})

def findproduct(request):
    if request.method == 'POST':
        x = request.POST.get('prod_search')
        mydata = blog_category.objects.filter(Q(blog_cat__icontains = x))
        if mydata:
            return render(request, 'myblogs/home.html',{"category":mydata})
        else:
            return render(request, 'myblogs/home.html', {'warning':'No Record Found'})
def contact(request):
    # return HttpResponse('<h1>this is the contact page</h1>')
    if request.method == 'GET':
        return render(request, 'myblogs/contact.html')
    elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email=email, u_message=message)
        x.save()
        print(email)
        print(message)
        return render(request,'myblogs/contact.html',{'feedback':'Your message has been recorded'})
    
def subscription(request):
    if request.method == 'GET':
        return render(request, 'myblogs/subscription.html')
    elif request.method == 'POST':
        email = request.POST.get('u_email')
        membership = request.POST.get('u_membership')
        x = Subscription(u_email=email, u_membership=membership)
        if(Subscription.objects.filter(u_email = email).exists()):
          return render(request, 'myblogs/subscription.html', {'feedback' : "You are already a subscribed user!!"})  
        else:    
            x.save()
            print(x)
            print(email)
            print(membership)
            return render(request, 'myblogs/subscription.html', {'feedback' : "Thanks for Subscribing!!"})


def blog(request):
    x = Blog_Form()  
    if request.method == "GET":
        return render(request,'myblogs/blog.html',{"x":x})
    else:
        print("hi")
        form = Blog_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            return render(request,'myblogs/blog.html',{"x":x})
        
@login_required(login_url='loginuser')
def allblogs(request):
    y=Blog_post.objects.all()
    # return render(request,'myblogs/allblogs.html',{"y":y})
    paginator = Paginator(y, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request,"myblogs/allblogs.html",{"y": page_obj})

def blog_details(request, blog_id):
    obj = get_object_or_404(Blog_post, pk=blog_id)
    z= obj.views_count
    z=z+1
    obj.views_count=z
    form=CommentForm()
    obj.save()
    # print(obj)
    # print(blog_id)
    return render(request,'myblogs/blog_details.html', {"obj":obj, "form":form})

    # return HttpResponse('blog_details')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'myblogs/loginuser.html', {'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a, password=b)
        if user is None:
            return render(request,'myblogs/loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Credentials'} )
        else:
            login(request, user)
            return redirect('home')
        
def signupuser(request):
    if request.method =='GET':
        return render(request,'myblogs/signupuser.html',{'form':UserCreationForm()})
    else:
        a= request.POST.get('username') 
        b= request.POST.get('password1') 
        c= request.POST.get('password2') 
        if b==c:
            # check whether user name is unique
            if (User.objects.filter(username =a)):
                return render(request,'myblogs/signupuser.html',{'form':UserCreationForm(),'error': 'User Name  Already exists Try Again'})
            else :
                user =User.objects.create_user(username =a , password=b)
                user.save()
                login(request,user)
                return redirect('home')
        else:
            return render(request,'myblogs/signupuser.html',{'form':UserCreationForm(),'error': 'password Mismatch Try Again'})
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')
    


def blog_cat(request, blog_cat):
    # print(blog_cat)
    x = blog_category.objects.get(blog_cat= blog_cat)
    a = Blog_post.objects.filter(blog_cat=x)

    paginator = Paginator(a, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request,"myblogs/allblogs.html",{"y": page_obj})

def add_likes(request, blog_id):
    obj = get_object_or_404(Blog_post, pk=blog_id)
    print(obj.like_count)
    y= obj.like_count
    y=y+1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)

def add_comment(request, blog_id):
    post = get_object_or_404(Blog_post, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_details', blog_id=post.id)


def delete_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('blog_details', blog_id=blog_id)