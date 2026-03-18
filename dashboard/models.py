from django.db import models

class Flood_report (models.Model):
    region= models.CharField(max_length=50)
    water_level= models.CharField(max_length=50)
    severity= models.CharField(max_length=50)
    displaced_people= models.IntegerField()
    death_toll= models.IntegerField()
   

    def __str__(self):
        return self.region

