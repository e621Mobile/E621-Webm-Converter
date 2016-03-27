from django.db import models
from django.conf import settings
from subprocess import Popen, PIPE
from PIL import Image
import os
import tempfile
import urllib2
import json
import shutil

# Create your models here.
class E621Webm(models.Model):
	IMAGE_SUBPATH = "E621Webm" + os.sep + "image" + os.sep;
	THUMB_SUBPATH = "E621Webm" + os.sep + "thumb" + os.sep;
	VIDEO_SUBPATH = "E621Webm" + os.sep + "video" + os.sep;
	
	post_id = models.IntegerField(primary_key=True)
	
	image = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,IMAGE_SUBPATH), default='', blank=True)
	thumbnail = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT,THUMB_SUBPATH), default='', blank=True)
	video = models.FileField(upload_to=os.path.join(settings.MEDIA_ROOT,VIDEO_SUBPATH), default='', blank=True)
	
	def generate_thumbnail(self, post=None, output=False):
		webm_handle,webm = tempfile.mkstemp(suffix=".webm");
		webm = open(webm,"wb");
		jpg_handle,jpg = tempfile.mkstemp(suffix=".jpg")
		os.close(jpg_handle)
		os.remove(jpg)
		
		if(post == None):
			response = urllib2.urlopen('http://e621.net/post/show.json?id=%d'%(self.post_id,))
			response = response.read()
			
			try:
				post = json.loads(response)
				post = post["file_url"]
			except ValueError:
				return;
		
		response = urllib2.urlopen(post)
		shutil.copyfileobj(response, webm)
		webm.close()
		os.close(webm_handle)

		_PIPE = (None if output else PIPE);
		
		p = Popen([settings.FFMPEG_LOCATION,"-i",webm.name,"-r","1","-t","1","-f","image2",jpg], stdout=_PIPE, stderr=_PIPE);
		p.communicate()
		
		video_path = os.path.join(self.VIDEO_SUBPATH,str(self.post_id)+".mp4");
		p = Popen([settings.FFMPEG_LOCATION,"-i",webm.name,"-vf","scale=trunc(iw/2)*2:trunc(ih/2)*2","-c:v","libx264","-profile:v","baseline","-c:a","aac","-strict","-2","-ar","44100","-ac","2","-b:a","128k","-y",os.path.join(settings.MEDIA_ROOT,video_path)],stdout=_PIPE,stderr=_PIPE);
		p.communicate()
		self.video = video_path

		os.remove(webm.name);
		
		try:
			img = Image.open(jpg).convert("RGB")
		except IOError:
			return False
		
		play_button = Image.open(settings.PLAY_BUTTON_LOCATION);
		
		
		image_path = os.path.join(self.IMAGE_SUBPATH,str(self.post_id)+".jpg");
		img.thumbnail((480,480),Image.ANTIALIAS)
		play_button.thumbnail([i/2.0 for i in img.size],Image.ANTIALIAS);
		img.paste(play_button,tuple([(img.size[i]/2) - (play_button.size[i]/2) for i in xrange(len(img.size))]),play_button)
		img.save(os.path.join(settings.MEDIA_ROOT,image_path), 'JPEG')
		self.image = image_path
		
		thumb_path = os.path.join(self.THUMB_SUBPATH,str(self.post_id)+".jpg");
		img.thumbnail((120,120),Image.ANTIALIAS)
		img.save(os.path.join(settings.MEDIA_ROOT,thumb_path), 'JPEG')
		self.thumbnail = thumb_path
		
		os.remove(jpg);
		
		return;
	
	@staticmethod
	def retrieve_webm(limit=20, output=False):
		tags = "type:webm+order:id"
		
		try:
			tags += "+id:>" + str(E621Webm.objects.latest('post_id').post_id)
		except:
			pass
		
		response = urllib2.urlopen('https://e621.net/post/index.json?tags=%s&limit=%d'%(tags,limit))
		response = response.read()
		
		try:
			post = json.loads(response)
			for p in post:
				e = E621Webm(p['id'])
				e.save()
				e.generate_thumbnail(p['file_url'],output)
				e.save()
		except ValueError:
			return;

	def __unicode__(self):
		return "%d" % self.post_id
