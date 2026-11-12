from django.contrib import admin
from .models import Mission, Exercise

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """Admin configuration for Mission model."""
    list_display = ('code', 'title', 'section', 'order')
    ordering = ('order',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Admin configuration for Exercise model."""
    list_display = ('code', 'title', 'type', 'mission', 'order')
    list_filter = ('type', 'mission')
    ordering = ('mission', 'order')
