from django.db import models

class SpeechRecognition(models.Model):
    original_text = models.TextField()
    language_code = models.CharField(max_length=10)
    recognized_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_text[:50]  # Display the first 50 characters

class Translation(models.Model):
    speech_recognition = models.ForeignKey(SpeechRecognition, on_delete=models.CASCADE)
    translated_text = models.TextField()
    target_language_code = models.CharField(max_length=10)
    translated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.translated_text[:50]  # Display the first 50 characters



# Create your models here.
