import xlwt
from django.shortcuts import render, redirect
import string
import datetime
from django.views.decorators.csrf import csrf_exempt
from function.models import OthersideModule,Comments
from django.http import JsonResponse, HttpResponse
import json
import base64
import datetime
from io import BytesIO

# Create your views here.
@csrf_exempt
def export_content(request):
    order_number = request.POST.get('orderNo', None)
    author_realname = request.POST.get('name', None)
    platform = request.POST.get('platform', None)
    author_tel = request.POST.get('tel', None)
    start_comment_time = request.POST.get('startTime')
    end_time = request.POST.get('endTime')
    start_arti_score = request.POST.get('lowScore', None)
    end_arti_score = request.POST.get('highScore', None)
    replys_count = request.POST.get('replyState', None)
    code_name = request.POST.get('code_name', None)
    library = request.POST.get('library', None)

    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet', cell_overwrite_ok=True)

    # 设置文件头的样式
    style_heading = xlwt.easyxf("""
                                   font:
                                       name Arial,
                                       colour_index white,
                                       bold on,
                                       height 0xA0;
                                   align:
                                       wrap off,
                                       vert center,
                                       horiz center;
                                   pattern:
                                       pattern solid,
                                       fore-colour 0x19;
                                   borders:
                                       left THIN,
                                       right THIN,
                                       top THIN,
                                       bottom THIN;
                                   """)

    # 写入文件标题
    sheet.write(0, 0, 'ID', style_heading)
    sheet.write(0, 1, '订单号', style_heading)
    sheet.write(0, 2, '订单ID', style_heading)
    sheet.write(0, 3, '用户真实姓名', style_heading)
    sheet.write(0, 4, '用户电话号码', style_heading)
    sheet.write(0, 5, '平台', style_heading)
    sheet.write(0, 6, '模块', style_heading)
    sheet.write(0, 7, '评论内容', style_heading)
    sheet.write(0, 8, '评论时间', style_heading)
    sheet.write(0, 9, '还车服务评价', style_heading)
    sheet.write(0, 10, '用车过程评价', style_heading)
    sheet.write(0, 11, '体验全过程评分', style_heading)
    sheet.write(0, 12, '提车服务评分', style_heading)
    sheet.write(0, 13, '用户评价', style_heading)
    sheet.write(0, 14, '维修速度评价', style_heading)
    sheet.write(0, 15, '维修效果评价', style_heading)
    sheet.write(0, 16, '服务态度评价', style_heading)
    sheet.write(0, 17, '总体评价', style_heading)
    sheet.write(0, 18, '回复状态', style_heading)
    sheet.write(0, 19, '系统评分', style_heading)
    sheet.write(0, 20, '人工评分', style_heading)
    # modules = OthersideModule.objects.filter(code_name__isnull=False)
    # for mo in modules:
    #     print(mo.code_name, '000')
    #     names = OthersideModule.objects.filter(code_name=mo.code_name)
    #     for na in names:
    #         print(na.module, '111')
    #         sheet.write(0, 12, mo.code_name, style_heading)

    if library == "high":
        comment = Comments.objects.filter(arti_score__gt=0.5, is_scored=1)
    if library == "low":
        comment = Comments.objects.filter(arti_score__lte=0.5, is_scored=1)
    # 评论未处理
    if library == "comment":
        comment = Comments.objects.filter(is_scored=0, type=2)
    # 评价未处理
    if library == "judgement":
        comment = Comments.objects.filter(is_scored=0, type=1)

    #全都为空
    if not order_number and not author_realname and not platform and not author_tel and not start_comment_time and \
            not end_time and not start_arti_score and not end_arti_score and not replys_count:
        # 写入数据
        data_row = 1
        print(comment, '===')
        for i in comment:
            sheet.write(data_row, 0, i.comment_id)
            sheet.write(data_row, 1, i.order_number)
            sheet.write(data_row, 2, i.order_id)
            sheet.write(data_row, 3, i.author_realname)
            sheet.write(data_row, 4, i.author_tel)
            sheet.write(data_row, 5, i.platform)
            sheet.write(data_row, 6, i.module)
            sheet.write(data_row, 7, i.comment_content)
            if i.comment_time == ' ' or not i.comment_time:
                i.comment_time = ' '
                sheet.write(data_row, 8, i.comment_time)
            else:
                comment_time = i.comment_time.strftime('%Y-%m-%d')
                sheet.write(data_row, 8, comment_time)
            if i.code_name == '511':
                stars = i.comment_stars
                sheet.write(data_row, 9, stars)   #还车服务评分
            else:
                stars = ' '
                sheet.write(data_row, 9, stars)  # 还车服务评分
            if i.code_name == '521':
                stars = i.comment_stars
                sheet.write(data_row, 10, stars)   #用车体验评分
            else:
                stars = ' '
                sheet.write(data_row, 10, stars)  # 用车体验评分
            if i.code_name == '522':
                stars = i.comment_stars
                sheet.write(data_row, 11, stars)  # 体验全过程评分
            else:
                stars = ' '
                sheet.write(data_row, 11, stars)  # 体验全过程评分
            if i.code_name == '523':
                stars = i.comment_stars
                sheet.write(data_row, 12, stars)  # 提车服务评分
            else:
                stars = ' '
                sheet.write(data_row, 12, stars)  # 提车服务评分
            if i.code_name == '671':
                stars = i.comment_stars
                sheet.write(data_row, 13, stars)  # 用户评分
            else:
                stars = ' '
                sheet.write(data_row, 13, stars)  # 用户评分
            if i.code_name == '791':
                stars = i.comment_stars
                sheet.write(data_row, 14, stars)  # 维修速度
            else:
                stars = ' '
                sheet.write(data_row, 14, stars)  # 维修速度
            if i.code_name == '792':
                stars = i.comment_stars
                sheet.write(data_row, 15, stars)  # 维修效果
            else:
                stars = ' '
                sheet.write(data_row, 15, stars)  # 维修效果
            if i.code_name == '793':
                stars = i.comment_stars
                sheet.write(data_row, 16, stars)  # 服务态度
            else:
                stars = ' '
                sheet.write(data_row, 16, stars)  # 服务态度
            if i.code_name == '794':
                stars = i.comment_stars
                sheet.write(data_row, 17, stars)  # 总体评价
            else:
                stars = ' '
                sheet.write(data_row, 17, stars)  # 总体评价
            if i.replys_count == 0:
                sheet.write(data_row, 18, '未回访')
            else:
                sheet.write(data_row, 18, '已回访')
            sheet.write(data_row, 19, i.sys_score)
            sheet.write(data_row, 20, i.arti_score)
            # if i.code_name == mo.code_name:
            #     print(i.comment_stars, '333')
                # sheet.write(data_row, 12, )
            data_row = data_row + 1
        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=export%s.xls' % nowtime
        response.write(output.getvalue())
        return response
    # 订单号不为空
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

    # 写入数据
    data_row = 1
    for i in data:
        sheet.write(data_row, 0, i.comment_id)
        sheet.write(data_row, 1, i.order_number)
        sheet.write(data_row, 2, i.order_id)
        sheet.write(data_row, 3, i.author_realname)
        sheet.write(data_row, 4, i.author_tel)
        sheet.write(data_row, 5, i.platform)
        sheet.write(data_row, 6, i.module)
        sheet.write(data_row, 7, i.comment_content)
        if i.comment_time == ' ' or not i.comment_time:
            i.comment_time = ' '
            sheet.write(data_row, 8, i.comment_time)
        else:
            comment_time = i.comment_time.strftime('%Y-%m-%d')
            sheet.write(data_row, 8, comment_time)
        if i.code_name == '511':
            stars = i.comment_stars
            sheet.write(data_row, 9, stars)  # 还车服务评分
        else:
            stars = ' '
            sheet.write(data_row, 9, stars)  # 还车服务评分
        if i.code_name == '521':
            stars = i.comment_stars
            sheet.write(data_row, 10, stars)  # 用车体验评分
        else:
            stars = ' '
            sheet.write(data_row, 10, stars)  # 用车体验评分
        if i.code_name == '522':
            stars = i.comment_stars
            sheet.write(data_row, 11, stars)  # 体验全过程评分
        else:
            stars = ' '
            sheet.write(data_row, 11, stars)  # 体验全过程评分
        if i.code_name == '523':
            stars = i.comment_stars
            sheet.write(data_row, 12, stars)  # 提车服务评分
        else:
            stars = ' '
            sheet.write(data_row, 12, stars)  # 提车服务评分
        if i.code_name == '671':
            stars = i.comment_stars
            sheet.write(data_row, 13, stars)  # 用户评分
        else:
            stars = ' '
            sheet.write(data_row, 13, stars)  # 用户评分
        if i.code_name == '791':
            stars = i.comment_stars
            sheet.write(data_row, 14, stars)  # 维修速度
        else:
            stars = ' '
            sheet.write(data_row, 14, stars)  # 维修速度
        if i.code_name == '792':
            stars = i.comment_stars
            sheet.write(data_row, 15, stars)  # 维修效果
        else:
            stars = ' '
            sheet.write(data_row, 15, stars)  # 维修效果
        if i.code_name == '793':
            stars = i.comment_stars
            sheet.write(data_row, 16, stars)  # 服务态度
        else:
            stars = ' '
            sheet.write(data_row, 16, stars)  # 服务态度
        if i.code_name == '794':
            stars = i.comment_stars
            sheet.write(data_row, 17, stars)  # 总体评价
        else:
            stars = ' '
            sheet.write(data_row, 17, stars)  # 总体评价
        if i.replys_count == 0:
            sheet.write(data_row, 18, '未回访')
        else:
            sheet.write(data_row, 18, '已回访')
        sheet.write(data_row, 19, i.sys_score)
        sheet.write(data_row, 20, i.arti_score)
        data_row = data_row + 1
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=export-%s.xls' % nowtime
    response.write(output.getvalue())
    return response

