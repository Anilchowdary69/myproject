from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=150)
    pub_date=models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        time=timezone.now()
        return time- datetime.timedelta(days=1) <= self.pub_date <= time
    
class Choice(models.Model):
    question=models.ForeignKey(Question,  on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=150)
    votes=models.IntegerField(default=0)

    def __str__ (self):
        return self.choice_text
    