from django.db import models
from app.variables import *

class Trimestre(models.Model):
    id_trimestre = models.AutoField(primary_key=True)
    trimestre = models.CharField(max_length=20,null=False,choices=trimestres_default) 
    # etat_trimestre = models.CharField(max_length=50, choices=etat_annee, default='En attente') 
    # date_ouverture = models.DateField(null=True,blank=True)  
    # date_cloture = models.DateField(null=True,blank=True)  
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "Trimestre" 
        verbose_name = "Trimestre"
        # verbose_name_plural = "Années scolaires"

    def __str__(self):
        return f"{self.trimestre}"

class Periode(models.Model):
    id_periode = models.AutoField(primary_key=True) 
    periode = models.CharField(max_length=20,null=False,choices=periodes_default) 
    id_trimestre = models.ForeignKey("Trimestre",on_delete=models.PROTECT,null=False) 
    # date_debut = models.DateField(null=True,blank=True)  
    # date_fin = models.DateField(null=True,blank=True)
    # etat_periode = models.CharField(max_length=50, choices=etat_annee, default='En attente') 
    is_active = models.BooleanField(default=True)
    

    class Meta:
        db_table = "periode"  
        verbose_name = "periode"
        # verbose_name_plural = "Années scolaires"

    def __str__(self):
        return f"{self.periode}"


class Annee(models.Model):
    id_annee = models.AutoField(primary_key=True)
    debut = models.IntegerField(null=True, blank=True)  
    fin = models.IntegerField(null=True, blank=True)  
    annee = models.CharField(max_length=20,null=False) 
    etat_annee = models.CharField(max_length=50, choices=etat_annee, default='En attente') 
    date_ouverture = models.DateField()  
    date_cloture = models.DateField()  
    is_active = models.BooleanField(default=True)
     
    class Meta:
        db_table = "annee"  
        verbose_name = "Année_scolaire"

    def __str__(self):
        return f"{self.annee}"


class Annee_periode(models.Model):
    id_periode = models.AutoField(primary_key=True) 
    periode = models.ForeignKey("Periode",on_delete=models.PROTECT,null =False) 
    debut = models.DateField(null=True,blank=True) 
    fin = models.DateField(null=True,blank=True) 
    etat_periode = models.CharField(max_length=50, choices=etat_annee, default='En attente') 
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False) 
    id_campus = models.ForeignKey("Campus",on_delete = models.PROTECT,null=False) 
    id_cycle = models.ForeignKey("Classe_cycle_actif",on_delete=models.PROTECT,null=False) 
    id_classe = models.ForeignKey("Classe_active",on_delete=models.PROTECT,null=False) 
    id_trimestre_annee = models.ForeignKey('Annee_trimestre',on_delete=models.PROTECT,null=False)
    
    class Meta:
        db_table = "annee_periode"  
        verbose_name = "Période_AnnéeScolaire"
        # verbose_name_plural = "Périodes d'années scolaires"

    def __str__(self):
        return f"{self.periode.periode} "
    
    
class Annee_trimestre(models.Model):
    id_trimestre = models.AutoField(primary_key=True)  
    trimestre = models.ForeignKey('Trimestre',on_delete=models.PROTECT,null=False)
    debut = models.DateField(null=True,blank=True) 
    fin = models.DateField(null=True,blank=True) 
    etat_trimestre = models.CharField(max_length=50, choices=etat_annee, default='En attente') 
    id_cycle = models.ForeignKey("Classe_cycle_actif",on_delete=models.PROTECT,null=False) 
    id_classe = models.ForeignKey("Classe_active",on_delete=models.PROTECT,null=False)  
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False) 
    id_campus = models.ForeignKey("Campus",on_delete = models.PROTECT,null=False) 

    class Meta:
        db_table = "annee_trimestre" 
        verbose_name = "Trimestre_AnnéeScolaire"
        # verbose_name_plural = "Trimestres d'années scolaires"

    def __str__(self):
        return f"{self.trimestre.trimestre}"

