# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import Leave, ApplicationRequest, RemainingLeaves;
# Register your models here.

admin.site.register(Leave);
admin.site.register(ApplicationRequest);
admin.site.register(RemainingLeaves);
