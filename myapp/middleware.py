from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        restricted_path=[reverse('blog:login'), reverse('blog:register')]
        if request.user.is_authenticated and request.path in restricted_path:
            return redirect('blog:index')
        return self.get_response(request)

class RedirectUnauthMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response
    def __call__(self, request):
        restricted_paths=[reverse('blog:dashboard')]
        if not request.user.is_authenticated and request.path in restricted_paths:
            return redirect('blog:index')
        return self.get_response(request)