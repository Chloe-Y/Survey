from django.contrib import admin

# Register your models here.
from .models import Category, Survey, Question, User, Answer

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1
	fieldsets = [(None, {'fields': ['order', 'text', 'types', 'choices']}),]

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'category')
	list_filter = ['name', 'category']
	fieldsets = [
	(None, {'fields': ['name', 'description', 'slug', 'category']}),
	]
	inlines = [QuestionInline]

class AnswerInline(admin.StackedInline):
	model = Answer
	fieldsets = [(None, {'fields': []}),]
	extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('name', 'message', 'pk', 'survey', 'date')
	list_filter = ['name', 'date']
	fieldsets = [
	(None, {'fields': ['name', 'message', 'survey']}),
	]
	inlines = [AnswerInline]


class SurveyInline(admin.TabularInline):
	model = Survey
	fieldsets = [
	(None, {'fields': ['name']}),
	]
	extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	inlines = [SurveyInline]