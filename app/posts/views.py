import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Post, Comment, HashTag
from .forms import CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')

    else:
        form = PostForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 POST에 댓글을 생성하는 view
    'POST'메서드 요청만 처리

    'content'키로 돌아온 값을 사용해 댓글 생성. 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create/

    :param request:
    :param post_pk:
    :return:
    """

    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            p = re.compile(r'#(?P<tag>\w+)')
            tags = [HashTag.objects.get_or_create(name=name)[0]
                    for name in re.findall(p, comment.content)]
            comment.tags.set(tags)
            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    # Post중, 자신에게 속한 Comment가 가진 HashTag목록 중 tag_name이 HashTag가 포함된
    # Post목록을 posts변수에 할당
    # context에 담아서 리턴 return
    # HTML: /posts/tag_post_list.html
    posts = Post.objects.filter(comments__tags__name=tag_name)
    context = {
        'posts': posts,
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)


def post_like_toggle(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.like_toggle(request.user)
        url = reverse('posts:post-list')
        return redirect(url + f'#post-{post_pk}')

