# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.signals import pre_save


from django.core.urlresolvers import reverse

class ComentariosManager(models.Manager):


	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		qs =super(ComentariosManager, self).filter(content_type= content_type, object_id= obj_id).filter(padre=None)
		return qs


class Responder(models.Model):
	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
	respuesta = models.TextField(verbose_name="Respuesta", default="Hi")
	tiempo = models.DateTimeField(auto_now_add=True)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	padre = models.ForeignKey("self", null=True, blank=True)

	objects = ComentariosManager()

 	class Meta:
   		ordering = ['-tiempo']

	def  get_absolute_url(self):
   		return reverse("respuesta_detail", kwargs={"pk": self.pk})

	def Hijo(self):
		return Responder.objects.filter(padre=self)
