from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Survey, Question, User, Answer
import random


# Create your views here.
def index(request):
	allCategories = Category.objects.all()
	return render(request, 'index.html', {'categories': allCategories})
	# not sure how to show all categories with their inner survey, try get all surveys first

def survey(request, slug):
	s = get_object_or_404(Survey, slug = slug)
	questions = Question.objects.filter(survey = s)
	if not questions:
		questions = []

	if request.method == 'POST':
		u = User(name = 'test', survey = s)
		u.save()
		try:
			for i, q in enumerate(questions):
				if q.types == 'M':
					value = request.POST.getlist('answer-'+str(i+1))
					a = Answer(user = u, question = q, text = '\n'.join(value))
					a.save()
				else:
					value = request.POST['answer-'+str(i+1)]
					a = Answer(user = u, question = q, text = value)
					a.save()
		except Exception as e:
			# raise e
			return render(request, 'index.html', {'survey': s, 'questions': questions, 'errorMsg': '(*꒦ິㅿ꒦ີ) 出错了： '+ e})
		else:
			return redirect('survey:addUser', pk = u.pk)
	return render(request, 'index.html', {'survey': s, 'questions': questions})

def addUser(request, pk=1):
	u = get_object_or_404(User, pk = pk)
	if request.method == 'POST':
		try:
			u.name = request.POST['name']
			u.message = request.POST.get('message', '')
		except Exception as e:
			return render(request, 'user.html', {'user': u, 'errorMsg': '(๑•́₋•̩̥̀๑) 出错了：'+ e})
		else:
			u.save()
			return redirect('survey:user', pk = u.pk)
	return render(request, 'user.html', {'user': u})
		

def user(request, pk):
	u = get_object_or_404(User, pk = pk)
	answers = u.answer_set.all()
	return render(request, 'user.html', {'user': u,'answers': answers, 'getRandomUser': True})
	#save to pdf, txt, png in user html

def randUser(request, pk):
	u = get_object_or_404(User, pk = pk)
	us = User.objects.filter(survey = u.survey).exclude(pk = u.pk)
	randu = random.choice(us)
	answers = randu.answer_set.all()
	return render(request, 'user.html', {'user':randu, 'answers': answers})



def analysis(request):
	pass

def addSurvey(request):
	pass