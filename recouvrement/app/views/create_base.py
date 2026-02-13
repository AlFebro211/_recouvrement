from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from app import models
from app.forms.recouvrement_forms import (VariableCategorieForm,VariableCategorie,Variable,
                                VariableForm,BanqueForm,CompteForm,Compte,Banque,
                                VariablePrixForm,VariablePrix,VariableDerogationForm,
                                VariableDerogation,VariableReductionForm,Eleve_reduction_prix,
                                VariableDatebutoire,VariableDateButoireForm,PaiementForm,Paiement,PenaliteForm)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404
from app.models import Classe_active,Annee

import logging
import datetime
from django.db.models import Sum, Count
from app.models import *


logger = logging.getLogger(__name__)
import os



def ajouter_categorie_variable(request):
   
    if request.method == "POST":
        form = VariableCategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"La categorie créee avec succès")
            return redirect('categorie_variable')
    else:
        form = VariableCategorieForm()
    variablesCategories = VariableCategorie.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'variable_categorie': variablesCategories,
        'form_variable_categorie': form,
        'form_type': 'variablecategorie_form',
       

    })
    
    

def ajouter_variable(request):

    if request.method == "POST":
        form = VariableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"La variable  créee avec succès")
            return redirect('create_variable_frais')
    else:
        form = VariableForm()
    variablesList = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'variableList': variablesList,
        'form_variable': form,
        'form_type': 'variable_form',
       

    })
    
    
    

def ajouter_banque_epargne(request):
    if request.method == "POST":
        form = BanqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"La Banque a été créee avec succès")
            return redirect('create_banque')
    else:
        form = BanqueForm()
    banqueList = Banque.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'banque_list': banqueList,
        'form_banque': form,
        'form_type': 'banque_form',
      

    })


def ajouter_compte_epargne(request):
    if request.method == "POST":
        compte = request.POST.get('compte')
        form = CompteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Le compte a été créee avec succès")
            return redirect('create_compte')
    else:
        form = CompteForm()
    compteList = Compte.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'compte_list': compteList,
        'form_compte': form,
        'form_type': 'compte_form',
       

    })
    


def ajouter_variable_prix(request):
    
    if request.method == "POST":
        form = VariablePrixForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Le prix pour la variable choisi a été créee avec succès")
            return redirect('create_compte')
    else:
        form = VariablePrixForm()
    variableprixList = VariablePrix.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'variable_prix_list': variableprixList,
        'form_variable_prix': form,
        'form_type': 'variable_prix_form',
       

    })


def add_paiement_for_anyclass(request):
    if request.method == "POST":
        form = PaiementForm(request.POST)
        if form.is_valid():
            print("Formulaire valide ✅")
            print("Champs nettoyés (cleaned_data) :")
            for key, value in form.cleaned_data.items():
                print(f"{key} = {value}")

            paiement = form.save(commit=False) 

            compte = paiement.id_compte
            if not compte:
                messages.error(request, "Veuillez sélectionner un compte.")
                return redirect('create_compte')

            paiement.id_banque = compte.id_banque
            classe_active = paiement.id_classe_active
            if not classe_active:
                messages.error(request, "Classe active manquante.")
                return redirect('create_compte')

            paiement.id_campus = classe_active.id_campus  
            paiement.id_cycle_actif = classe_active.cycle_id
            paiement.status = True


            paiement.save() 
            # form.save()
            messages.success(request,"Le paiement a été enregistré avec succès")
            return redirect('create_compte')
    else:
        form = PaiementForm()
    annees = Annee.objects.all()
    print("Années disponibles:", annees)

    paiementList = Paiement.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'paiement_list': paiementList,
        'form_paiement': form,
        'form_type': 'paiement_form',
        'annees': annees,
        
    })
    



def ajouter_variable_derogation(request):
    
    form = VariableDerogationForm()
    is_derog = True
    derogationList = VariableDerogation.objects.all()
    variables_list = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'derogation_list': derogationList,
        'variable_list': variables_list,
        'form_derogation': form,
        'derogationField':is_derog,
        'form_type': 'derogation_form',
       

    })
    
    

def ajouter_reduction_for_pupil(request):
    
    form = VariableReductionForm()
    is_reduct = True
    variables_list = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'variable_list': variables_list,
        'form_reduction': form,
        'reductionField':is_reduct,
        'form_type': 'reduction_form',
       

    })


def ajouter_date_butoire_for_anyclass(request):
  
    form = VariableDateButoireForm()
    is_butoire = True
    variables_list = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'variable_list': variables_list,
        'form_butoire': form,
        'butoireField':is_butoire,
        'form_type': 'butoire_form',
        

    })

def ajouter_penalite(request):
    form = PenaliteForm()
    variables_list = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'form_penalite': form,
        'form_type': 'penalite_form',
        'variable_list': variables_list,
    })

def eleves_penalite(request):
    return render(request, 'recouvrement/index_recouvrement.html', {
        'eleves_en_penalite_form': True,
        'form_type': 'eleves_en_penalite_form',
        'annees': Annee.objects.all(),
        'classes': Classe_active.objects.all(),
        'trimestres': ['Trimestre 1','Trimestre 2','Trimestre 3','Trimestre 4','Trimestre 5'],
        'variables': Variable.objects.all(),
    })


def historique(request):
    return render(request, 'recouvrement/index_recouvrement.html', {
        'historique_financier_form': True,
        'form_type': 'historique_financier_form',
        'annees': Annee.objects.all(),
        'comptes_bancaires': Compte.objects.select_related('id_banque').all(),
        'classes': Classe_active.objects.all(),  
        'trimestres': ['Trimestre 1','Trimestre 2','Trimestre 3','Trimestre 4','Trimestre 5'],
        'variables_list': Variable.objects.all(),  
        'eleves': Eleve_inscription.objects.all(),  
    })

def dette_anterieures(request):
    return render(request, 'recouvrement/index_recouvrement.html', {
        'dette_anterieures_form': True,
        'form_type': 'dette_anterieures_form',
        'annees': Annee.objects.all(),
        'comptes_bancaires': Compte.objects.select_related('id_banque').all(),
        'classes': Classe_active.objects.all(),  
        'trimestres': ['Trimestre 1','Trimestre 2','Trimestre 3','Trimestre 4','Trimestre 5'],
        'variables_list': Variable.objects.all(),  
        'eleves': Eleve_inscription.objects.all(),  
    })

def update_paiement(request):
    return render(request, 'recouvrement/index_recouvrement.html', {
        'update_paiement_form': True,
        'form_type': 'paiement_update_form',
        'annees': Annee.objects.all(),
        'comptes_bancaires': Compte.objects.select_related('id_banque').all(),
        'classes': Classe_active.objects.all(),
    })

def suivi_reduction_derogation(request):
    # page HTML avec formulaire et tableau
    annees = Annee.objects.all()  # exemple
    variables = Variable.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'suivi_reduction_derogation_form': True,
        'form_type': 'suivi_reduction_derogation_form',
        'annees': annees,
        'variables': variables,
    })
def situation_journaliere(request):
    annees = Annee.objects.all()  
    variables = Variable.objects.all()
    paiements = Paiement.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'situation_journaliere_form': True,
        'form_type': 'situation_journaliere_form',
        'annees': annees,
        'variables': variables,
        'paiements': paiements,
    })

@csrf_protect
def save_paiement(request):
    if request.method == 'POST':
        try:
            logger.info(f"Données reçues : {request.POST}, Fichiers : {request.FILES}")
            print("POST brut :", request.POST)
            form = PaiementForm(request.POST, request.FILES)
            if form.is_valid():
                print("Formulaire valide ✅")
                print("Champs nettoyés (cleaned_data) :")
                for key, value in form.cleaned_data.items():
                    print(f"{key} = {value}")

                logger.info(f"Données validées : {form.cleaned_data}")
                id_annee = form.cleaned_data['id_annee'].id_annee
                id_classe_active = form.cleaned_data['id_classe_active'].id_classe_active
                id_eleve = form.cleaned_data['id_eleve'].id_eleve
                id_variable = form.cleaned_data['id_variable'].id_variable
                # id_banque = form.cleaned_data['id_banque'].id_banque
                id_compte = form.cleaned_data['id_compte'].id_compte
                montant = form.cleaned_data['montant']
                date_paie = form.cleaned_data['date_paie']
                bordereau = form.cleaned_data['bordereau']

                if isinstance(date_paie, datetime.datetime):
                    date_paie = date_paie.date()
                today = datetime.date.today()
                if date_paie > today:
                    return JsonResponse({
                        'success': False,
                        'error': f"La date de paiement ({date_paie}) ne peut pas être antérieure à aujourd'hui ({today})."
                    })

                try:
                    compte = Compte.objects.get(id_compte=id_compte)
                except Compte.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Compte non trouvé.'}, status=404)

                id_banque = compte.id_banque.id_banque if compte.id_banque else None
                print(f"Compte choisi : {compte}, Banque : {id_banque}")

                # if Paiement.objects.filter(
                #     id_eleve_id=id_eleve,
                #     id_variable_id=id_variable,
                #     date_paie=date_paie
                # ).exists():
                #     return JsonResponse({
                #         'success': False,
                #         'error': 'Ce paiement existe déjà.'
                #     }, status=400)

                try:
                    classe_active = Classe_active.objects.get(id_classe_active=id_classe_active)
                    id_campus = classe_active.id_campus.id_campus
                    id_cycle_actif = classe_active.cycle_id.id_cycle_actif
                except Classe_active.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Classe active non trouvée.'
                    }, status=404)
                
                try:
                    variable_date_butoire = VariableDatebutoire.objects.get(
                        id_variable_id=id_variable,
                        id_annee_id=id_annee,
                        id_campus_id=id_campus,
                        id_cycle_actif_id=id_cycle_actif,
                        id_classe_active_id=id_classe_active
                    )
                except VariableDatebutoire.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': "Aucune date butoire définie pour cette variable."
                    }, status=400)

                date_limite = variable_date_butoire.date_butoire

                derogation = VariableDerogation.objects.filter(
                    id_eleve_id=id_eleve,
                    id_variable_id=id_variable,
                    id_annee_id=id_annee,
                    id_campus_id=id_campus,
                    id_cycle_actif_id=id_cycle_actif,
                    id_classe_active_id=id_classe_active
                ).first()

                if derogation:
                    date_limite = derogation.date_derogation

                try:
                    variable_prix = VariablePrix.objects.get(
                        id_variable_id=id_variable,
                        id_annee_id=id_annee,
                        id_campus_id=id_campus,
                        id_cycle_actif_id=id_cycle_actif,
                        id_classe_active_id=id_classe_active
                    )
                except VariablePrix.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Aucun prix défini pour cette variable.'
                    }, status=400)

                prix_max = variable_prix.prix

                reduction = Eleve_reduction_prix.objects.filter(
                    id_eleve_id=id_eleve,
                    id_variable_id=id_variable,
                    id_annee_id=id_annee,
                    id_campus_id=id_campus,
                    id_cycle_actif_id=id_cycle_actif,
                    id_classe_active_id=id_classe_active
                ).first()

                montant_autorise = prix_max  

                if reduction:
                    pourcentage = reduction.pourcentage
                    montant_reduction = (prix_max * pourcentage) / 100
                    montant_autorise = prix_max - montant_reduction

                    print(f"Réduction appliquée: {pourcentage}%")
                    print(f"Prix normal: {prix_max}")
                    print(f"Montant autorisé après réduction: {montant_autorise}")

                # ========================== Vérification cumul ==========================
                total_deja_paye = Paiement.objects.filter(
                    id_eleve_id=id_eleve,
                    id_variable_id=id_variable,
                ).aggregate(total=Sum('montant'))['total'] or 0

                if total_deja_paye + montant > montant_autorise:
                    montant_restant = montant_autorise - total_deja_paye
                    message = (
                    f"Le paiement dépasse le montant autorisé pour cette variable.\n"
                    f"Montant à payer : {montant_autorise}\n"
                    f"Déjà payé : {total_deja_paye}\n"
                    f"Montant restant à payer : {montant_restant}\n"
                )
                    
                    if reduction:
                        message = (
                            f"L'élève bénéficie d'une réduction de {reduction.pourcentage}%.\n"
                            f"Montant à payer : {montant_autorise}\n"
                            f"Déjà payé : {total_deja_paye}\n"
                            f"Montant restant à payer : {montant_restant}\n"
                        )

                    return JsonResponse({
                        'success': False,
                        'error': message
                    })
                
                paiement = Paiement(
                    id_variable_id=id_variable,
                    montant=montant,
                    id_banque_id=id_banque,
                    id_compte_id=id_compte,
                    date_paie=date_paie,
                    id_eleve_id=id_eleve,
                    id_campus_id=id_campus,
                    id_annee_id=id_annee,
                    id_cycle_actif_id=id_cycle_actif,
                    id_classe_active_id=id_classe_active,
                    status = True
                )

                if bordereau:
                    paiement.save()
                    file_extension = os.path.splitext(bordereau.name)[1]  
                    new_filename = f"{bordereau.name}_{paiement.id_paiement}"
                    paiement.bordereau.save(new_filename, bordereau, save=False)
                    paiement.bordereau.name = new_filename
                    paiement.save()
                else:
                    paiement.save()

                logger.info(f"Paiement enregistré: id={paiement.id_paiement}, eleve={id_eleve}, annee={id_annee}, campus={id_campus}, cycle={id_cycle_actif}, classe={id_classe_active}, variable={id_variable}, montant={montant}, banque={id_banque}, compte={id_compte}, date={date_paie}, bordereau={paiement.bordereau.name if paiement.bordereau else None}")

                return JsonResponse({'success': True})
            else:
                errors = form.errors.as_json()
                logger.warning(f"Erreurs de validation du formulaire Paiement: {errors}")
                return JsonResponse({
                    'success': False,
                    'error': 'Erreurs de validation du formulaire.',
                    'details': errors
                }, status=400)
        except Exception as e:
            logger.error(f"Erreur dans save_paiement: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée.'
    }, status=405)


def dashboard(request):

    context = {
        'annees': Annee.objects.all(),
        'classes': Classe.objects.all(),
        'campus': Campus.objects.all(),
        'cycles': Classe_cycle_actif.objects.all(),
    }

    return render(request,'recouvrement/index_recouvrement.html',context)



from django.db.models import Sum
from django.http import JsonResponse

def dashboard_data(request):
    annee = request.GET.get('annee')
    classe_id = request.GET.get('classe')
    eleve_id = request.GET.get('eleve')
    trimestre_id = request.GET.get('trimestre')
    variable_id = request.GET.get('variable')

    if not annee:
        return JsonResponse({'success': False})

    # =======================
    # Récupération classe si existante
    # =======================
    classe_active = None
    campus_id = None
    cycle_id = None
    if classe_id and classe_id.isdigit():
        classe_active = Classe_active.objects.filter(id_classe_active=int(classe_id)).first()
        if classe_active:
            campus_id = classe_active.id_campus
            cycle_id = classe_active.cycle_id

    # =======================
    # Élèves actifs selon filtres
    # =======================
    eleves = Eleve_inscription.objects.filter(id_annee_id=annee, status=True)
    if classe_active:
        eleves = eleves.filter(
            id_classe_id=classe_active.id_classe_active,
            id_campus_id=campus_id,
            id_classe_cycle_id=cycle_id
        )
    if eleve_id and eleve_id.isdigit():
        eleves = eleves.filter(id_eleve_id=int(eleve_id))

    eleves_ids = list(eleves.values_list('id_eleve_id', flat=True))

    # =======================
    # Variables selon filtre
    # =======================
    variables_prix = VariablePrix.objects.filter(id_annee_id=annee)
    if classe_active:
        variables_prix = variables_prix.filter(id_classe_active_id=classe_active.id_classe_active)
    if variable_id and variable_id.isdigit():
        variables_prix = variables_prix.filter(id_variable_id=int(variable_id))
    if trimestre_id and trimestre_id.isdigit():
        variables_prix = variables_prix.filter(id_annee_trimestre_id=int(trimestre_id))

    # =======================
    # Paiements filtrés
    # =======================
    paiements = Paiement.objects.filter(
        id_annee_id=annee,
        status=True,
        id_eleve_id__in=eleves_ids,
        id_variable_id__in=variables_prix.values_list('id_variable', flat=True)
    )

    total_paye = paiements.aggregate(total=Sum('montant'))['total'] or 0
    total_transactions = paiements.count()

    # Paiements rejetés
    paiements_rejetes = Paiement.objects.filter(
        id_annee_id=annee,
        is_rejected=True,
        id_eleve_id__in=eleves_ids,
        id_variable_id__in=variables_prix.values_list('id_variable', flat=True)
    )
    total_rejete = paiements_rejetes.count()

    # Montant attendu et dettes
    total_attendu = 0
    eleves_en_dette_set = set()

    for vp in variables_prix:
        prix = vp.prix
        for e_id in eleves_ids:
            reduction = Eleve_reduction_prix.objects.filter(
                id_variable_id=vp.id_variable,
                id_eleve_id=e_id,
                id_annee_id=annee
            ).first()

            attendu = prix
            if reduction:
                attendu -= (prix * reduction.pourcentage)/100

            total_attendu += attendu

            total_paye_eleve = Paiement.objects.filter(
                id_variable_id=vp.id_variable,
                id_eleve_id=e_id,
                id_annee_id=annee,
                status=True,
                is_rejected=False
            ).aggregate(total=Sum('montant'))['total'] or 0

            if total_paye_eleve < attendu:
                eleves_en_dette_set.add(e_id)

    reste_a_payer = max(total_attendu - total_paye, 0)

    return JsonResponse({
        'success': True,
        'stats': {
            'total_transactions': total_transactions,
            'total_paye': total_paye,
            'total_attendu': total_attendu,
            'reste_a_payer': reste_a_payer,
            'eleves_en_dette': len(eleves_en_dette_set),
            'total_rejete': total_rejete
        }
    })

from django.db.models import Sum
from django.http import JsonResponse

def dashboard_details(request):
    annee = request.GET.get('annee')
    classe_id = request.GET.get('classe')
    variable_id = request.GET.get('variable')
    type_stat = request.GET.get('type')
    eleve_id = request.GET.get('eleve')
    trimestre_id = request.GET.get('trimestre')

    if not annee:
        return JsonResponse({'success': False, 'rows': []})

    rows = []
    title = ""

    # =======================
    # Classe active
    # =======================
    classe_active = None
    campus_id = None
    cycle_id = None
    if classe_id and classe_id.isdigit():
        classe_active = Classe_active.objects.filter(id_classe_active=int(classe_id)).first()
        if classe_active:
            campus_id = classe_active.id_campus
            cycle_id = classe_active.cycle_id

    # =======================
    # Élèves
    # =======================
    eleves = Eleve_inscription.objects.filter(id_annee_id=annee, status=True)
    if classe_active:
        eleves = eleves.filter(
            id_classe_id=classe_active.id_classe_active,
            id_campus_id=campus_id,
            id_classe_cycle_id=cycle_id
        )
    if eleve_id and eleve_id.isdigit():
        eleves = eleves.filter(id_eleve_id=int(eleve_id))

    # =======================
    # Variables
    # =======================
    variables_prix = VariablePrix.objects.filter(id_annee_id=annee)
    if classe_active:
        variables_prix = variables_prix.filter(id_classe_active=classe_active.id_classe_active)
    if variable_id and variable_id.isdigit():
        variables_prix = variables_prix.filter(id_variable_id=int(variable_id))
    if trimestre_id and trimestre_id.isdigit():
        variables_prix = variables_prix.filter(id_annee_trimestre_id=int(trimestre_id))

    def get_classe_nom(obj):
        c = obj.id_classe_active
        return f"{c.id_campus.campus} - {c.cycle_id.cycle_id.cycle} - {c.classe_id.classe} {c.groupe or ''}"

    # =======================
    # Construction des stats
    # =======================
    if type_stat == "dette":
        title = "Élèves en dette"
        for vp in variables_prix:
            prix = vp.prix
            for e in eleves:
                reduction = Eleve_reduction_prix.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee
                ).first()
                attendu = prix
                if reduction:
                    attendu -= (prix * reduction.pourcentage)/100
                total_paye = Paiement.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee,
                    status=True,
                    is_rejected=False
                ).aggregate(total=Sum('montant'))['total'] or 0
                reste = attendu - total_paye
                if reste > 0:
                    rows.append({
                        "classe": get_classe_nom(vp),
                        "nom": f"{e.id_eleve.nom} {e.id_eleve.prenom}",
                        "variable": vp.id_variable.variable,
                        "total": reste
                    })

    elif type_stat == "reste":
        title = "Reste à payer par variable"
        for vp in variables_prix:
            reste_global = 0
            prix = vp.prix
            for e in eleves:
                reduction = Eleve_reduction_prix.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee
                ).first()
                attendu = prix
                if reduction:
                    attendu -= (prix * reduction.pourcentage)/100
                total_paye = Paiement.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee,
                    status=True,
                    is_rejected=False
                ).aggregate(total=Sum('montant'))['total'] or 0
                reste_global += max(attendu - total_paye, 0)
            rows.append({
                "classe": get_classe_nom(vp),
                "variable": vp.id_variable.variable,
                "total": reste_global
            })

    elif type_stat == "transactions":
        title = "Nombre de paiements par variable"
        for vp in variables_prix:
            qs = Paiement.objects.filter(
                id_variable_id=vp.id_variable_id,
                id_annee_id=annee,
                status=True,
                is_rejected=False
            )
            if classe_active:
                qs = qs.filter(id_classe_active_id=classe_active.id_classe_active)
            rows.append({
                "classe": get_classe_nom(vp),
                "variable": vp.id_variable.variable,
                "total": qs.count()
            })

    elif type_stat == "paye":
        title = "Montants payés"
        for vp in variables_prix:
            for e in eleves:
                paiements_qs = Paiement.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee,
                    status=True,
                    is_rejected=False
                )
                if classe_active:
                    paiements_qs = paiements_qs.filter(id_classe_active_id=classe_active.id_classe_active)
                total_montant = paiements_qs.aggregate(total=Sum('montant'))['total'] or 0
                if total_montant > 0:
                    rows.append({
                        "classe": get_classe_nom(vp),
                        "nom": f"{e.id_eleve.nom} {e.id_eleve.prenom}",
                        "variable": vp.id_variable.variable,
                        "total": total_montant
                    })

    elif type_stat == "attendu":
        title = "Montant attendu par variable"
        for vp in variables_prix:
            total_attendu = 0
            prix = vp.prix
            for e in eleves:
                reduction = Eleve_reduction_prix.objects.filter(
                    id_variable_id=vp.id_variable_id,
                    id_eleve_id=e.id_eleve_id,
                    id_annee_id=annee
                ).first()
                if reduction:
                    total_attendu += prix - (prix * reduction.pourcentage)/100
                else:
                    total_attendu += prix
            rows.append({
                "classe": get_classe_nom(vp),
                "variable": vp.id_variable.variable,
                "total": total_attendu
            })

    elif type_stat == "rejet":
        title = "Paiements rejetés"
        for vp in variables_prix:
            qs = Paiement.objects.filter(
                id_variable_id=vp.id_variable_id,
                id_annee_id=annee,
                is_rejected=True
            )
            if classe_active:
                qs = qs.filter(id_classe_active_id=classe_active.id_classe_active)
            rows.append({
                "classe": get_classe_nom(vp),
                "variable": vp.id_variable.variable,
                "total": qs.count()
            })

    return JsonResponse({
        'success': True,
        'title': title,
        'rows': rows
    })
