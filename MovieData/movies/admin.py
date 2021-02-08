from django.contrib import admin
from .models import *
# Register your models here.

class MoviesDataAdmin(admin.ModelAdmin):
  list_display = ["id","title",'rating','genres','released_year','update_at','create_at']
  
admin.site.register(MoviesData,MoviesDataAdmin)
