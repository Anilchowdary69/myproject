import datetime
from django.test import TestCase

from django.utils import timezone
from django.urls import reverse
from .models import Question

def create_question(question_text,days):
    time=timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewtests(TestCase):
    def test_no_questions(self):
        response=self.client.get(reverse('polls:home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are avaliable")
        self.assertQuerysetEqual(response.context['asked_questions'],[])

    def test_past_questions(self):
        question=create_question(question_text="hii anil",days=-30)
        response=self.client.get(reverse('polls:home'))
        self.assertQuerysetEqual(response.context['asked_questions'],[question])

    def test_future_questions(self):
        question=create_question(question_text="hii venkat",days=30)
        response=self.client.get(reverse('polls:home'))
        self.assertContains(response,"No polls are avaliable")
        self.assertQuerysetEqual(response.context['asked_questions'],[])

    def test_future_question_and_past_question(self):
        question1=create_question(question_text="hey",days=-3)
        question2=create_question(question_text="hii",days=3)
        response=self.client.get(reverse('polls:home'))
        self.assertQuerysetEqual(response.context['asked_questions'],[question1])

    def test_two_past_questions(self):
        question1 = create_question(question_text="he", days=-30)
        question2 = create_question(question_text="she", days=-5)
        response = self.client.get(reverse('polls:home'))
        self.assertQuerysetEqual(response.context['asked_questions'],[question1, question2],)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time=timezone.now() + datetime.timedelta(days=30)
        future_question=Question(pub_date =time)
        self.assertIs(future_question.was_published_recently(),False)
    def test_was_published_recently_with_old_question(self):
        time=timezone.now()  - datetime.timedelta(days=30)
        old_question=Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        time=timezone.now() - datetime.timedelta(hours=23)
        recent_question=Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)






