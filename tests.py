from django.test import TestCase, Client
from django.urls import reverse
from .models import Survey, Question
# Create your tests here.

class QuestionTestCase(TestCase):
	def test_radio_with_multi_choices(self):
		'add 3 radio choices with blank, should return them with striped'
		q1 = Question(order = 1, text = 'Radio Question with multi choices test.', types = 'R', choices = "radio 1\nradio 2\n radio 3 \n")
		self.assertEqual(q1.get_choices(), ['radio 1', 'radio 2', 'radio 3'])

	def test_select_with_multi_choices(self):
		'add 3 select choices with blank, should return them with striped'
		q2 = Question(order = 2, text = 'Select Question with multi choices test.', types = "S", choices = "select 1 \n select 2\n select 3")
		self.assertEqual(q2.get_choices(), ['select 1', 'select 2', 'select 3'])

	def test_checkbox_with_multi_choices(self):
		'add 2 checkbox choices with blank, should return them with striped'
		q3 = Question(order = 3, text = 'Checkbox question with multi choices test.', types = "M", choices = "checkbox 1\n checkbox 2\n")
		self.assertEqual(q3.get_choices(), ['checkbox 1', 'checkbox 2'])
		
	def test_radio_with_one_choice(self):
		'add radio question with only 1 choice, should raise ValueError'
		with self.assertRaisesMessage(ValueError, 'Radio, Select and Checkbox type must contain more than one choice'):
			q4 = Question(order = 4, text = 'Radio Question with one line choice', types = "R", choices = "just one line")
			q4.save()

	def test_select_with_one_line_choice(self):
		'add question with invalid choices'
		with self.assertRaisesMessage(ValueError, 'Radio, Select and Checkbox type must contain more than one choice'):
			q5 = Question(order = 5, text = "Select question with one line choice", types = "S", choices = "one line choice \n   \n  \n")
			q5.save()

	def test_checkbox_with_2_line_empty_choices(self):
		'add question with 1 line choice and 1 line empty, should raise error'
		with self.assertRaisesMessage(ValueError, 'Radio, Select and Checkbox type must contain more than one choice'):
			q6 = Question(order = 6, text = "Checkbox Question with 2 line but no words", types = "M", choices = " 测试中文换行 \n      ")
			q6.save()

class SurveyTestCase(TestCase):
	def test_survey_without_question(self):
		'create survey without question'
		s = Survey.objects.create(name = 'Test Survey', slug = 'test-survey', description = 'survey for test')

		response = self.client.get(reverse('survey:survey', args = ('test-survey',)))
		self.assertEqual(response.status_code, 200)

	def test_survey_with_questions(self):
		'create survey and add 6 type questions, then try post data and redirect to add user page'
		s = Survey.objects.create(name = 'Test Survey', slug = 'test-survey', description = 'survey for test')

		s.question_set.create(order =1, text = 'question text', types = 'C')
		s.question_set.create(order = 2, text = 'question textarea', types = 'T')
		s.question_set.create(order = 3, text = 'radio type question', types = 'R', choices = 'radio 1\n radio 2\n  radio 3  ')
		s.question_set.create(order = 4, text = 'checkbox type question', types = 'M', choices = 'checkbox 1\n checkbox 2\n checkbox 3')
		s.question_set.create(order = 5, text = 'select type question', types = 'S', choices = 'select 1\nselect 2\n select 3')
		s.question_set.create(order = 6, text = 'give a rate', types = 'N')

		response = self.client.post(reverse('survey:survey', args = ('test-survey',)), {'answer-1':'answer text', 'answer-2':'answer textarea', 'answer-3': 'radio 3', 'answer-4':('checkbox 1', 'checkbox 2', 'checkbox 3'), 'answer-5': 'select 3', 'answer-6': '10'}, follow = True)

		# print(response.context)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain, [('/survey/add/1', 302)])
