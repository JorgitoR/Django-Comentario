# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Pregunta, Usuario

admin.site.register(Pregunta)
admin.site.register(Usuario)