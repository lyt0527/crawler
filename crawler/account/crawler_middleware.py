from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        a = ['/account/login/', '/account/logout/', '/account/api/v1/login/', '/function/navigator/',
             '/function/index/',
             '/function/comment/', '/function/judgement/', '/function/train/', '/function/rejudge/',
             '/function/message/','/export/export_all/','/receive/receive_all/']
        if request.path not in a:
            if request.META.get('HTTP_AUTHORIZATION'):
                print('111111111111111111111111111111111')
                pass
            else:
                print('222222222222222222222222')
                # return JsonResponse({'msg': "你没有权限访问，请与管理员联系。"})
                return HttpResponseRedirect('/account/logout/')