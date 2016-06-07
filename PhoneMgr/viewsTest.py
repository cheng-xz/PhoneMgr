from django.http import HttpResponse
import time,traceback

def int_process(request,offset):
    try:
        i = int(offset)
    except ValueError:
        raise Http404()
    if request.method == 'POST':
        print request.POST
    s = 'offset is : %d,method is: %s' % (i,request.method)

    return HttpResponse(s)

def hello(reuqest):

    return HttpResponse('hello world')

def TimeNow():
    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
