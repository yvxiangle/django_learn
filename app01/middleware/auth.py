from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse, render


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""
    def process_request(self, request):
        if request.path_info in ['/login/', '/image/code/']:
            return
        info_dict = request.session.get('info')
        if info_dict:
            return
        return redirect('/login/')
