
from django.db import models
# from app.models.eleves import Eleve

class CampusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
class Campus(models.Model):
    id_campus = models.AutoField(primary_key=True) 
    campus = models.CharField(max_length=50,null=False,unique=True)  
    adresse = models.CharField(max_length=255,null=False) 
    localisation = models.CharField(max_length=255,null=True,blank=True) 
    is_active = models.BooleanField(default=True)
    
    # Manager par défaut (retourne uniquement les campus actifs)
    objects = CampusManager()
    # Manager pour accéder à tous les campus (actifs et inactifs)
    all_objects = models.Manager()

    class Meta:
        db_table = "campus" 
        verbose_name = "Campus"
        # verbose_name_plural = "Campus"

    def __str__(self):
        return self.campus
   