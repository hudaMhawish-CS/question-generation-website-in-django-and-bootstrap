from django.contrib import admin
from .models import Board
# Register your models here.

admin.site.register(Board)

# change style admin
admin.site.site_header = "Question generation"
admin.site.site_title = "Question generation"