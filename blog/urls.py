from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug_id>", views.detail, name="detail"),
    path("old-url", views.old_url_view, name="old-url"),
    path("new-url-path", views.new_url_site, name="new-url-view"),
    path("contact", views.contact, name="contact-form"),
    path("about", views.about, name='about-page'),
    path("register", views.register, name='register'),
    path("login", views.login, name='login'),
    path("dashboard", views.dashboard, name='dashboard'),
    path("logout", views.logout, name='logout'),
    path("forgot-password", views.forgot_password, name='forgot-password'),
    path("reset-password/<uidb64>/<token>", views.reset_password, name='reset-password'),
    path("new_post", views.new_post, name='new_post'),
    path("edit_post/<int:post_id>", views.edit_post, name='edit_post'),
    path("delete_post/<slug:slug>", views.delete_post, name='delete_post'),
    path("publish_post/<slug:slug>", views.publish_post, name='publish_post'),
]