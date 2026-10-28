from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from .models import Challenge
from .serializers import ChallengeSerializer

POSTS = [
    {'id': 1, 'title': 'First post', 'content': 'Hallo Welt', 'slug': slugify('First post')},
    {'id': 2, 'title': 'Zweiter Post', 'content': 'Noch ein Text', 'slug': slugify('Zweiter Post')},
]


class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


def index(request):
    return render(request, 'core/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class PostsListView(View):
    def get(self, request):
        return JsonResponse(POSTS, safe=False)

    def post(self, request):
        title = request.POST.get('title', '')
        post = {
            'id': len(POSTS) + 1,
            'title': title,
            'content': request.POST.get('content', ''),
            'slug': slugify(title),
        }
        POSTS.append(post)
        return JsonResponse(post, status=201)


def post_detail(request, post_id):
    for post in POSTS:
        if post['id'] == post_id:
            return JsonResponse(post)
    raise Http404('Post nicht gefunden')


def post_by_slug(request, post_slug):
    for post in POSTS:
        if post['slug'] == post_slug:
            return JsonResponse(post)
    raise Http404('Post nicht gefunden')


def latest_post(request):
    return JsonResponse(POSTS[-1])


def old_latest(request):
    return redirect('latest-post')


def http404_demo(request):
    raise Http404('Diese Seite gibt es nicht (Http404)')


def not_found_response(request):
    return HttpResponseNotFound('Nicht gefunden (HttpResponseNotFound)')