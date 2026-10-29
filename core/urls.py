from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Übungsseite: Aufgaben holen und Antworten prüfen
    path('api/missions/', views.missions_api, name='missions-api'),
    path('api/check/', views.check_api, name='check-api'),

    # Demo-Endpunkte für die Live-Übungen
    path('demo/posts/', views.PostsListView.as_view(), name='posts'),
    path('demo/posts/strict/', views.strict_post, name='posts-strict'),
    path('demo/posts/latest/', views.latest_post, name='latest-post'),
    path('demo/posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('demo/posts/<slug:post_slug>/', views.post_by_slug, name='post-by-slug'),
    path('demo/alt/', views.old_latest, name='old-latest'),
    path('demo/404/', views.http404_demo, name='http404-demo'),
    path('demo/404-response/', views.not_found_response, name='not-found-response'),
]