# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from principal.models import Pregunta
from .forms import FormComentario
from .models import Responder

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


def view_ipk(request, pk):

	    instance = get_object_or_404(Pregunta, pk=pk)
	
	    inicializar_datos = {

		  "content_type":instance.get_content_type,
		  "object_id": instance.id

	    }

	    form = FormComentario(request.POST or None, initial=inicializar_datos)

   	    if form.is_valid():
                respuesta = form.cleaned_data.get("content_type")
                content_type =ContentType.objects.get(model=respuesta)
                obj_id = form.cleaned_data.get("object_id")
                content_data = form.cleaned_data.get("respuesta")
            
                padre_obj = None

                try:
                    padre_id=int(request.POST.get("padre_id"))
                except:
                    padre_id = None

                if padre_id:
                    padre_qs = Responder.objects.filter(id=padre_id)
                    if padre_qs.exists() and padre_qs.count()==1:
                        padre_obj = padre_qs.first()

                comentario, created= Responder.objects.get_or_create(

                                usuario = request.user,
                                object_id  = obj_id,
                                content_type = content_type,
                                respuesta = content_data,
                                padre = padre_obj

                )

                return HttpResponseRedirect(comentario.content_object.get_absolute_url())

                if created:
           	        print("yeah it worked")

	    comunidad = instance.comentarios
   
	    context = {

			'form':form,
			'instance':instance,
			'comunidad':comunidad,

	    }

	    return render(request, 'comentar/comentar.html', context)