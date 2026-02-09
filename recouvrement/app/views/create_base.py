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



def dashboard_data(request):
    annee = request.GET.get('annee')
    classe = request.GET.get('classe')
    eleve = request.GET.get('eleve')
    trimestre = request.GET.get('trimestre')
    variable = request.GET.get('variable')

    if not annee:
        return JsonResponse({'success': False})

    # 🔵 BASE QUERY PAIEMENTS
    paiements = Paiement.objects.filter(id_annee_id=annee, status=True)

    if classe and classe.isdigit():
        paiements = paiements.filter(id_classe_active_id=int(classe))
    if eleve and eleve.isdigit():
        paiements = paiements.filter(id_eleve_id=int(eleve))
    if variable and variable.isdigit():
        paiements = paiements.filter(id_variable_id=int(variable))

    # 🔵 STATS DE BASE
    total_paye = paiements.aggregate(total=Sum('montant'))['total'] or 0
    total_transactions = paiements.count()

    # 🔵 CONTEXTE CLASSE
    classe_active = None
    campus = None
    cycle = None
    if classe and classe.isdigit():
        classe_active = Classe_active.objects.filter(id_classe_active=int(classe)) \
            .select_related('id_campus', 'cycle_id').first()
        if classe_active:
            campus = classe_active.id_campus_id
            cycle = classe_active.cycle_id_id

    # 🔵 ÉLÈVES INSCRITS
    eleves_inscrits = Eleve_inscription.objects.filter(id_annee_id=annee, status=1)
    if classe_active:
        eleves_inscrits = eleves_inscrits.filter(
            id_classe_id=int(classe),
            id_campus_id=campus,
            id_classe_cycle_id=cycle
        )
    eleves_inscrits = list(eleves_inscrits.values_list('id_eleve_id', flat=True))

    # 🔥 CALCUL TOTAL ATTENDU
    total_attendu = 0
    variables_prix = VariablePrix.objects.filter(id_annee_id=annee)
    if classe_active:
        variables_prix = variables_prix.filter(
            id_classe_active_id=int(classe),
            id_campus_id=campus,
            id_cycle_actif_id=cycle
        )
    if variable and variable.isdigit():
        variables_prix = variables_prix.filter(id_variable=int(variable))

    if eleve and eleve.isdigit():
        # CAS ÉLÈVE SPÉCIFIQUE
        for vp in variables_prix:
            prix_normal = vp.prix
            reduction = Eleve_reduction_prix.objects.filter(
                id_variable_id=vp.id_variable_id,
                id_eleve_id=int(eleve),
                id_annee_id=annee,
                id_classe_active_id=int(classe) if classe and classe.isdigit() else None,
                id_campus_id=campus,
                id_cycle_actif_id=cycle
            ).first()
            montant_final = prix_normal
            if reduction:
                montant_final -= (prix_normal * reduction.pourcentage) / 100
            total_attendu += montant_final
    else:
        # CAS CLASSE OU ANNÉE ENTIÈRE
        for vp in variables_prix:
            prix_normal = vp.prix
            variable_id = vp.id_variable_id

            reductions = Eleve_reduction_prix.objects.filter(
                id_variable_id=variable_id,
                id_annee_id=annee,
                id_classe_active_id=int(classe) if classe and classe.isdigit() else None,
                id_campus_id=campus,
                id_cycle_actif_id=cycle,
                id_eleve_id__in=eleves_inscrits
            )

            nb_reduction = reductions.count()
            nb_total_eleves = len(eleves_inscrits)
            nb_sans_reduction = nb_total_eleves - nb_reduction

            total_sans_reduction = prix_normal * nb_sans_reduction
            total_avec_reduction = sum(
                prix_normal - (prix_normal * red.pourcentage / 100) for red in reductions
            )
            total_attendu += total_sans_reduction + total_avec_reduction

    # 🔵 RESTE A PAYER
    reste_a_payer = total_attendu - total_paye

    # 🔵 BANQUES
    banques = paiements.values('id_banque__banque').annotate(total=Sum('montant'))

    # 🔵 VARIABLES POUR GRAPH
    variables_data = paiements.values('id_variable__variable').annotate(total=Sum('montant'))

    return JsonResponse({
        'success': True,
        'stats': {
            'total_transactions': total_transactions,
            'total_paye': total_paye,
            'total_attendu': total_attendu,
            'reste_a_payer': reste_a_payer,
            'eleves_en_dette': 0,
            'total_rejete': 0
        },
        'banques': list(banques),
        'variables': list(variables_data),
    })
