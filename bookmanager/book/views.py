from django.http import HttpResponse
from django.core import serializers
import book.models as models
import json

b = models.Book.objects


def books(request):
    params = request.GET
    print(params)
    return HttpResponse(serializers.serialize('json', b.all()))


def save(request):
    # 获取表单参数
    # params = request.POST
    # print(params)
    # 获取body参数
    body = request.body
    params = json.loads(body.decode())
    print(params)
    b.create(
        url=params['url'],
        remark=params['remark'],
        type=params['type']
    )
    return HttpResponse('ok')


def update(request, book_id):
    body = request.body
    params = json.loads(body.decode())
    print(params)
    b.filter(id=book_id).update(remark=params['remark'])
    return HttpResponse('ok')


def delete(request, book_id):
    b.filter(id=book_id).delete()
    return HttpResponse('ok')
