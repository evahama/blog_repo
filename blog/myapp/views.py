from django.shortcuts import render,get_object_or_404
from .models import Post
from .forms import EmailSendForm
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def post_list_view(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'myapp/post_list.html',{'post_list':post_list})

def post_detail_view(request,year,month,day,pp):
    post_detail = get_object_or_404(Post,slug=pp,
                                    status='published',
                                    publish__year=year,publish__month=month,publish__day=day)
    return render(request,'myapp/post_detail.html',{'post_detail':post_detail})

def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    form = EmailSendForm()
    if request.method == 'POST':
        form =EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject = '{} by {} sent this article "{}" to you'.format(cd['name'],cd['email'],post.title)
            current_post_url = request.build_absolute_uri(post.get_absolute_url())
            ms='Red this post at {}, \n {} sent to you \n {} say: \n {} '.format(current_post_url,cd['name'],cd['name'],cd['comments'])
            send_mail(subject,ms,'sender',[cd['to'],])
            sent = True
    return render(request,'myapp/sharebymail.html',{'form':form,'post':post,'sent':sent})
