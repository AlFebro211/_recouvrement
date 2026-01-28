
from django import forms
from app.models.recouvrement import (VariableCategorie,VariablePrix,Variable,Banque,
                                 Compte,VariableDatebutoire,VariableDerogation,
                                 Eleve_reduction_prix,Paiement)
from app.models.annee import Annee_trimestre
from app.models import PenaliteConfig

class VariableForm(forms.ModelForm):
    class Meta:
        model = Variable
        fields = ['id_variable_categorie','variable']
        labels = {
            'id_variable_categorie': "Catégorie de variable",
        }
        widgets = {
            'id_variable_categorie': forms.Select(attrs={'class': 'form-select'}),
            
        }


class VariableCategorieForm(forms.ModelForm):
    class Meta:
        model = VariableCategorie
        fields = ['nom']
        labels = {
            'nom': "Nom de la catégorie",
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Minerval'}),
        }


class VariablePrixForm(forms.ModelForm):
    class Meta:
        model = VariablePrix
        fields = [ 'id_campus','id_annee','id_classe_active','id_cycle_actif']
        labels = {
            'prix': "prix",
            'id_classe_active': "Classe",
            
        }
        widgets = {
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

class BanqueForm(forms.ModelForm):
    class Meta:
        model = Banque
        fields = ['banque', 'sigle']
        labels = {
            'banque': "Nom de la banque",
            'sigle': "Sigle (optionnel)",
        }
        widgets = {
            'banque': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Banque Commerciale du Burundi'
            }),
            'sigle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: BCB'
            }),
        }

class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['id_banque','compte']
        labels = {
            'compte': "Numéro de compte",
            'id_banque': "Banque associée",
        }
        widgets = {
            'compte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 001-123456789-00-45'
            }),
            'id_banque': forms.Select(attrs={'class': 'form-select'}),
        }

class VariablePrixForm(forms.ModelForm):
    class Meta:
        model = VariablePrix
        fields = ['id_annee', 'id_classe_active','id_annee_trimestre', 'id_variable', 'prix']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # 🔒 Vide par défaut
            self.fields['id_annee_trimestre'].queryset = Annee_trimestre.objects.none()
            self.fields['id_variable'].queryset = Variable.objects.none()
        labels = {
            'id_variable': "Frais scolaire / Variable",
            'prix': "Montant (Prix)",
            'id_annee': "Année scolaire",
            'id_classe_active': "Classe",
            'id_annee_trimestre': "Trimestre",
        }
        widgets = {
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            'id_annee_trimestre': forms.Select(attrs={'class': 'form-select'}),
            'id_variable': forms.Select(attrs={'class': 'form-select'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 50000'}),
    }
        

class VariableDerogationForm(forms.ModelForm):
    class Meta:
        model = VariableDerogation
        fields = [
            'id_campus',
            'id_annee',
            'id_cycle_actif',
            'id_classe_active',
            'id_eleve',
            # 'date_butoire',
        ]
        labels = {
            'id_eleve': "Eleve",
            'id_campus': "Campus",
            'id_annee': "Année scolaire",
            'id_cycle_actif': "Cycle",
            'id_classe_active': "Classe",
            # 'date_butoire': "Date butoir (derogation)",
        }
        widgets = {
            'id_eleve': forms.Select(attrs={'class': 'form-select'}),
            'id_campus': forms.Select(attrs={'class': 'form-select'}),
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_cycle_actif': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            # 'date_butoire': forms.DateInput(
            #     attrs={
            #         'class': 'form-control',
            #         'type': 'date'
            #     }
            # ),
        }

class VariableDateButoireForm(forms.ModelForm):
    class Meta:
        model = VariableDatebutoire
        fields = [
            'id_campus',
            'id_annee',
            'id_cycle_actif',
            'id_classe_active',
            # 'id_variable',
            # 'date_butoire',
        ]
        labels = {
            'id_campus': "Campus",
            'id_annee': "Année scolaire",
            'id_cycle_actif': "Cycle",
            'id_classe_active': "Classe",
            # 'date_butoire': "Date butoir (derogation)",
        }
        widgets = {
            'id_variable': forms.Select(attrs={'class': 'form-select'}),
            'id_campus': forms.Select(attrs={'class': 'form-select'}),
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_cycle_actif': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            
        }


class VariableReductionForm(forms.ModelForm):
    class Meta:
        model = Eleve_reduction_prix
        fields = [
            'id_campus',
            'id_annee',
            'id_cycle_actif',
            'id_classe_active',
            'id_eleve',
        ]
        labels = {
            'id_eleve': "Eleve",
            'id_campus': "Campus",
            'id_annee': "Année scolaire",
            'id_cycle_actif': "Cycle",
            'id_classe_active': "Classe",
    
             
        }
        widgets = {
            'id_eleve': forms.Select(attrs={'class': 'form-select'}),
            'id_campus': forms.Select(attrs={'class': 'form-select'}),
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_cycle_actif': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            
        }



class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = [
            # 'id_campus',
            'id_annee',
            # 'id_cycle_actif',
            'id_classe_active',
            'id_eleve',
            'id_variable',
            # 'id_banque',
            'id_compte',
            'montant',
            'bordereau',
            'date_paie',
            
        ]
        labels = {
            # 'id_campus': "Campus",
            'id_annee': "Année scolaire",
            # 'id_cycle_actif': "Cycle",
            'id_classe_active': "Classe",
            'id_eleve':'Elève',
            'id_variable':'Variable',
            'id_banque':'Banque',
            'id_compte':'Compte',
            'bordereau':'Image de bordereau',
            'montant':'montant',
            'date_paie':'Date de paiement'
            
            # 'date_butoire': "Date butoir (derogation)",
        }
        widgets = {
            'id_variable': forms.Select(attrs={'class': 'form-select'}),
            'id_campus': forms.Select(attrs={'class': 'form-select'}),
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_cycle_actif': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            'id_compte': forms.Select(attrs={'class': 'form-select'}),
            'date_paie': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bordereau': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
            
            
        }


class PenaliteForm(forms.ModelForm):
    class Meta:
        model = PenaliteConfig
        fields = [
            'id_campus',
            'id_annee',
            'id_cycle_actif',
            'id_classe_active',
            'id_annee_trimestre',
            'id_variable',
            'type_penalite',
            'valeur',
            'plafond',
        ]
        labels = {
            'id_campus': "Campus",
            'id_annee': "Année",
            'id_cycle_actif': "Cycle",
            'id_classe_active': "Classe",
            'id_variable': "Variable (optionnel)",
            'id_annee_trimestre': "Trimestre",
            'type_penalite': "Type de pénalité",
            'valeur': "Valeur de la pénalité",
            'plafond': "Plafond (uniquement si %)",
        }
        widgets = {
            'id_campus': forms.Select(attrs={'class': 'form-select'}),
            'id_annee': forms.Select(attrs={'class': 'form-select'}),
            'id_cycle_actif': forms.Select(attrs={'class': 'form-select'}),
            'id_classe_active': forms.Select(attrs={'class': 'form-select'}),
            'id_annee_trimestre': forms.Select(attrs={'class': 'form-select'}),
            'id_variable': forms.Select(attrs={'class': 'form-select'}),
            'type_penalite': forms.Select(attrs={'class': 'form-select'}),
            'valeur': forms.NumberInput(attrs={'class': 'form-control'}),
            'plafond': forms.NumberInput(attrs={'class': 'form-control'}),
        }
