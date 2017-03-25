from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from mainmodel.models import Company, Freelancer, userlikes, Project
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import pearson_correlation
from scikits.crab.similarities import UserSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender

import random

def home(request):
	return render(request, 'home.html')

def getstarted(request):
	if request.method == "GET":
		return render(request, 'project_idea.html')
	else:
	    name = request.POST.get('q1')
	    email = request.POST.get('q2')
	    requirement = request.POST.get('q3')
	    description = request.POST.get('q4')
	    budget = request.POST.get('q5')
	    try:
	    	project = Project.objects.create(
	    			user_id = request.user,
	    			name = name,
	    			email =email,
	    			proj_type = requirement,
	    			description = description,
	    			budget = budget,
	    		)
	    	project.save()
	    except:
	    	print "error"
	    	return render(request, 'project_idea.html')
	    return render(request, 'project_idea.html')

@csrf_exempt
def register(request):
	print "1"
	if request.method == 'POST':
		email = request.POST.get('email')
		if len(User.objects.filter(email=email)) == 0:
			if email:
				user = User.objects.create_user(email.split('@')[0], email, 'doodleblue')
				like = userlikes.objects.create(user_id=user)
				user.save()
				like.save()
				print 2
				return JsonResponse({"status": True, "message": "200"})
			else:
				# 400 bad request - invalid input
				return JsonResponse({"status": False, "message": "400"})
		else:
			# user already exist
			return JsonResponse({"status": False, "message": "409"})
	else:
		# HTTP Error 405 Method not allowed
		return JsonResponse({"status": False, "message": "405"})

@csrf_exempt
def login_mod(request):
	if request.method == "POST":
		email = request.POST.get('email')
		print email
		if email:
			user = authenticate(username=email.split('@')[0], password='doodleblue')
			print 1
			if user:
				print 2
				login(request, user)
				print "4"
				return JsonResponse({"status": True, "message": "200"})
			else:
				# authentication failed
				return JsonResponse({"status": False, "message": "401"})
		else:
			return JsonResponse({"status": False, "message": "400"})
	else:
		# HTTP Error 405 Method not allowed
		return JsonResponse({"status": False, "message": "405"})

@csrf_exempt
def logout_met(request):
	if request.user.is_authenticated():
		logout(request)
	return redirect('home')

def recommender(request):

	freelancer = {"user_ids":{}, 'data':{}, 'item_ids':{}}
	for user in User.objects.all():
		freelancer['user_ids'][user.id] = user.username

	for user in User.objects.all():
		freelancer['item_ids'][user.id] = user.username

	test_item = {"ios": 1, "ui":2, "android":3, "website":4}

	for user in User.objects.all():
		freelancer['data'][user.id] = {}
		for project in Project.objects.all():
			if project.user_id.username == project.user_id.id:
				freelancer['data'][user.id][test_item[proj_type]] = 4
				break
		for id, item in test_item.items():
			freelancer['data'][user.id][item] = random.randint(1,4)

	print freelancer['data']

	freelancer['data'] = {1: {1: 3.0, 2: 4.0, 3: 3.5, 4: 5.0, 5: 3.0},
    	2: {1: 3.0, 2: 4.0, 3: 2.0, 5: 3.0, 6: 2.0},
     	3: {2: 3.5, 3: 2.5, 4: 4.0, 5: 4.5, 6: 3.0},
     	4: {1: 2.5, 2: 3.5, 3: 2.5, 4: 3.5, 5: 3.0, 6: 3.0},
     	5: {2: 4.5, 3: 1.0, 4: 4.0},
     	6: {1: 3.0, 2: 3.5, 3: 3.5, 4: 5.0, 5: 3.0, 6: 1.5},
     	7: {1: 2.5, 4: 3.5, 5: 4.0}}


	model = MatrixPreferenceDataModel(freelancer['data'])
	similarity = UserSimilarity(model, pearson_correlation)
	recommender = UserBasedRecommender(model, similarity, with_preference=True)
	print freelancer['data']
	print recommender.recommend(request.user.id)
	return JsonResponse({"status": True, "data":recommender.recommend(request.user.id)})