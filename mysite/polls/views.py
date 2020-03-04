from django.shortcuts import render, get_object_or_404
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

"""
def index(request):
	# Returns main page.

	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template("polls/index.html")
	context = {
		"latest_question_list" : latest_question_list 
	}
	
	return HttpResponse(template.render(context, request))
"""
class Index_view(generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_question_list"

	def get_queryset(self):
		return Question.objects.order_by("-pub_date")[:5]

"""
def detail(request, question_id):
	# Returns page of one question and its choices.

	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	
	return render(request, 'polls/detail.html', {'question': question})
"""

class Detail_view(generic.DetailView):
	model = Question
	template_name = "polls/detail.html"

"""
def results(request, question_id):
	# Returns page of result of your voting.

	question = get_object_or_404(Question, pk=question_id)
	
	return render(request, "polls/results.html", context={"question" : question})
"""

class Results_view(generic.DetailView):
	model = Question
	template_name = "polls/results.html"

def vote(request, question_id):
	# Returns redirect to results viev after your voting.
	
	question = get_object_or_404(Question, pk=question_id)

	try:
		selected_choice = question.choice_set.get(pk=request.POST["choice"])
	except (KeyError, Choice.DoesNotExist):
		return render(request, "polls/detail.html", context={"question" : question,
															 "error_message" : "You didn't select a choice"})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		
		return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
