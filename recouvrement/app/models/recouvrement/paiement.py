
from django.db import models
from .rubrique_variable import Variable,Compte,Banque
# from app.models.recouvrement import Eleve



class Eleve_reduction_prix(models.Model):
    id_reduction_prix = models.AutoField(primary_key=True)
    id_eleve = models.ForeignKey("Eleve",on_delete=models.PROTECT,null=False)
    id_campus = models.ForeignKey("Campus",on_delete=models.PROTECT,null=False)  
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)
    id_cycle_actif= models.ForeignKey("Classe_cycle_actif",on_delete=models.PROTECT,null=False) 
    id_classe_active= models.ForeignKey("Classe_active",on_delete=models.PROTECT,null=False) 
    id_variable = models.ForeignKey(Variable,on_delete=models.PROTECT,null=False)
    pourcentage = models.PositiveIntegerField()

    class Meta:
        db_table = 'recouvrment_reduction_prix'
        
        
    def __str__(self):
        return self.id_eleve



class Paiement(models.Model):
    id_paiement = models.AutoField(primary_key=True)
    id_variable = models.ForeignKey(Variable,on_delete=models.PROTECT,null=False)
    montant = models.PositiveIntegerField(default=0)
    id_banque = models.ForeignKey(Banque,on_delete=models.PROTECT,null=False)
    id_compte = models.ForeignKey(Compte,on_delete=models.PROTECT,null=False)
    date_saisie = models.DateField(auto_now_add= True)
    date_paie = models.DateField()
    bordereau = models.ImageField(upload_to='invoices/',null=True,blank=True)
    id_eleve = models.ForeignKey("Eleve",on_delete=models.PROTECT,null=False)
    id_campus = models.ForeignKey("Campus",on_delete=models.PROTECT,null=False)  
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)
    id_cycle_actif = models.ForeignKey("Classe_cycle_actif",on_delete=models.PROTECT,null=False) 
    id_classe_active= models.ForeignKey("Classe_active",on_delete=models.PROTECT,null=False) 
    status = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
    
    class Meta:
        db_table = 'recouvrment_paiement'
        
        
    def __str__(self):
        return self.montant
    

class PenaliteConfig(models.Model):
    id_penalite_regle = models.AutoField(primary_key=True)
    # Portée de la règle (NULL = global)
    id_annee = models.ForeignKey("Annee",on_delete=models.PROTECT,null=False)
    id_campus = models.ForeignKey("Campus", on_delete=models.PROTECT, null=True, blank=True)
    id_cycle_actif = models.ForeignKey("Classe_cycle_actif", on_delete=models.PROTECT, null=True, blank=True)
    id_classe_active = models.ForeignKey("Classe_active", on_delete=models.PROTECT, null=True, blank=True)
    id_variable = models.ForeignKey("Variable", on_delete=models.PROTECT, null=True, blank=True)
    id_annee_trimestre = models.ForeignKey("Annee_trimestre", on_delete=models.PROTECT, null=True, blank=True)
    type_penalite = models.CharField(max_length=20,choices=[('FORFAIT', 'Forfait'),('POURCENTAGE', 'Pourcentage'),])
    valeur = models.FloatField()  # montant ou %
    plafond = models.PositiveIntegerField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        db_table = "recouvrement_penalite_regle"
        unique_together = ('id_variable', 'id_annee_trimestre', 'id_classe_active', 'id_cycle_actif', 'id_campus')

    def __str__(self):
        cible = self.id_variable.variable if self.id_variable else "Toutes variables"
        tranche = self.id_annee_trimestre.trimestre if self.id_annee_trimestre else "Toutes périodes"
        return f"{cible} - {tranche} - {self.valeur}{'%' if self.type_penalite == 'POURCENTAGE' else ' FORFAIT'}"

