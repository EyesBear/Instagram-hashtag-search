from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect
from instagram_app.models import *
from django.template import *
from dateutil.parser import parse
from el_pagination.decorators import page_template
from dateutil import tz

import json, urllib2, datetime

API_PREFIX = 'https://api.instagram.com/v1'
CLIENT_ID = "8fd639afdd084574a427ac3a2bf75e58"
ACCESS_TOKEN = '272855367.b6f7db4.27aee70b486a4fd7b1b5546c1da0453d'

    
@csrf_exempt
@page_template('index.html') 
def index(request, extra_context=None):
	context = {
        'images':  ''
    }

	if request.method == "POST":
		context['images'] = Image.objects.all()
		formData = request.POST.dict()
		store_data(formData['tagName'], formData['startDate'], formData['endDate'])
	elif 'page' in request.GET.dict():
		#accessing different pages
		context['images'] = Image.objects.all()

	if extra_context is not None:
			context.update(extra_context)
	return render( request,'index.html', context)

def make_api_request(url=None):
		request = urllib2.Request(url)
		f = urllib2.urlopen(request)
		response = f.read()
		f.close()
		api_dict = json.loads(response)
		return api_dict

def convert_timezone(time):
	#convert time to Eastern time
	utc_zone = tz.gettz('UTC')
	east_zone = tz.gettz('America/New_York')
	time = time.replace(tzinfo=utc_zone)
	time = time.astimezone(east_zone)
	print time
	return time

def store_data(TAG, START, END):
	Image.objects.all().delete()
	img_counter = 1
	next_url = '%s/tags/%s/media/recent?access_token=%s&count=50' % (API_PREFIX, TAG, ACCESS_TOKEN)

	START = parse(START).date()
	END = parse(END).date()

	while True:
		outdated = False 
		instagram_dict = make_api_request(next_url)
		try:
			instagram_data = instagram_dict['data']
			# for every picture tagged 
			for pic_dict in instagram_data:
				img_link = pic_dict['link']
				try:
					if pic_dict['caption'] != None and TAG in pic_dict['caption']['text']:
						# get picture upload time and converts into Toronto timezone
						utc_time = int(pic_dict['caption']['created_time'])
						pic_time = datetime.datetime.utcfromtimestamp(utc_time)
						pic_time = convert_timezone(pic_time)

					#check comments
					elif TAG in pic_dict['tags']:
						media_id = pic_dict['id']
						
						comments_url = '%s/media/%s/comments?access_token=%s' % (API_PREFIX, media_id, ACCESS_TOKEN)
						comments_dict = make_api_request(comments_url)
						
						for comment in comments_dict['data']:
							if TAG in comment['text']:
								utc_time = int(comment['created_time'])
								pic_time = datetime.datetime.utcfromtimestamp(utc_time)
								pic_time = convert_timezone(pic_time)
								break

				except Exception as e:
					print e

				if (pic_time.date() >= START) & (pic_time.date() <= END):
					if pic_dict['type'] == 'image':
						image = pic_dict['images']['low_resolution']
						img_url = image['url']
						img_tag = TAG
						img_datatype = 'image'
					else:
						image = pic_dict['videos']['low_resolution']
						img_url = image['url']
						img_tag = TAG
						img_datatype = 'video'

					username = pic_dict['user']['username']
					# putting into image database
					Image.objects.create(id=img_counter, User=username,
						image_url=img_url, image_link = img_link, image_datatype = img_datatype, 
						post_date = pic_time)

					print 'Successfully created image!'
					img_counter += 1
				elif pic_time.date() < START:
					outdated = True
					print img_link
					break
					
			if outdated:
				break

			# keep fetching more images
			next_url = instagram_dict['pagination']['next_url']

		except Exception as e:
			#no images found
			print e
			break




