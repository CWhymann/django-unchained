from django.db import models

class Mission(models.Model):
    """Represents a mission containing multiple exercises."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    section = models.CharField(max_length=200)
    intro = models.TextField()
    outro = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.code} - {self.title}"

class Exercise(models.Model):
    """Represents an exercise within a mission."""
    TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('fill', 'Fill in the blanks'),
        ('bug', 'Find the bug'),
        ('order', 'Order the lines'),
        ('live', 'Live request'),
    ]
    
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='exercises')
    code = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    question = models.TextField()
    solution = models.JSONField()
    explain = models.TextField()
    hint = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    
    data = models.JSONField(default=dict, blank=True, help_text="Type-specific data like options, lines, etc.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.code} - {self.title}"