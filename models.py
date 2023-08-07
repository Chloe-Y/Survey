from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length = 50)

	def __str__(self):
		return self.name

class Survey(models.Model):
	name = models.CharField(max_length = 50)
	slug = models.SlugField()
	description = models.TextField()

	category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True)
	#maybe template for every different Survey

	analysis = models.TextField(null = True, blank = True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('survey:survey', args = (self.slug,))

class User(models.Model):
	name = models.CharField(max_length = 30, blank = True, null = True)
	message = models.CharField(max_length = 100, blank = True, null = True)
	date = models.DateTimeField(auto_now_add = True)
	survey = models.ForeignKey(Survey, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Question(models.Model):
	order = models.PositiveSmallIntegerField()
	text = models.CharField(max_length = 100)
	survey = models.ForeignKey(Survey, on_delete = models.CASCADE, null = True, blank = True)
	questionTypes = [
		('C', 'text'),
		('T', 'textarea'),
		('R', 'radio'),
		('N', 'number'),
		('S', 'select'),
		('M', 'checkbox')
	]
	types = models.CharField(max_length = 1, choices = questionTypes, default = 'C') # i can't use just type
	choices = models.TextField(blank = True, null = True, help_text = 'if the question type is raido, select or checkbox, provide a line-separated("\\n separated") list of options for this question.')

	def get_choices(self):
		'return radio/select/checkbox type questions\'s choices as a list'
		choices = self.choices.split('\n')
		choicesList = []
		for c in choices:
			c = c.strip()
			if c:
				choicesList.append(c.strip())
		return choicesList

	def validity(self):
		'if question type is R/S/M, then there should be at least 2 choices'
		if self.types in ['R', 'S', 'M'] and len(self.get_choices()) < 2:
			raise ValueError('Radio, Select and Checkbox type must contain more than one choice')

	def save(self, *args, **kwargs):
		self.validity()
		super().save(*args, **kwargs)


	def __str__(self):
		return self.text


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	text = models.TextField(blank = True, null = True)

	def __str__(self):
		return self.question.text+'\n'+self.text