import datetime
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from crawler import settings
import pymysql
from function.views import Comments, News, OthersideModule, OthersideInfo

@csrf_exempt
def receive_content(request):
    data = json.loads(request.body.decode("utf-8"))
    comment_content = data["comment_content"]
    otherside_address = data["otherside_address"]
    catch_time = data["catch_time"]
    author_id = data["author_id"]
    author_nickname = data["author_nickname"]
    author_realname = data["author_realname"]
    author_tel = data["author_tel"]
    comment_time = data["comment_time"]
    order_id = data["order_id"]
    order_number = data["order_number"]
    otherside_comment_id = data["otherside_comment_id"]
    comment_score = data["comment_score"]
    comment_images = data["comment_images"]
    if order_number or order_id:
        type = 1
    else:
        type = 2
    comment1 = data["comment"]
    i = 0
    while i < len(comment1):
        comment_stars = comment1[i]["comment_stars"]
        add_comments = comment1[i]["add_comments"]
        code_name = comment1[i]["code_name"]
        label_id = comment1[i]["label_id"]
        label_name = comment1[i]["label_name"]
        code = OthersideModule.objects.get(code_name=code_name).info_id
        mol = OthersideModule.objects.get(code_name=code_name).parent_id
        module = OthersideModule.objects.get(otherside_module_id=mol).module
        plat = OthersideInfo.objects.get(otherside_info_id=code).platform
        Comments.objects.create(author_realname=author_realname, author_nickname=author_nickname,
                                comment_content=comment_content, order_number=order_number,
                                order_id=order_id, otherside_address=otherside_address, catch_time=catch_time,
                                author_id=author_id, author_tel=author_tel, label_name=label_name,
                                comment_time=comment_time, comment_score=comment_score, comment_stars=comment_stars,
                                comment_images=comment_images, label_id=label_id,
                                add_comments=add_comments, otherside_comment_id=otherside_comment_id,
                                code_name=code_name, is_scored=0, is_saved=0,
                                platform=plat, module=module, is_sys=0, type=type, replys_count=0)
        if int(comment_stars) <= 1:
            comment_id = Comments.objects.last().comment_id
            print(comment_id)
            alert_time = datetime.datetime.now()
            News.objects.create(comment_id=comment_id, author_realname=author_realname, author_nickname=author_nickname,
                                comment_content=comment_content, order_number=order_number,
                                order_id=order_id, otherside_address=otherside_address, catch_time=catch_time,
                                author_id=author_id, author_tel=author_tel, module=module, label_id=label_id,
                                comment_time=comment_time, comment_score=comment_score, comment_star=comment_stars,
                                comment_images=comment_images, add_comments=add_comments, label_name=label_name,
                                otherside_comment_id=otherside_comment_id, alert_time=alert_time, code_name=code_name,
                                is_read=0, is_ignored=0, type=type, platform=plat)
        i += 1
    return JsonResponse({'msg': 'success'})
















