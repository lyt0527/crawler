from time import sleep

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import *
from django.conf import settings  # 导入配置文件
from django.core.mail import send_mail  # 导入发送邮件的包
import json
from snownlp import sentiment,SnowNLP
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import base64
import datetime
import calendar
from django.contrib.auth import authenticate, login, logout

#navigator主页
@csrf_exempt
def count(request):
    #validate(request)
    #消息显示数量
    userid=request.POST.get('userid',None)
    if userid:
        news = News.objects.filter(is_ignored=0)
        low_comms_count = 0
        for i in news:
            low_comms_count += 1
        auth=AuthUser.objects.get(id=userid)
        username=auth.username
        # print(';;;;;;;;;;;;;;;;',low_comms_count)
        return JsonResponse({"msgNum":low_comms_count,"userName":username,"msg": "success"})
    else:
        news = News.objects.filter(is_ignored=0)
        low_comms_count = 0
        for i in news:
            low_comms_count += 1
        # print('...................',low_comms_count)
        return JsonResponse({"msgNum":low_comms_count,"msg": "success"})

@csrf_exempt
def count_day(request):
    #validate(request)

    time_today = datetime.datetime.now()
    zero_today = time_today - datetime.timedelta(hours = time_today.hour, minutes = time_today.minute,
                                    seconds = time_today.second,microseconds = time_today.microsecond)
    time_sevendays = time_today - datetime.timedelta(days=7)
    time_thirtydays = time_today - datetime.timedelta(days=30)
    # 评价未处理 今天
    eval_unprocesseds_day = Comments.objects.filter(is_scored=0, comment_time__gte=zero_today,
                                                     comment_time__lt=time_today,order_number__isnull=False)
    eval_unprocessed_day = 0
    for i in eval_unprocesseds_day:
        eval_unprocessed_day = eval_unprocessed_day + 1
    # 评价未处理 一周
    eval_unprocesseds_week = Comments.objects.filter(is_scored=0, comment_time__gte=time_sevendays,
                                                     comment_time__lt=time_today,order_number__isnull=False)
    eval_unprocessed_week = 0
    for i in eval_unprocesseds_week:
        eval_unprocessed_week = eval_unprocessed_week + 1
    # 评价未处理 一个月
    eval_unprocesseds_month = Comments.objects.filter(is_scored=0, comment_time__gte=time_thirtydays,
                                                     comment_time__lt=time_today,order_number__isnull=False)
    eval_unprocessed_month = 0
    for i in eval_unprocesseds_month:
        eval_unprocessed_month = eval_unprocessed_month + 1

    # 评论未处理 今天
    comm_unprocesseds_day = Comments.objects.filter(is_scored=0, comment_time__gte=zero_today,
                                                     comment_time__lt=time_today,order_number__isnull=True)
    comm_unprocessed_day = 0
    for i in comm_unprocesseds_day:
        comm_unprocessed_day = comm_unprocessed_day + 1
    # 评论未处理 一周
    comm_unprocesseds_week = Comments.objects.filter(is_scored=0, comment_time__gte=time_sevendays,
                                                     comment_time__lt=time_today,order_number__isnull=True)
    comm_unprocessed_week = 0
    for i in comm_unprocesseds_week:
        comm_unprocessed_week = comm_unprocessed_week + 1
    # 评论未处理 一个月
    comm_unprocesseds_month = Comments.objects.filter(is_scored=0, comment_time__gte=time_thirtydays,
                                                     comment_time__lt=time_today,order_number__isnull=True)
    comm_unprocessed_month = 0
    for i in comm_unprocesseds_month:
        comm_unprocessed_month = comm_unprocessed_month + 1

    # 低分已处理 今天
    low_processeds_day = Comments.objects.filter(arti_score__lte=0.5, is_scored=1, comment_time__gte=zero_today,
                                                     comment_time__lt=time_today)
    low_processed_day = 0
    for i in low_processeds_day:
        low_processed_day = low_processed_day + 1
    # 低分已处理 一周
    low_processeds_week = Comments.objects.filter(arti_score__lte=0.5, is_scored=1, comment_time__gte=time_sevendays,
                                                     comment_time__lt=time_today)
    low_processed_week = 0
    for i in low_processeds_week:
        low_processed_week = low_processed_week + 1
    # 低分已处理 一个月
    low_processeds_month = Comments.objects.filter(arti_score__lte=0.5, is_scored=1, comment_time__gte=time_thirtydays,
                                                     comment_time__lt=time_today)
    low_processed_month = 0
    for i in low_processeds_month:
        low_processed_month = low_processed_month + 1

    # 高分已处理 今天
    high_processeds_day = Comments.objects.filter(arti_score__gt=0.5, is_scored=1, comment_time__gte=zero_today,
                                                     comment_time__lt=time_today)
    high_processed_day = 0
    for i in high_processeds_day:
        high_processed_day = high_processed_day + 1
    # 高分已处理 一周
    high_processeds_week = Comments.objects.filter(arti_score__gt=0.5, is_scored=1, comment_time__gte=time_sevendays,
                                                     comment_time__lt=time_today)
    high_processed_week = 0
    for i in high_processeds_week:
        high_processed_week = high_processed_week + 1
    # 高分已处理 一个月
    high_processeds_month = Comments.objects.filter(arti_score__gt=0.5, is_scored=1, comment_time__gte=time_thirtydays,
                                                     comment_time__lt=time_today)
    high_processed_month = 0
    for i in high_processeds_month:
        high_processed_month = high_processed_month + 1
    return JsonResponse({"judgementToday": eval_unprocessed_day,"judgementWeek": eval_unprocessed_week,
                         "judgementMonth": eval_unprocessed_month,"commentToday": comm_unprocessed_day,
                         "commentWeek": comm_unprocessed_week,
                         "commentMonth": comm_unprocessed_month,"lowToday": low_processed_day,
                         "lowWeek": low_processed_week,"lowMonth": low_processed_month,
                         "highToday": high_processed_day,"highWeek": high_processed_week,
                         "highMonth": high_processed_month,"msg": "success"})

#看板
@csrf_exempt
def plotting(request):
    #validate(request)
    time_sta=request.POST.get("startTime", None)
    time_en=request.POST.get("endTime", None)
    score_type=request.POST.get("type", None)
    now = datetime.datetime.now()
    zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond)
    lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
    one_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
    if time_sta==datetime.datetime.strftime(now,"%Y-%m-%d") and time_en==datetime.datetime.strftime(now,"%Y-%m-%d") :
        time_start = zeroToday
        time_end = now
    else :
        time_start = datetime.datetime.strptime(time_sta + " 00:00:00", "%Y-%m-%d 00:00:00")
        time_end = datetime.datetime.strptime(time_en + " 23:59:59", "%Y-%m-%d 23:59:59")
    #一天
    if time_end-time_start<=one_day:
        comms_list = []
        dateList = []
        sum = []
        charge = []
        secondHand = []
        customer = []
        Eplus = []
        experience = []
        mall = []
        service = []
        #当天
        if time_start>=zeroToday:
            time_hour = str(datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second))
            time_interval = int(time_hour.split(":")[0])
            floor = time_interval // 2
            i = 0
            while i < floor:
                time_middle = time_start + datetime.timedelta(hours = 2)
                if score_type == "0" or not score_type :
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge").count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand").count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer").count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus").count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience").count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall").count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service").count()
                    service.append(time_comms)
                if score_type == "2":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, arti_score__lte=0.5).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", arti_score__lte=0.5).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", arti_score__lte=0.5).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", arti_score__lte=0.5).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", arti_score__lte=0.5).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", arti_score__lte=0.5).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", arti_score__lte=0.5).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", arti_score__lte=0.5).count()
                    service.append(time_comms)
                if score_type == "1":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, arti_score__gt=0.5).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", arti_score__gt=0.5).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", arti_score__gt=0.5).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", arti_score__gt=0.5).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", arti_score__gt=0.5).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", arti_score__gt=0.5).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", arti_score__gt=0.5).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", arti_score__gt=0.5).count()
                    service.append(time_comms)
                if score_type == "3":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, is_scored=0).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", is_scored=0).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", is_scored=0).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", is_scored=0).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", is_scored=0).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", is_scored=0).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", is_scored=0).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", is_scored=0).count()
                    service.append(time_comms)
                time_start = time_middle
                i += 1
            return JsonResponse({"msg": "success", "sum": sum, "charge" : charge, "secondHand":secondHand,
                                 "customer":customer, "Eplus":Eplus, "experience":experience, "mall":mall,
                                 "service":service,"dateList": dateList})
        #之前的某一天
        else:
            i=0
            while i < 12:
                time_middle = time_start + datetime.timedelta(hours=2)
                if score_type == "0":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge").count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand").count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer").count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus").count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience").count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall").count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service").count()
                    service.append(time_comms)
                if score_type == "2":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, arti_score__lte=0.5).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", arti_score__lte=0.5).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", arti_score__lte=0.5).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", arti_score__lte=0.5).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", arti_score__lte=0.5).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", arti_score__lte=0.5).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", arti_score__lte=0.5).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", arti_score__lte=0.5).count()
                    service.append(time_comms)
                if score_type == "1":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, arti_score__gt=0.5).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", arti_score__gt=0.5).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", arti_score__gt=0.5).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", arti_score__gt=0.5).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", arti_score__gt=0.5).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", arti_score__gt=0.5).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", arti_score__gt=0.5).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", arti_score__gt=0.5).count()
                    service.append(time_comms)
                if score_type == "3":
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                         platform__isnull=False, is_scored=0).count()
                    sum.append(time_comms)
                    dateList.append(datetime.datetime.strftime(time_middle, "%H"))
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="charge", is_scored=0).count()
                    charge.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="secondHand", is_scored=0).count()
                    secondHand.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="customer", is_scored=0).count()
                    customer.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="Eplus", is_scored=0).count()
                    Eplus.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="experience", is_scored=0).count()
                    experience.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="mall", is_scored=0).count()
                    mall.append(time_comms)
                    time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                         comment_time__gte=time_start,
                                                         platform="service", is_scored=0).count()
                    service.append(time_comms)

                time_start = time_middle
                i += 1
            return JsonResponse({"msg": "success", "sum": sum, "charge" : charge, "secondHand":secondHand,
                                 "customer":customer, "Eplus":Eplus, "experience":experience, "mall":mall,
                                 "service":service,"dateList": dateList})
    #大于一天小于31天
    elif time_end-time_start<datetime.timedelta(days=31) and time_end-time_start>one_day:
        time_day = str(time_end - time_start)
        time_inter = (time_day.split(",")[0]).split(" ")[0]
        time_count = int(time_inter)
        comms_list = []
        dateList = []
        sum = []
        charge = []
        secondHand = []
        customer = []
        Eplus = []
        experience = []
        mall = []
        service = []
        i = 0
        while i <= time_count:
            time_middle=time_start+datetime.timedelta(days=1)
            if score_type == "0":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_start, "%m%d"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge").count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand").count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer").count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus").count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience").count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall").count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service").count()
                service.append(time_comms)
            if score_type == "2":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__lte=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%m%d"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__lte=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__lte=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__lte=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__lte=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__lte=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__lte=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__lte=0.5).count()
                service.append(time_comms)
            if score_type == "1":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__gt=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%m%d"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__gt=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__gt=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__gt=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__gt=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__gt=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__gt=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__gt=0.5).count()
                service.append(time_comms)
            if score_type == "3":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, is_scored=0).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%m%d"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", is_scored=0).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", is_scored=0).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", is_scored=0).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", is_scored=0).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", is_scored=0).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", is_scored=0).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", is_scored=0).count()
                service.append(time_comms)
            time_start = time_middle
            i += 1
        return JsonResponse({"msg": "success", "sum": sum, "charge" : charge, "secondHand":secondHand,
                                 "customer":customer, "Eplus":Eplus, "experience":experience, "mall":mall,
                                 "service":service,"dateList": dateList})
    #大于31天
    elif time_end-time_start>datetime.timedelta(days=31) and time_end-time_start<datetime.timedelta(days=366):
        time_curmonth = str(time_end).split(" ")[0].split("-")[2]
        time_curmonth = int(time_curmonth)
        now_years = int(str(time_end).split(" ")[0].split("-")[0])
        now_months = int(str(time_end).split(" ")[0].split("-")[1])
        time_months = str(time_end - time_start)
        time_inter = (time_months.split(",")[0]).split(" ")[0]
        time_inter = int(time_inter)
        time_month = (time_inter - time_curmonth)//30+1
        dateList = []
        sum = []
        charge = []
        secondHand = []
        customer = []
        Eplus = []
        experience = []
        mall = []
        service = []
        i = time_month
        while i >= 0 :
            if i >= 0 and now_months - i > 0:
                monthRange = calendar.monthrange(now_years, now_months-i)
                now_days = monthRange[1]
                time_start = datetime.datetime.strptime(str(now_years)+"-"+str(now_months-i)+"-1"+" 00:00:00",
                                                        "%Y-%m-%d %H:%M:%S")
                time_middle = datetime.datetime.strptime(str(now_years)+"-"+str(now_months-i)+"-"+str(now_days)+" 23:59:59",
                                                         "%Y-%m-%d %H:%M:%S")
            elif i >= 0 and now_months - i <= 0:
                monthRange = calendar.monthrange(now_years-1, 12+now_months-i)
                now_days = monthRange[1]
                time_start = datetime.datetime.strptime(str(now_years-1)+"-"+str(12+now_months-i)+"-1"+" 00:00:00",
                                                        "%Y-%m-%d %H:%M:%S")
                time_middle = datetime.datetime.strptime(str(now_years-1)+"-"+str(12+now_months-i)+"-"+str(now_days)+" 23:59:59",
                                                         "%Y-%m-%d %H:%M:%S")
            # print(time_start,time_middle)
            if score_type == "0":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y%m"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge").count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand").count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer").count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus").count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience").count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall").count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service").count()
                service.append(time_comms)
            if score_type == "2":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__lte=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y%m"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__lte=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__lte=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__lte=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__lte=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__lte=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__lte=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__lte=0.5).count()
                service.append(time_comms)
            if score_type == "1":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__gt=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y%m"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__gt=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__gt=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__gt=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__gt=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__gt=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__gt=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__gt=0.5).count()
                service.append(time_comms)
            if score_type == "3":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, is_scored=0).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y%m"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", is_scored=0).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", is_scored=0).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", is_scored=0).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", is_scored=0).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", is_scored=0).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", is_scored=0).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", is_scored=0).count()
                service.append(time_comms)
            i -= 1
        return JsonResponse({"msg": "success", "sum": sum, "charge": charge, "secondHand": secondHand,
                             "customer": customer, "Eplus": Eplus, "experience": experience, "mall": mall,
                             "service": service, "dateList": dateList})
    # 大于366天
    elif time_end - time_start > datetime.timedelta(days=366):
        time_curmonth = str(time_end).split(" ")[0].split("-")[2]
        time_curmonth = int(time_curmonth)
        now_years = int(str(time_end).split(" ")[0].split("-")[0])
        now_months = int(str(time_end).split(" ")[0].split("-")[1])
        time_years = str(time_end - time_start)
        # print(time_years,'11111111111111111111')
        time_inter = (time_years.split(",")[0]).split(" ")[0]
        time_inter = int(time_inter)
        time_month = (time_inter - time_curmonth) // 366
        dateList = []
        sum = []
        charge = []
        secondHand = []
        customer = []
        Eplus = []
        experience = []
        mall = []
        service = []
        i = time_month
        while i >= 0:
            time_start = datetime.datetime.strptime(
                str(now_years - i) + "-1-1" + " 00:00:00", "%Y-%m-%d %H:%M:%S")
            time_middle = datetime.datetime.strptime(
                str(now_years - i) + "-12-31" + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                # print(time_start,time_middle)
            # print('11111111111111111111111',time_start,time_middle)
            if score_type == "0":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge").count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand").count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer").count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus").count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience").count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall").count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service").count()
                service.append(time_comms)
            if score_type == "2":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__lte=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__lte=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__lte=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__lte=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__lte=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__lte=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__lte=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__lte=0.5).count()
                service.append(time_comms)
            if score_type == "1":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, arti_score__gt=0.5).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", arti_score__gt=0.5).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", arti_score__gt=0.5).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", arti_score__gt=0.5).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", arti_score__gt=0.5).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", arti_score__gt=0.5).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", arti_score__gt=0.5).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", arti_score__gt=0.5).count()
                service.append(time_comms)
            if score_type == "3":
                time_comms = Comments.objects.filter(comment_time__lte=time_middle, comment_time__gte=time_start,
                                                     platform__isnull=False, is_scored=0).count()
                sum.append(time_comms)
                dateList.append(datetime.datetime.strftime(time_middle, "%Y"))
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="charge", is_scored=0).count()
                charge.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="secondHand", is_scored=0).count()
                secondHand.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="customer", is_scored=0).count()
                customer.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="Eplus", is_scored=0).count()
                Eplus.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="experience", is_scored=0).count()
                experience.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="mall", is_scored=0).count()
                mall.append(time_comms)
                time_comms = Comments.objects.filter(comment_time__lte=time_middle,
                                                     comment_time__gte=time_start,
                                                     platform="service", is_scored=0).count()
                service.append(time_comms)
            i -= 1
        return JsonResponse({"msg": "success", "sum": sum, "charge": charge, "secondHand": secondHand,
                             "customer": customer, "Eplus": Eplus, "experience": experience, "mall": mall,
                             "service": service, "dateList": dateList})
#消息
@csrf_exempt
def news(request):
    #validate(request)
    # low_comms1 = Comments.objects.filter(comment_score__lte = 1)
    # low_comms2 = Comments.objects.filter(comment_stars__lte = 1)
    # low_comms3 = Comments.objects.filter(arti_score__lte = 0.1, is_scored = 1)
    low_comms = News.objects.filter(is_ignored=0)
    current_page=int(request.POST.get('currentPage'))
    start = (current_page - 1) * 10
    end = (current_page * 10)
    low_list=[]
    low_counts = 0
    for i in low_comms:
        low_counts = low_counts + 1
    for i in low_comms[start:end]:
        c_id=News.objects.get(comment_id=i.comment_id)
        if c_id.type==1:
            comment_type="评价"
        else:
            comment_type="评论"
        if c_id.comment_time:
            comment_time = str(i.comment_time).split("T")
        else:
            comment_time = "---"
        if c_id.catch_time:
            catch_time = str(i.catch_time).split("T")
        else:
            catch_time = "---"
        if c_id.platform:
            platform = i.platform
        else:
            platform = "---"
        if c_id.otherside_address:
            comment_address = i.otherside_address
        else:
            comment_address = "---"
        if c_id.author_realname:
            author_realname = i.author_realname
        else:
            author_realname = "---"
        if c_id.comment_score:
            comment_score = i.comment_score
        else:
            comment_score = "---"
        if c_id.comment_star:
            comment_star = i.comment_star
        else:
            comment_star = "---"
        low_list.append({"comment_id" : i.comment_id, "comment_time" : comment_time, "platform" : platform,
                         "comment_content" : i.comment_content, "arti_score" : i.arti_score,
                         "comment_score":comment_score,"alert_time":i.alert_time,"comment_star":comment_star,
                         "author_realname":author_realname,"author_tel":i.author_tel,"catch_time":catch_time,
                         "order_number":i.order_number,"is_read":i.is_read,"comment_type":comment_type,
                         "comment_address":comment_address})
    pages = (low_counts // 10)
    if low_counts % 10 != 0:
        pages = pages + 1
    return JsonResponse({"msg":"success","low_list":low_list})

@csrf_exempt
def all_page(request):
    #validate(request)
    low_comms = News.objects.filter(is_ignored=0)
    low_count=0
    for i in low_comms:
        low_count += 1
    pages = (low_count // 10)
    if low_count % 10 != 0:
        pages = pages +1
    return JsonResponse({"msg":"success","allPage":pages})


#查看消息
@csrf_exempt
def check_news(request):
    #validate(request)
    pass
    # page_current = request.POST.get("page_current", None)
    # page_current = int(page_current)
    # # page_current = 1 if page_current==None else page_current
    # start = (page_current - 1) * 10
    # end = (page_current * 10)
    #
    # news_comms = Comments.objects.filter(arti_score__lte=0.1, order_number__isnull=False, is_ignore=1)
    # news_list = []
    # news_comm = 0
    # for i in news_comms:
    #     news_comm = news_comm + 1
    # for i in news_comms[start:end]:
    #     news_list.append({"id": i.comment_id,"catch_time": i.catch_time,"comment_time": i.comment_time,
    #                      "final_score": i.sys_score,"author_realname":i.author_realname, "platform":i.platform})
    #
    # pages = (news_comm // 10)
    # if news_comm % 10 != 0:
    #     pages = pages +1
    # print(news_list[0])
    # return JsonResponse({"msg": "success", "items": news_list, "pages": pages})

#忽略消息
@csrf_exempt
def is_ignore(request):
    #validate(request)
    comment_id=request.POST.get("id")
    News.objects.filter(comment_id=comment_id).update(is_ignored=1)
    return JsonResponse({"msg":"success"})

@csrf_exempt
def index(request):
    return render(request, "function/index.html")

@csrf_exempt
def navigator(request):
    return render(request, "function/navigator.html")

@csrf_exempt
def comment(request):
    return render(request, "function/comment.html")

@csrf_exempt
def judgement(request):
    return render(request, "function/judgement.html")

@csrf_exempt
def train(request):
    return render(request, "function/train.html")

@csrf_exempt
def rejudge(request):
    return render(request, "function/rejudge.html")

@csrf_exempt
def message(request):
    return render(request, "function/message.html")

@csrf_exempt
def admin(request):
    return redirect(request, "admin/index.html")


@csrf_exempt
def count1(request):
    # #validate(request)
    comment_id = int(request.POST.get("comment_id"))
    comment = Comments.objects.get(comment_id = comment_id)
    low_comment = []
    low_comments = Comments.objects.filter(sys_score__lte = 0.5)
    for x in (low_comments):
        low_comment.append(x.comment_id)
    if comment.is_scored == 0:
        library = "unprocessed"
        dic = {"msg": "success", "library": library, "comment_id": comment_id}
        return HttpResponse(json.dumps(dic))
    else:
        if comment.comment_id in low_comment:
            library = "low_processed"
            dic = {"msg" : "success", "library" : library, "comment_id" : comment_id}
            return HttpResponse(json.dumps(dic))
        else:
            library = "high_processed"
            dic = {"msg" : "success", "library" : library, "comment_id" : comment_id}
            return HttpResponse(json.dumps(dic))

#评论详情
@csrf_exempt
def comment_content(request):
    #validate(request)
    comment_Id = int(request.POST.get("id", None))
    id = News.objects.filter(comment_id=comment_Id)
    if id:
        News.objects.filter(comment_id=comment_Id).update(is_read=1)
        new=News.objects.get(comment_id=comment_Id)
        type = new.type
        if new.comment_time:
            comment_time = str(new.comment_time).split(" ")[0] + " " + str(new.comment_time).split(" ")[1]
        else:
            comment_time = "---"
        if new.catch_time:
            catch_time = str(new.catch_time).split(" ")[0] + " " + str(new.catch_time).split(" ")[1]
        else:
            catch_time = "---"
        if new.platform:
            platform = new.platform
        else:
            platform = "---"
        if new.otherside_address:
            comment_address = new.otherside_address
        else:
            comment_address = "---"
        if new.author_nickname:
            author_nickname = new.author_nickname
        else:
            author_nickname = "---"
        if new.author_realname:
            author_realname = new.author_realname
        else:
            author_realname = "---"
        if new.author_tel:
            author_tel = new.author_tel
        else:
            author_tel = "---"
        if new.sys_score:
            sys_score = new.sys_score
        else:
            sys_score = "---"
        if new.arti_score:
            arti_score = new.arti_score
        else:
            arti_score = "---"
        dict2 = [{"comment_id": new.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": new.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": new.author_id,
                  "author_nickname": author_nickname, "comment_stars": new.comment_star,
                  "order_number": new.order_number, "comment_score": new.comment_score, "is_read": new.is_read,
                  "is_ignored": new.is_ignored, "source": new.source, "platform":platform,"type":new.type}]
        # print('111111111111111111111111111', dict2)
    else:
        comment = Comments.objects.get(comment_id=comment_Id)
        type=comment.type
        if comment.comment_time:
            comment_time = str(comment.comment_time).split(" ")[0] + " " + str(comment.comment_time).split(" ")[1]
        else:
            comment_time = "---"
        if comment.catch_time:
            catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
        else:
            catch_time = "---"
        if comment.platform:
            platform = comment.platform
        else:
            platform = "---"
        if comment.otherside_address:
            comment_address = comment.otherside_address
        else:
            comment_address = "---"
        if comment.author_nickname:
            author_nickname = comment.author_nickname
        else:
            author_nickname = "---"
        if comment.author_realname:
            author_realname = comment.author_realname
        else:
            author_realname = "---"
        if comment.author_tel:
            author_tel = comment.author_tel
        else:
            author_tel = "---"
        if comment.sys_score:
            sys_score = comment.sys_score
        else:
            sys_score = "---"
        if comment.arti_score:
            arti_score = comment.arti_score
        else:
            arti_score = "---"
        # print('comment.sys_score',comment.sys_score)
        dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
        # print('222222222222222222222222222222',dict2)
    return JsonResponse({"msg" : "success", "dic" : dict2})


@csrf_exempt
# 人工评分
def submit_newscore(request):
    #validate(request)
    comment_current_id = request.POST.get('No')
    new_score = request.POST.get('newScore')
    # print('id',comment_current_id, new_score)
    # print(new_score)
    # print(type(new_score))
    # new_score = float(new_score)
    if new_score == 0 or new_score == '0':
        new_score = 0
    else:
        new_score = float(new_score)
    if new_score or new_score == 0:
        alert_time=datetime.datetime.now()
        Comments.objects.filter(comment_id = comment_current_id).update(arti_score=new_score, is_scored=1)
        if new_score>0.1:
            # print('1111111111111111111111111')
            News.objects.filter(comment_id=comment_current_id).update(arti_score=new_score, is_ignored=1, is_read=0)
            return JsonResponse({"msg": "success"})
        if new_score <= 0.1:
            # print('222222222222222222222222')
            id = News.objects.filter(comment_id=comment_current_id)
            if not id:
                c = Comments.objects.get(comment_id = comment_current_id)
                News.objects.create(comment_id=comment_current_id,comment_time=c.comment_time,alert_time=alert_time,
                                    comment_content=c.comment_content,comment_star=c.comment_stars,
                                    comment_score=c.comment_score,comment_type=c.comment_type,
                                    author_realname=c.author_realname,author_tel=c.author_tel,platform=c.platform,
                                    order_number=c.order_number,sys_score=c.sys_score,arti_score=c.arti_score,
                                    catch_time=c.catch_time,type=c.type,source=c.source,
                                    otherside_address=c.otherside_address,author_nickname=c.author_nickname,
                                    comment_images=c.comment_images,add_comments=c.add_comments,author_id=c.author_id,
                                    otherside_comment_id=c.otherside_comment_id,module=c.module,is_ignored=0,is_read=0)#is_ignored=0 关注 is_read=0未读
            else:
                News.objects.filter(comment_id=comment_current_id).update(arti_score=new_score,is_ignored=0,is_read=0)
            return JsonResponse({"msg" : "success"})
    else:
        return JsonResponse({"msg" : "failure"})


#翻页
@csrf_exempt
def changeitems(request):
    #validate(request)
    comment_id = int(request.POST.get("id", None))
    target = request.POST.get('item', None)
    order_number = request.POST.get('orderNo', None)
    author_realname = request.POST.get('name', None)
    platform = request.POST.get('platform', None)
    author_tel = request.POST.get('tel', None)
    start_comment_time = request.POST.get('startTime', None)
    end_comment_time = request.POST.get('endTime', None)
    start_arti_score = request.POST.get('lowScore', None)
    end_arti_score = request.POST.get('highScore', None)
    replys_count = request.POST.get('replyState', None)
    library = request.POST.get('library', None)

    # print(comment_id,'11111111111111111111')
    # #当不输入时间时
    # if start_comment_time == '' and end_comment_time == '' or not start_comment_time and not end_comment_time:
    #     start_comment_time = datetime.datetime.now()
    #     year = start_comment_time.year
    #     month = start_comment_time.month
    #     day = start_comment_time.day
    #     end_time = str(year) + '-' + str(month) + '-' + str(day)
    #     start_comment_time = str(year-30) + '-' + str(month) + '-' + str(day)
    #     start_comment_time = datetime.datetime.strptime(start_comment_time, '%Y-%m-%d')
    #     end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    # else:
    #     start_comment_time = datetime.datetime.strptime(start_comment_time, '%Y-%m-%d')
    #     end_time = datetime.datetime.strptime(end_comment_time, '%Y-%m-%d') + datetime.timedelta(days=1)

    if library == "high":
        comment = Comments.objects.filter(arti_score__gt=0.5, is_scored=1)
    if library == "low":
        comment = Comments.objects.filter(arti_score__lte=0.5, is_scored=1)
    # 评价未处理
    if library == "comment":
        comment = Comments.objects.filter(is_scored=0, order_number__isnull=True)
    # 评论未处理
    if library == "judgement":
        comment = Comments.objects.filter(is_scored=0, order_number__isnull=False)  # 没有order_number为评论

    if not order_number and not author_realname and not platform and not author_tel and not start_comment_time \
            and not end_comment_time and not start_arti_score and not end_arti_score and not replys_count:
        commentLi = comment
        list = []
        for i in commentLi:
            list.append(i.comment_id)
        # 上一页
        if target == "上一条":
            commentList = []
            for x in commentLi:
                if x.comment_id < comment_id:
                    commentList.append(x.comment_id)
            if commentList == []:
                comment = Comments.objects.get(comment_id=list[-1])
                if comment.comment_time:
                    comment_time = str(comment.comment_time).split(" ")[0] + " " + str(comment.comment_time).split(" ")[
                        1]
                else:
                    comment_time = "---"
                if comment.catch_time:
                    catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
                else:
                    catch_time = "---"
                if comment.platform:
                    platform = comment.platform
                else:
                    platform = "---"
                if comment.otherside_address:
                    comment_address = comment.otherside_address
                else:
                    comment_address = "---"
                if comment.author_nickname:
                    author_nickname = comment.author_nickname
                else:
                    author_nickname = "---"
                if comment.author_realname:
                    author_realname = comment.author_realname
                else:
                    author_realname = "---"
                if comment.author_tel:
                    author_tel = comment.author_tel
                else:
                    author_tel = "---"
                if comment.sys_score:
                    sys_score = comment.sys_score
                else:
                    sys_score = "---"
                if comment.arti_score:
                    arti_score = comment.arti_score
                else:
                    arti_score = "---"
                dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                return JsonResponse({"msg": "success", "dic": dict2})
            else:
                for y in commentList[::-1]:
                    if comment_id - y > 0:
                        comment = Comments.objects.get(comment_id=y)
                        if comment.comment_time:
                            comment_time = str(comment.comment_time).split(" ")[0] + " " + \
                                           str(comment.comment_time).split(" ")[1]
                        else:
                            comment_time = "---"
                        if comment.catch_time:
                            catch_time = str(comment.catch_time).split(" ")[0] + " " + \
                                         str(comment.catch_time).split(" ")[1]
                        else:
                            catch_time = "---"
                        if comment.platform:
                            platform = comment.platform
                        else:
                            platform = "---"
                        if comment.otherside_address:
                            comment_address = comment.otherside_address
                        else:
                            comment_address = "---"
                        if comment.author_nickname:
                            author_nickname = comment.author_nickname
                        else:
                            author_nickname = "---"
                        if comment.author_realname:
                            author_realname = comment.author_realname
                        else:
                            author_realname = "---"
                        if comment.author_tel:
                            author_tel = comment.author_tel
                        else:
                            author_tel = "---"
                        if comment.sys_score:
                            sys_score = comment.sys_score
                        else:
                            sys_score = "---"
                        if comment.arti_score:
                            arti_score = comment.arti_score
                        else:
                            arti_score = "---"
                        dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                        return JsonResponse({"msg": "success", "dic": dict2})
                    else:
                        return JsonResponse({"msg": "failure"})
        # 下一页
        elif target == "下一条":
            commentList = []
            for x in commentLi:
                if x.comment_id > comment_id:
                    commentList.append(x.comment_id)
            if commentList == []:
                comment = Comments.objects.get(comment_id=list[0])
                if comment.comment_time:
                    comment_time = str(comment.comment_time).split(" ")[0] + " " + str(comment.comment_time).split(" ")[
                        1]
                else:
                    comment_time = "---"
                if comment.catch_time:
                    catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
                else:
                    catch_time = "---"
                if comment.platform:
                    platform = comment.platform
                else:
                    platform = "---"
                if comment.otherside_address:
                    comment_address = comment.otherside_address
                else:
                    comment_address = "---"
                if comment.author_nickname:
                    author_nickname = comment.author_nickname
                else:
                    author_nickname = "---"
                if comment.author_realname:
                    author_realname = comment.author_realname
                else:
                    author_realname = "---"
                if comment.author_tel:
                    author_tel = comment.author_tel
                else:
                    author_tel = "---"
                if comment.sys_score:
                    sys_score = comment.sys_score
                else:
                    sys_score = "---"
                if comment.arti_score:
                    arti_score = comment.arti_score
                else:
                    arti_score = "---"
                dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                return JsonResponse({"msg": "success", "dic": dict2})
            else:
                for y in commentList:
                    if y - comment_id > 0:
                        comment = Comments.objects.get(comment_id=y)
                        if comment.comment_time:
                            comment_time = str(comment.comment_time).split(" ")[0] + " " + \
                                           str(comment.comment_time).split(" ")[1]
                        else:
                            comment_time = "---"
                        if comment.catch_time:
                            catch_time = str(comment.catch_time).split(" ")[0] + " " + \
                                         str(comment.catch_time).split(" ")[1]
                        else:
                            catch_time = "---"
                        if comment.platform:
                            platform = comment.platform
                        else:
                            platform = "---"
                        if comment.otherside_address:
                            comment_address = comment.otherside_address
                        else:
                            comment_address = "---"
                        if comment.author_nickname:
                            author_nickname = comment.author_nickname
                        else:
                            author_nickname = "---"
                        if comment.author_realname:
                            author_realname = comment.author_realname
                        else:
                            author_realname = "---"
                        if comment.author_tel:
                            author_tel = comment.author_tel
                        else:
                            author_tel = "---"
                        if comment.sys_score:
                            sys_score = comment.sys_score
                        else:
                            sys_score = "---"
                        if comment.arti_score:
                            arti_score = comment.arti_score
                        else:
                            arti_score = "---"
                        dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                        return JsonResponse({"msg": "success", "dic": dict2})
                    else:
                        return JsonResponse({"msg": "failure"})


    # 订单号不为空
    if order_number:
        data = comment.filter(order_number=order_number)
        if author_realname:
            data = data.filter(author_realname__contains=author_realname)
        if platform:
            data = data.filter(platform=platform)
        if author_tel:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_comment_time:
            data =data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
        if start_arti_score and end_arti_score is not None:
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
        if author_tel is not None:
            data = data.filter(author_tel__contains=author_tel)
        if start_comment_time and end_comment_time:
            data =data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
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
        if start_comment_time and end_comment_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
        if start_arti_score and end_arti_score is not None:
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
        if start_comment_time and end_comment_time:
            data =data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
        if replys_count:
            if replys_count == "未回访":
                data = data.filter(replys_count=0)
            else:
                data = data.filter(replys_count__gte=1)

    if start_comment_time and end_comment_time:
        data = comment.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
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
        if start_comment_time and end_comment_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
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
        if start_comment_time and end_comment_time:
            data = data.filter(comment_time__gte=start_comment_time, comment_time__lte=end_comment_time)
        if start_arti_score and end_arti_score:
            data = data.filter(arti_score__gte=start_arti_score, arti_score__lte=end_arti_score)
    commentLi=data
    list = []
    for i in commentLi:
        list.append(i.comment_id)
    # 上一页
    if target == "上一条":
        commentList = []
        for x in commentLi:
            if x.comment_id < comment_id:
                commentList.append(x.comment_id)
        if commentList == []:
            comment = Comments.objects.get(comment_id=list[-1])
            if comment.comment_time:
                comment_time = str(comment.comment_time).split(" ")[0] + " " + str(comment.comment_time).split(" ")[1]
            else:
                comment_time = "---"
            if comment.catch_time:
                catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
            else:
                catch_time = "---"
            if comment.platform:
                platform = comment.platform
            else:
                platform = "---"
            if comment.otherside_address:
                comment_address = comment.otherside_address
            else:
                comment_address = "---"
            if comment.author_nickname:
                author_nickname = comment.author_nickname
            else:
                author_nickname = "---"
            if comment.author_realname:
                author_realname = comment.author_realname
            else:
                author_realname = "---"
            if comment.author_tel:
                author_tel = comment.author_tel
            else:
                author_tel = "---"
            if comment.sys_score:
                sys_score = comment.sys_score
            else:
                sys_score = "---"
            if comment.arti_score:
                arti_score = comment.arti_score
            else:
                arti_score = "---"
            dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
            return JsonResponse({"msg": "success", "dic": dict2})
        else:
            for y in commentList[::-1]:
                if comment_id - y > 0:
                    comment = Comments.objects.get(comment_id=y)
                    if comment.comment_time:
                        comment_time = str(comment.comment_time).split(" ")[0] + " " + \
                                       str(comment.comment_time).split(" ")[1]
                    else:
                        comment_time = "---"
                    if comment.catch_time:
                        catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
                    else:
                        catch_time = "---"
                    if comment.platform:
                        platform = comment.platform
                    else:
                        platform = "---"
                    if comment.otherside_address:
                        comment_address = comment.otherside_address
                    else:
                        comment_address = "---"
                    if comment.author_nickname:
                        author_nickname = comment.author_nickname
                    else:
                        author_nickname = "---"
                    if comment.author_realname:
                        author_realname = comment.author_realname
                    else:
                        author_realname = "---"
                    if comment.author_tel:
                        author_tel = comment.author_tel
                    else:
                        author_tel = "---"
                    if comment.sys_score:
                        sys_score = comment.sys_score
                    else:
                        sys_score = "---"
                    if comment.arti_score:
                        arti_score = comment.arti_score
                    else:
                        arti_score = "---"
                    dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                    return JsonResponse({"msg": "success", "dic": dict2})
                else:
                    return JsonResponse({"msg": "failure"})
    # 下一页
    elif target == "下一条":
        commentList = []
        for x in commentLi:
            if x.comment_id > comment_id:
                commentList.append(x.comment_id)
        if commentList == []:
            comment = Comments.objects.get(comment_id=list[0])
            if comment.comment_time:
                comment_time = str(comment.comment_time).split(" ")[0] + " " + str(comment.comment_time).split(" ")[1]
            else:
                comment_time = "---"
            if comment.catch_time:
                catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
            else:
                catch_time = "---"
            if comment.platform:
                platform = comment.platform
            else:
                platform = "---"
            if comment.otherside_address:
                comment_address = comment.otherside_address
            else:
                comment_address = "---"
            if comment.author_nickname:
                author_nickname = comment.author_nickname
            else:
                author_nickname = "---"
            if comment.author_realname:
                author_realname = comment.author_realname
            else:
                author_realname = "---"
            if comment.author_tel:
                author_tel = comment.author_tel
            else:
                author_tel = "---"
            if comment.sys_score:
                sys_score = comment.sys_score
            else:
                sys_score = "---"
            if comment.arti_score:
                arti_score = comment.arti_score
            else:
                arti_score = "---"
            dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
            return JsonResponse({"msg": "success", "dic": dict2})
        else:
            for y in commentList:
                if y - comment_id > 0:
                    comment = Comments.objects.get(comment_id=y)
                    if comment.comment_time:
                        comment_time = str(comment.comment_time).split(" ")[0] + " " + \
                                       str(comment.comment_time).split(" ")[1]
                    else:
                        comment_time = "---"
                    if comment.catch_time:
                        catch_time = str(comment.catch_time).split(" ")[0] + " " + str(comment.catch_time).split(" ")[1]
                    else:
                        catch_time = "---"
                    if comment.platform:
                        platform = comment.platform
                    else:
                        platform = "---"
                    if comment.otherside_address:
                        comment_address = comment.otherside_address
                    else:
                        comment_address = "---"
                    if comment.author_nickname:
                        author_nickname = comment.author_nickname
                    else:
                        author_nickname = "---"
                    if comment.author_realname:
                        author_realname = comment.author_realname
                    else:
                        author_realname = "---"
                    if comment.author_tel:
                        author_tel = comment.author_tel
                    else:
                        author_tel = "---"
                    if comment.sys_score:
                        sys_score = comment.sys_score
                    else:
                        sys_score = "---"
                    if comment.arti_score:
                        arti_score = comment.arti_score
                    else:
                        arti_score = "---"
                    dict2 = [{"comment_id": comment.comment_id, "comment_address": comment_address,
                  "catch_time": catch_time, "comment_time": comment_time,
                  "sys_score": sys_score, "comment_content": comment.comment_content,
                  'arti_score': arti_score, "tel": author_tel,
                  "author_realname": author_realname, "author_id": comment.author_id,
                  "author_nickname": author_nickname, "comment_stars": comment.comment_stars,
                  "order_number": comment.order_number, "comment_score": comment.comment_score,
                  "source": comment.source, "platform":platform,"type":comment.type}]
                    return JsonResponse({"msg": "success", "dic": dict2})
                else:
                    return JsonResponse({"msg": "failure"})


@csrf_exempt
def last_rejudge(request):
    #validate(request)
    sys_id = SysScore.objects.filter().order_by("-id")[0]
    sys_time=str(sys_id.sys_score_time)
    sys_time=sys_time.split(" ")[0]+"\n"+sys_time.split(" ")[1]
    return JsonResponse({"msg": "success", "last_rate": sys_id.precision_rate, "last_sum": sys_id.sum,
                         "last_correct": sys_id.correct, "last_wrong": sys_id.wrong,
                         "last_sys_time": sys_time})

@csrf_exempt
def precision(request):
    #validate(request)
    #重新系统评分
    # samples = Comments.objects.all()
    samples = Comments.objects.filter(is_sys=0)
    samples1 = News.objects.filter()
    for i in samples:
        s = SnowNLP(str(i.comment_content))
        i.sys_score = s.sentiments
        i.is_sys = 1
        i.save()
    for j in samples1:

        s = SnowNLP(str(j.comment_content))
        j.sys_score = s.sentiments
        j.save()

    #正确率
    sample = 0
    right = 0
    wrong = 0
    is_scoreds = Comments.objects.filter(is_scored=1)
    for i in is_scoreds:
        sample = sample + 1
        if (i.arti_score <= 0.5 and i.sys_score <= 0.5) or (i.arti_score>0.5 and i.sys_score>0.5):
            right = right + 1
        else:
            wrong = wrong + 1

    sys_id=SysScore.objects.filter().order_by("-id")[:1]
    if not sys_id:
        last_rate = "0%"
        last_sum = 0
        last_correct = 0
        last_wrong = 0
        last_sys_time = ""
        last_time = ""
    else:
        sys_score = SysScore.objects.get(id=sys_id)
        last_rate = sys_score.precision_rate
        last_sum = sys_score.sum
        last_correct = sys_score.correct
        last_wrong = sys_score.wrong
        last_sys_time = sys_score.sys_score_time
        last_time = str(last_sys_time)
        last_time = last_time.split(" ")[0]+"\n"+last_time.split(" ")[1]
    pre_rate = str(100*(round(right / sample, 2)))+"%"
    pre_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pre_sum = sample
    pre_correct = right
    pre_wrong = wrong

    SysScore.objects.create(precision_rate = pre_rate, sum = pre_sum, sys_score_time = pre_time,
                            correct = pre_correct, wrong = pre_wrong)
    # j = json.dumps(str(str(precision_rate*100) + "%" + "，    总数：" + str(sample) + "，   正确数：" + str(right)
    #                    + "，   错误数：" + str(wrong)),ensure_ascii=False)
    pre_time = str(pre_time)
    pre_time = pre_time.split(" ")[0]+"\n"+pre_time.split(" ")[1]
    return JsonResponse({"msg" : "success", "last_rate" : last_rate, "last_sum" : last_sum,
                         "last_correct" : last_correct, "last_wrong" : last_wrong, "last_sys_time" : last_time,
                         "pre_rate" : pre_rate, "pre_time" : pre_time, "pre_sum" : pre_sum,
                         "pre_correct" : pre_correct, "pre_wrong" : pre_wrong})


# @csrf_exempt
# def sys_all(request):
#     #validate(request)
#     # samples = Comments.objects.all()
#     # for i in samples:
#     #      s = SnowNLP(str(i.comment_content))
#     #      i.sys_score = s.sentiments
#     #      i.save()
#     samples = Comments.objects.filter(is_sys=0)
#     for i in samples:
#         s = SnowNLP(str(i.comment_content))
#         i.sys_score = s.sentiments
#         i.is_sys = 1
#         i.save()
#     return JsonResponse({"msg": "success"})


#保存并训练
@csrf_exempt
def save_train(request):
    #validate(request)
    # f = open('C:/Program Files (x86)/Python36-32/Lib/site-packages/snownlp/sentiment/pos.txt',
    #          'a+', encoding='utf-8')
    #
    # high_processeds = Comments.objects.filter(arti_score__gt=0.5, is_scored=1, is_saved=0)
    # for i in high_processeds:
    #     high_list = i.comment_content
    #     f.write('\n')
    #     f.write(high_list)
    #     i.is_saved = 1
    #     i.save()
    # f.close()
    #
    # f = open('C:/Program Files (x86)/Python36-32/Lib/site-packages/snownlp/sentiment/neg.txt',
    #          'a+', encoding='utf-8')
    #
    # low_processeds = Comments.objects.filter(arti_score__lte=0.5, is_scored=1, is_saved=0)
    # for i in low_processeds:
    #     low_list = i.comment_content
    #     f.write('\n')
    #     f.write(low_list)
    #     i.is_saved = 1
    #     i.save()
    # f.close()
    #
    # sentiment.train('C:/Program Files (x86)/Python36-32/Lib/site-packages/snownlp/sentiment/neg.txt',
    #                 'C:/Program Files (x86)/Python36-32/Lib/site-packages/snownlp/sentiment/pos.txt')
    # sentiment.save('C:/Program Files (x86)/Python36-32/Lib/site-packages/snownlp/sentiment//sentiment.marshal')
    #
    # return JsonResponse({"msg": "success"})
    f = open(
        '/usr/local/lib/python3.5/site-packages/snownlp/sentiment/SGMW_pos.txt',
        'a+', encoding='utf-8')
    high_processeds = Comments.objects.filter(arti_score__gt=0.5, is_scored=1, is_saved=0)
    for i in high_processeds:
        high_list = i.comment_content
        f.write('\n')
        f.write(high_list)
        i.is_saved=1
        i.save()
    f.close()

    f = open(
        '/usr/local/lib/python3.5/site-packages/snownlp/sentiment/SGMW_neg.txt',
        'a+', encoding='utf-8')
    low_processeds = Comments.objects.filter(arti_score__lte=0.5, is_scored=1, is_saved=0)
    for i in low_processeds:
        low_list = i.comment_content
        f.write('\n')
        f.write(low_list)
        i.is_saved=1
        i.save()
    f.close()

    sentiment.train(
        '/usr/local/lib/python3.5/site-packages/snownlp/sentiment/SGMW_neg.txt',
        '/usr/local/lib/python3.5/site-packages/snownlp/sentiment/SGMW_pos.txt')
    sentiment.save(
        '/usr/local/lib/python3.5/site-packages/snownlp/sentiment/SGMW_sentiment.marshal')

    return JsonResponse({"msg": "success"})


@csrf_exempt
def show_reply(request):
    #validate(request)
    comment_Id = request.POST.get("No")
    # print('cccccccccccccccccc',comment_Id)
    reply = Reply.objects.filter(comment_id = comment_Id)
    # print(reply,'rrrrrrrrrrrrrrrrrr','comment_Id',comment_Id)
    if reply:
        # print('11111111111111111111111111111')
        rep =[]
        repl = ""
        for i in reply:
            times=i.reply_time
            repl += datetime.datetime.strftime(times,"%Y%m%d %H:%M:%S") + "   "+ i.reply_content+"\n"
        rep.append({"history":repl})
        # print('rep',rep)
        author_realname=""
        author_tel=""
        reply1 = Reply.objects.filter(comment_id = comment_Id)
        # print('reply1',reply1)
        for i in reply1:
            # print('44444444444444444')
            author_realname = i.author_realname
            author_tel = i.author_tel
            # print('555555555555555')
        # print('222222222',author_realname,'33333333333',author_tel)
        if not author_realname:
            author_realname="未知"
        if not author_tel:
            author_tel="未知"
        return JsonResponse({"msg": "success","rep":rep,"author_realname":author_realname,"author_tel":author_tel,
                             "comment_id":comment_Id})
    else:
        # print('rrrrrrrrrrrrrrrrrrr',11111)
        comm=Comments.objects.get(comment_id = comment_Id)
        author_realname = comm.author_realname
        author_tel = comm.author_tel
        if not author_realname:
            author_realname="未知"
        if not author_tel:
            author_tel="未知"
        return JsonResponse({"msg":"success","author_realname":author_realname,"author_tel":author_tel,
                             "comment_id":comment_Id})

#回访
@csrf_exempt
def reply(request):
    #validate(request)
    reply_content = request.POST.get('replyContent')
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_Id = request.POST.get("No")
    admin_name = request.POST.get('admin_name')
    user_name = request.POST.get('user_name')
    tel = request.POST.get('tel')
    reply = Reply.objects.filter(comment_id=comment_Id)
    comms=Comments.objects.get(comment_id=comment_Id)
    comm_count=comms.replys_count
    reply_counts = comm_count
    Reply.objects.create(reply_content=reply_content, reply_time=date_time, reply_user=admin_name,
                         reply_count =reply_counts+1,comment_id=comment_Id,author_realname=comms.author_realname,
                         author_tel=comms.author_tel)
    Comments.objects.filter(comment_id=comment_Id).update(replys_count=comm_count+1)
    return JsonResponse({'msg':'success'})
