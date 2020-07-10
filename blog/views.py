from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost
# Create your views here.
def index(request):
    alldata = Blogpost.objects.all()
    print(alldata[0].title)
    return render(request,'blog/index.html',{'alldata':alldata,'range':range(0,len(alldata))})

def blogpost(request,id):
    lent = Blogpost.objects.all()
    post = Blogpost.objects.filter(post_id=id)[0]
    print(post.post_id)
    pre = post.post_id - 1
    nex = post.post_id + 1
    if pre == 0 :
        pre = post.post_id
    if nex > len(lent):
        nex = post.post_id
    print(pre,nex)
    return render(request,'blog/blogpost.html',{'post':post,'pre':pre,'nex':nex})