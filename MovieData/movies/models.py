from django.db import models
# import jsonfield

# Create your models here.

class MoviesData(models.Model):
	id= models.CharField(max_length=200,unique=True,primary_key=True)
	title = models.CharField(max_length=700,null=True,blank=True)
	released_year=models.CharField(max_length=50,null=True,blank=True)
	rating = models.FloatField(default=0)
	genres = models.TextField(null=True,blank=True)
	update_at = models.DateTimeField(auto_now=True)
	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.title} released in {self.released_year}'