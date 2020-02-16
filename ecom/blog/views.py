from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from . models import blogPost


def index(request):
    postID = blogPost.objects.all()
    all_posts = []

    for item in postID:
        all_posts.append(item)

    params = {'all_posts': all_posts}
 
    return render(request, 'blog/index.html', params)


def __str__(self):
    return self.titlle


def blogpost(request,id):
    post = blogPost.objects.filter(post_id=id)[0]
    return render(request, 'blog/blogpost.html',{'post':post})
