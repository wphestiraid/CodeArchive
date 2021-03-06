from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from .models import Post
from .forms import PostForm


def post_list(request) :
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

	pagedata = {'posts' : posts}

	return render(request, 'blog/post_list.html', pagedata)

def post_category(request, ct) :
	posts = Post.objects.filter(category = ct).order_by('-published_date')
	posts = posts.filter(published_date__lte=timezone.now())
	pagedata = {'posts' : posts, 'subtitle' : ct + " 글 목록"}

	return render(request, 'blog/post_list.html', pagedata)

def post_detail(request, pk) :
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post' : post})

def month_view(request, year, month) :
	posts = Post.objects.filter(published_date__year=year)
	posts = posts.filter(published_date__lte=timezone.now())
	posts = posts.filter(published_date__month=int(month)).order_by('-published_date')
	pagedata = {'posts':posts, 'subtitle':''}
	pagedata.update({'posts':posts, 'subtitle':"%s년 %s월의 글 목록" % (year, int(month)),})
	return render(request, 'blog/post_list.html', pagedata)

def search_post(request) :
	keyword = request.GET['keyword']
	posts1 = Post.objects.filter(title__contains=keyword).order_by('-published_date')
	posts2 = Post.objects.filter(text__contains=keyword).order_by('-published_date')
	posts = posts1|posts2
	posts = posts.filter(published_date__lte=timezone.now())
	posts = posts.order_by('-published_date')
	pagedata = {'posts':posts, 'subtitle' : '\"' + keyword + '" 검색 결과'}

	return render(request, 'blog/post_list.html', pagedata)


@login_required

def post_new(request) :
	if request.method == "POST" :
		form = PostForm(request.POST)
		if form.is_valid() :
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else :
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form' : form})

def post_edit(request, pk) :
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST" :
		form = PostForm(request.POST, instance=post)
		if form.is_valid() :
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else :
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form' : form})

def post_draft_list(request) :
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts' : posts})

def post_publish(request, pk) :
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

def post_remove(request, pk) :
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')