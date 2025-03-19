from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .models import Post, AboutUs, Category
from .forms import ContactForm, RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, PostForm
from django.contrib import messages
# To reset password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group

def index(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = int(request.GET.get('page', 1))
    post_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {'title':'Latest posts', 'posts':posts, 'post_obj':post_obj})
def detail(request, slug_id):
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request, "You have no permissions to view posts")
        return redirect("blog:index")
    try:
        post = Post.objects.get(slug=slug_id)
        related_posts = Post.objects.filter(category=post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404()
    return render(request, "blog/detail.html", {'post':post, 'related_posts':related_posts})
def old_url_view(request):
    return redirect("blog:new-url-view")
def new_url_site(request):
    return HttpResponse("This is new site")
def contact(request):
    form = ContactForm()
    name=""
    email=""
    message=""
    if request.method=="POST":
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if form.is_valid():
            print(form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['message'])
            success_message='Email has been sent'
            return render(request, "blog/contact.html", {'form':form, 'success_message':success_message})
        else:
            print("Form validation failed")
    return render(request, 'blog/contact.html', {'form':form, 'name':name, 'email':email, 'message':message})

def about(request):
    about = AboutUs.objects.first()
    if about is None or not about:
        about = "Default content goes here...."
    return render(request, 'blog/about.html', {'about':about})

def register(request):
    form=RegisterForm()
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            readers_group, created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request, "Registration successful. You can login")
            print("Registered successfully")
            return redirect("blog:login")
    return render(request, 'blog/register.html', {'form':form})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Login successful!")
                return redirect("blog:dashboard")
    return render(request, 'blog/login.html', {'form':form})

def dashboard(request):
    blog_title = "My posts"
    # Getting user posts
    all_posts = Post.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page', 1)
    post_obj = paginator.get_page(int(page_number))
    return render(request, "blog/dashboard.html", {"blog_title":blog_title, 'post_obj':post_obj})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    form=ForgotPasswordForm()
    if request.method=='POST':
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user = User.objects.get(email=email)
            # Send email to reset password
            protocol='https' if request.is_secure() else 'http'
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            subject="Reset password requested"
            domain=current_site.domain
            message=render_to_string("blog/reset_password_email_template.html", {'domain':domain, 'uid':uid, 'protocol':protocol, 'token':token,})
            send_mail(subject, message, 'noreply@gamil.com', [email])
            messages.success(request, f"Email has been successfully sent to {email}")
    return render(request, 'blog/forgot_password.html', {'form':form})

def reset_password(request, uidb64, token):
    form=ResetPasswordForm()
    if request.method=="POST":
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password=form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(ValueError, TypeError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")
                return redirect('blog:login')
            else:
                messages.error(request, "Password reset link is invalid")
    return render(request, 'blog/reset_password.html', {'form':form})

@login_required
@permission_required('blog.add_post', raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if post.img_url:
                post.img_url = form.cleaned_data['img_url']
            else:
                post.img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png"
            post.save()
            return redirect('blog:dashboard')
    return render(request, 'blog/new_post.html', {'categories':categories, 'form':form, })

@login_required
@permission_required('blog.change_post', raise_exception=True)
def edit_post(request, post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        raise PermissionDenied("You don't have access to this site")
    form=ContactForm()
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!!!")
            return redirect("blog:dashboard")
    return render(request, "blog/edit_post.html", {'post':post, 'categories':categories, 'form':form })

@login_required
@permission_required('blog.delete_post', raise_exception=True)
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect("blog:dashboard")

@login_required
@permission_required('blog.can_publish', raise_exception=True)
def publish_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.is_published = True
    post.save()
    messages.success(request, "Post published successfully")
    return redirect("blog:dashboard")