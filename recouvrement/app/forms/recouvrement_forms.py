
from django import forms
from app.models.recouvrement import (VariableCategorie,VariablePrix,Variable,Banque,
                                 Compte,VariableDatebutoire,VariableDerogation,
                                 Eleve_reduction_prix,Paiement)
from app.models.annee import Annee_trimestre
from app.models import *

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_variable'].queryset = Variable.objects.all()

        self.fields['id_annee_trimestre'].queryset = Annee_trimestre.objects.all()

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

class PaiementUpdateForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['id_variable', 'montant', 'id_compte', 'date_paie', 'bordereau']
        widgets = {
            'date_paie': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_compte': forms.Select(attrs={'class': 'form-control'}),
            'bordereau': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_variable': forms.Select(attrs={'class': 'form-control'}),
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

# form entree et sortie d'argent
class CategorieOperationForm(forms.ModelForm):
    class Meta:
        model = CategorieOperation
        fields = ['id_annee', 'id_campus', 'type_operation', 'nom', 'description']
        labels = {
            'id_annee': "Année",
            'id_campus': "Campus",
            'type_operation': "Type d'opération",
            'nom': "Nom de la catégorie",
            'description': "Description",

        }
        widgets = {
            'id_annee': forms.Select(attrs={'class': 'form-control'}),
            'id_campus': forms.Select(attrs={'class': 'form-control'}),
            'type_operation': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Fournitures scolaires'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la catégorie...'
            }),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['id_annee'].queryset = Annee.objects.filter(is_active=True)
    #     self.fields['id_campus'].queryset = Campus.objects.filter(is_active=True)

class OperationCaisseForm(forms.ModelForm):
    class Meta:
        model = OperationCaisse
        fields = [
            'id_annee', 'id_campus', 'categorie', 'montant',
            'date_operation', 'description', 'source_beneficiaire',
            'mode_paiement', 'reference', 'justificatif'
        ]
        labels = {
            'id_annee': 'Année',
            'id_campus': 'Campus',
            'categorie': 'Catégorie',
            'montant': 'Montant',
            'date_operation': 'Date',
            'description': 'Description',
            'source_beneficiaire': 'Source / Bénéficiaire',
            'mode_paiement': 'Mode de paiement',
            'reference': 'Référence (ex: N° chèque, référence...)',
            'justificatif': 'Justificatif (optionnel)', 
        }
        widgets = {
            'id_annee': forms.Select(attrs={'class': 'form-control'}),
            'id_campus': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Ex: 50000'}),
            'date_operation': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 2,'placeholder': 'Description de l\'opération...'}),
            'source_beneficiaire': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ex: Banque, Donateur, Fournisseur...'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control','placeholder': 'N° chèque, référence...'}),
            'justificatif': forms.FileInput(attrs={'class': 'form-control'}),}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id_annee' in self.data and 'id_campus' in self.data:
            try:
                annee_id = int(self.data.get('id_annee'))
                campus_id = int(self.data.get('id_campus'))
                self.fields['categorie'].queryset = CategorieOperation.objects.filter(
                    id_annee_id=annee_id,
                    id_campus_id=campus_id,
                    est_active=True
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['categorie'].queryset = CategorieOperation.objects.filter(
                id_annee=self.instance.id_annee,
                id_campus=self.instance.id_campus,
                est_active=True
            )
        else:
            self.fields['categorie'].queryset = CategorieOperation.objects.none()