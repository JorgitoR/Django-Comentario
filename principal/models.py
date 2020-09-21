# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.contenttypes.fields import GenericRelation
from comentario.models import Responder
from django.conf import settings

from django.db.models.signals import post_save

from django.db.models.signals import pre_save


from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
	imgperfil = models.ImageField(upload_to='foto_perfil', blank=True, null=True)


class Pregunta(models.Model):

	user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pregunta")
	pregunta = models.TextField(max_length=200, blank=True, null=True)
	slug      = models.SlugField(unique=True, blank=True)
	update    = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.pregunta
	
	def get_absolute_url(self):
		return reverse("view_ipk", kwargs={"pk": self.pk})

	def get_tiempo(self):
		return	self.timestamp.strftime("%b %d %I:%M %p")

	@property
	def comentarios(self):
		instance = self
		qs = Responder.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		content_type = ContentType.objects.get_for_model(Pregunta)
		return content_type


def new_url_ask(instance, nueva_url=None):

	slug = slugify(instance.pregunta)
	
	if nueva_url is not None:
		slug = nueva_url
	qs = Pregunta.objects.filter(slug=slug).order_by("-id")

	if qs.exists():
		nueva_url = "%s-%s"%(slug, qs.first().id)
		return new_url_ask(instance, nueva_url=nueva_url)
	return slug

def url_creada_ask(sender, instance, *args, **kwargs): #creamos nuestro callback 
	if not instance.slug:

		name = "who are you?"
		print("%s %s" % (name, 12))
		instance.slug = new_url_ask(instance)

pre_save.connect(url_creada_ask, sender=Pregunta)
