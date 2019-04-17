from django.shortcuts import render, redirect
import string
import datetime
from django.views.decorators.csrf import csrf_exempt
from function.models import *
from django.http import JsonResponse, HttpResponse
import json
from django.db import connection
from io import BytesIO
# Create your views here.
import base64
import datetime
import calendar
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def search(request):
    #validate(request)
    order_number = request.POST.get('orderNo', None)
    author_realname = request.POST.get('name', None)
    platform = request.POST.get('platform', None)
    author_tel = request.POST.get('tel', None)
    start_comment_time = request.POST.get('startTime')
    end_time = request.POST.get('endTime')
    start_arti_score = request.POST.get('lowScore')
    end_arti_score = request.POST.get('highScore')
    replys_count = request.POST.get('replyState', None)
    library = request.POST.get('library', None)
    current_page = int(request.POST.get('currentPage'))

    if library == "high":
        comment = Comments.objects.filter(arti_score__gt=0.5, is_scored=1)
    if library == "low":
        comment = Comments.objects.filter(arti_score__lte=0.5, is_scored=1)
        print(comment, '==========')
    # 评论未处理
    if library == "comment":
        comment = Comments.objects.filter(is_scored=0, type=2)
    # 评价未处理
    if library == "judgement":
        comment = Comments.objects.filter(is_scored=0, type=1)

    if not order_number and not author_realname and not author_tel and not platform and not start_arti_score and \
            not start_comment_time and not end_time and not end_arti_score and not replys_count:
        comment_list = []
        counts = 0
        start = (current_page-1) * 14
        end = current_page * 14
        for i in comment:
            counts += 1
        for i in comment[start:end]:
            comment_list.append({
                "comment_id": i.comment_id, "author_realname": i.author_realname, "platform": i.platform,
                "module":i.module, "catch_time": str(i.catch_time).split("T")[0],
                "comment_time": str(i.comment_time).split("T")[0], "arti_score": i.arti_score
            })
        pages = (counts // 14)
        if (counts % 14) != 0:
            pages += 1
        return JsonResponse({'msg': 'success', 'dic': comment_list, 'pages': pages})


    if order_number:
        data = comment.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)
    # 姓名不为空
    if author_realname:
        data = comment.filter(author_realname__contains=author_realname)
        if order_number:
            data = data.filter(order_number=order_number)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)
    # 手机号不为空
    if author_tel:
        data = comment.filter(author_tel__contains=author_tel)
        if order_number:
            data = data.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)

    # 来源不为空
    if platform:
        data = comment.filter(platform=platform)
        if order_number:
            data = data.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)
    if start_comment_time and end_time:
        data = comment.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if order_number:
            data = data.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)
    # 评分不为空
    if start_arti_score and end_arti_score:
        data = comment.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if order_number:
            data = data.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)
    if replys_count:
        if replys_count == "未回访":
            data = comment.filter(replys_count=0)
        else:
            data = comment.filter(replys_count__gte=1)
        if order_number:
            data = data.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)

    comment_list = []
    start = (current_page - 1) * 14
    end = (current_page * 14)
    counts = 0
    for i in data:
        counts += 1
    for i in data[start:end]:
        if i.platform:
            platform = i.platform
        else:
            platform = "---"
        comment_list.append({
            "comment_id": i.comment_id, "author_realname": i.author_realname, "platform": platform,
            "module":i.module, "catch_time": str(i.catch_time).split("T")[0],
            "comment_time": str(i.comment_time).split("T")[0], "arti_score": i.arti_score,
        })
    pages = (counts // 14)
    if (counts % 14) != 0:
        pages += 1
    return JsonResponse({'msg': 'success', 'dic': comment_list, 'pages': pages})