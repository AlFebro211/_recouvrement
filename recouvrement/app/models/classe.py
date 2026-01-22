from django.db import models
from app.variables import groupes,cycles_list
# from app.models.eleves import Eleve

class Classe(models.Model):
    id_classe = models.AutoField(primary_key=True) 
    classe = models.CharField(max_length=50,null=False,unique=True)  
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "classes" 
        verbose_name = "Classe"
        # verbose_name_plural = "Classes"

    def __str__(self):
        return self.classe

class CycleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
class Classe_cycle(models.Model):
    id_cycle = models.AutoField(primary_key=True) 
    cycle = models.CharField(max_length=200, null=False,unique=True,choices=cycles_list)  
    is_active = models.BooleanField(default=True)
    
     # Manager par défaut (retourne uniquement les campus actifs)
    objects = CycleManager()
    # Manager pour accéder à tous les campus (actifs et inactifs)
    all_objects = models.Manager()
    
    class Meta:
        db_table = "classe_cycle"  
        verbose_name = "Cycle de Classe"
        # verbose_name_plural = "Cycles de Classe"
    def __str__(self):
        return self.cycle

class Classe_active(models.Model):
    id_classe_active = models.AutoField(primary_key=True) 
    id_campus = models.ForeignKey("Campus",on_delete=models.PROTECT,null=False)  
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)
    cycle_id = models.ForeignKey("Classe_cycle_actif",on_delete=models.PROTECT,null=False) 
    classe_id = models.ForeignKey("Classe",on_delete=models.PROTECT,null=False) 
    groupe = models.CharField(max_length=10,choices=groupes,null=True, blank=True)
    isTerminale = models.BooleanField(default=False) 
    is_active  = models.BooleanField(default= True)
    date_creation = models.DateField(auto_now_add=True)
    ordre = models.PositiveIntegerField(null=True,blank=True)
    
    class Meta:
        db_table = "classe_active" 
        verbose_name = "Classe Active"
        # verbose_name_plural = "Classes Actives"

    def __str__(self):
        return f"{self.id_campus}-{self.classe_id}"

class Classe_cycle_actif(models.Model):
    id_cycle_actif = models.AutoField(primary_key=True) 
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)  
    id_campus = models.ForeignKey("Campus",on_delete=models.PROTECT,null=False) 
    cycle_id = models.ForeignKey("Classe_cycle",on_delete=models.PROTECT,null=False) 
    role = models.CharField(max_length=255,null=True,blank=True) 
    is_active  = models.BooleanField(default= True)
    date_creation = models.DateField(auto_now_add=True)
    nbre_classe_par_cycle_actif = models.PositiveIntegerField(default=1,null=True,blank=True)
    ordre = models.PositiveIntegerField(null=True,blank=True)
    
    class Meta:
        db_table = "classe_cycle_actif"  
        verbose_name = "Cycle Actif"
        # verbose_name_plural = "Cycles Actifs"
        
    def __str__(self):
        return f"{self.cycle_id.cycle}"
  

