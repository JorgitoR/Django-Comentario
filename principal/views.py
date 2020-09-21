# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from .models import Pregunta

def inicio(request):

	post = Pregunta.objects.all()

	context = {
		'post':post
	}

	return render(request, 'inicio.html', context)