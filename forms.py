from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Survey, User, Question, Answer

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['name', 'message']

	name = forms.CharField(max_length = 30, label = 'User Name', help_text = 'input a user name')
	message = forms.CharField(max_length = 100, label = 'Leave A Message', help_text = 'say something?')


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['order', 'text', 'survey', 'types', 'choices']

		order = forms.IntegerField()
		text = forms.CharField()

class CreateSurveyForm(forms.Form):
	SurveyFormSet = inlineformset_factory(Survey, Question, fields = ('order', 'text', 'types', 'choices'))
	
	name = forms.CharField(label = 'Survey Name')
	description = forms.CharField(label = 'Survey Description', help_text = 'what is this survey for?', widget = forms.Textarea)

	question_order = forms.IntegerField()
	question_type = forms.CharField(max_length = 1, help_text = 'choose question type\nR for radio, S for select, M for checkbox\nC for text, T for textarea, N for number')
	# question_text
	# maybe make it in admin

class SurveyForm(ModelForm):
	class Meta:
		model = Survey

	def __init__(self, *args, **kwargs):
		self.name = 
		self.questions = Survey.question_set.all()


	name = forms.CharField(label = Survey)




