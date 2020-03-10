from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
	def test_is_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		fut_q = Question(pub_date=time)
		self.assertIs(fut_q.is_recently(), False)

	def test_is_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_q = Question(pub_date=time)
		self.assertIs(old_q.is_recently(), False)

	def test_is_recently_with_recent_question(self):
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		rec_q = Question(pub_date=time)
		self.assertIs(rec_q.is_recently(), True)

def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
	def test_no_questions(self):
		response = self.client.get(reverse("polls:index"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context["latest_question_list"], [])

	def test_past_question(self):
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(response.context["latest_question_list"], ["<Question: Past question.>"])
		
	def test_future_question(self):
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context["latest_question_list"], [])

class QuestionDetailVievTests(TestCase):
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