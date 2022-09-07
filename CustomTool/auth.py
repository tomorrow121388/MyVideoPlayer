from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        info = request.session.get("is_login")
        if info:
            return
        if request.path_info == '/login/' or request.path_info == '/' or request.path_info == '/register/':
            return

        return redirect('/login/')

    # def process_response(self, request, response):
    #     pass
    #     return response
