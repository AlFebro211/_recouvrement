from django.db import models
from app.models.annee import *

from phonenumber_field.modelfields import PhoneNumberField
from app.variables import *

class Eleve(models.Model):
    id_eleve = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=250,null=False)
    prenom = models.CharField(max_length=50,null=False)
    genre = models.CharField(max_length=50,choices=sexe_choices, default='M')
    etat_civil = models.CharField(max_length=50,choices=etat_civil_choices, default='Célibataire',null=True,blank=True)
    code_eleve = models.CharField(max_length=250,null=True,blank=True)
    code_annee = models.IntegerField(default=0,null=True,blank=True)
    matricule = models.CharField(max_length=50,null=True,blank=True)
    nom_pere = models.CharField(max_length=200, default='',null=True,blank=True)
    prenom_pere = models.CharField(max_length=200, default='',null=True,blank=True)
    nom_mere = models.CharField(max_length=200, default='',null=True,blank=True)
    prenom_mere = models.CharField(max_length=200, default='',null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    email_parent = models.EmailField(null=True,blank=True)
    password_parent=models.CharField(max_length=300,null=True,blank=True)
    password=models.CharField(max_length=300,null=True,blank=True)
    tutaire = models.CharField(max_length=250,null=True,blank=True)
    telephone = PhoneNumberField(region='BI', null=True, blank=True)
    date_naissance = models.DateField(auto_now_add=True)
    naissance_region = models.CharField(max_length=30, default='',null=True,blank=True)
    naissance_pays = models.CharField(max_length=30, default='',null=True,blank=True)
    naissance_province = models.CharField(max_length=30, default='',null=True,blank=True)
    naissance_commune = models.CharField(max_length=30, default='',null=True,blank=True)
    naissance_zone = models.CharField(max_length=30, default='',null=True,blank=True)
    province_actuelle = models.CharField(max_length=20, default='',null=True,blank=True)
    commune_actuelle = models.CharField(max_length=20, default='',null=True,blank=True)
    zone_actuelle = models.CharField(max_length=20, default='',null=True,blank=True)
    imageUrl = models.ImageField(upload_to='logos/eleves/', blank=True, null=True)
    nationalite = models.CharField(max_length=50, default='',null=True,blank=True)
    professionPere = models.CharField(max_length=100, default='',null=True,blank=True)
    professionMere = models.CharField(max_length=100, default='',null=True,blank=True)
    profsion_tutaire= models.CharField(max_length=100, default='',null=True,blank=True)
    IDelivranceLieuEtDate = models.CharField(max_length=100, default='',null=True,blank=True)
    code_secret_parent = models.CharField(max_length=250,null=True,blank=True)
    code_secret_eleve = models.CharField(max_length=250,null=True,blank=True)
   
    
    def __str__(self):
        return f'{self.nom} {self.prenom}'

    class Meta:
        db_table = 'eleve'

class Eleve_inscription(models.Model):
    id_inscription = models.AutoField(primary_key=True)
    date_inscription = models.DateField(auto_now_add=True)
    id_eleve = models.ForeignKey("Eleve", on_delete=models.PROTECT,null=False)  
    id_trimestre = models.ForeignKey(Annee_trimestre,on_delete=models.PROTECT,null=False)
    id_campus = models.ForeignKey("Campus",on_delete=models.PROTECT,null=False)
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)
    id_classe_cycle = models.ForeignKey("Classe_cycle_actif", on_delete=models.PROTECT, null=False)
    id_classe = models.ForeignKey("Classe_active",on_delete=models.PROTECT,null=False)
    redoublement = models.BooleanField(default=False) 
    status = models.BooleanField(default=True) 
    isDelegue = models.BooleanField(default=False)  

    def __str__(self):
        return f'{self.id_eleve.nom} {self.id_eleve.prenom}'

    class Meta:
        db_table = 'eleve_inscription'
