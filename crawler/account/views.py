from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def jwt_response_payload_handler(token, user=None, request=None):
    # pass
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'msg' : 'success',
    }

@csrf_exempt
def auth_logout(request):
    logout(request)
    return redirect('/account/login/')




