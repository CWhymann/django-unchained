import json

from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from . import content

POSTS = [
    {
        'id': 1,
        'title': 'Showdown bei Sonnenuntergang',
        'content': 'Der Cowboy zieht schneller als sein Schatten.',
        'slug': slugify('Showdown bei Sonnenuntergang'),
    },
    {
        'id': 2,
        'title': 'Der Kopfgeldjäger von Mars Ridge',
        'content': 'Ein Fremder, ein Raumschiff, ein offener Haftbefehl.',
        'slug': slugify('Der Kopfgeldjäger von Mars Ridge'),
    },
]


# ---------- Übungsseite ----------

def index(request):
    return render(request, 'core/index.html')


@require_GET
def missions_api(request):
    return JsonResponse({'missions': content.public_missions()})


@require_POST
def check_api(request):
    try:
        data = json.loads(request.body)
        exercise = content.EXERCISES[data['id']]
        answer = data['answer']
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'error': 'Ungültige Anfrage'}, status=400)
    correct, details = content.check(exercise, answer)
    return JsonResponse({
        'correct': correct,
        'details': details,
        'explain': exercise['explain'],
    })


# ---------- Demo-Endpunkte für die Live-Übungen ----------

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


@require_POST
def strict_post(request):
    # Bewusst OHNE csrf_exempt: Ein POST ohne CSRF-Token wird mit 403 abgewiesen.
    return JsonResponse({'ok': True}, status=201)


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
    return redirect(reverse('latest-post'))


def http404_demo(request):
    raise Http404('Diese Seite gibt es nicht (Http404)')


def not_found_response(request):
    return HttpResponseNotFound('Nicht gefunden (HttpResponseNotFound)')