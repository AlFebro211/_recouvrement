from .create_base import *
from datetime import datetime
from app.models import *

@csrf_protect
def save_variable_prix(request):
    if request.method == 'POST':
        try:

            id_campus = request.POST.get('id_campus')
            id_cycle_actif = request.POST.get('id_cycle_actif')  #
            if not id_campus or not id_cycle_actif:
                return JsonResponse({
                    'success': False,
                    'error': "Champs obligatoires manquants : id_campus ou id_cycle_actif."
                }, status=400)

            try:
                id_campus = int(id_campus)
                id_cycle_actif = int(id_cycle_actif)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'error': "id_campus et id_cycle_actif doivent être des entiers."
                }, status=400)

            form = VariablePrixForm(request.POST)
            if not form.is_valid():
                errors = form.errors.as_json()
                return JsonResponse({
                    'success': False,
                    'error': 'Erreurs de validation du formulaire.',
                    'details': errors
                }, status=400)

            id_annee = form.cleaned_data['id_annee']
            id_classe_active = form.cleaned_data['id_classe_active']
            id_variable = form.cleaned_data['id_variable']
            id_annee_trimestre = form.cleaned_data['id_annee_trimestre']
            prix = form.cleaned_data['prix']

            if VariablePrix.objects.filter(
                id_annee=id_annee,
                id_classe_active=id_classe_active,
                id_variable=id_variable,
                id_annee_trimestre=id_annee_trimestre
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': "Cette combinaison d'année, classe et variable existe déjà."
                }, status=400)

            try:
                classe_active = Classe_active.objects.get(pk=id_classe_active.pk)
                if classe_active.id_campus_id != id_campus or classe_active.cycle_id_id != id_cycle_actif:
                    return JsonResponse({
                        'success': False,
                        'error': "Les valeurs de campus ou cycle ne correspondent pas à la classe sélectionnée."
                    }, status=400)
            except Classe_active.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': "Classe active introuvable."
                }, status=400)

            # Enregistrer
            variable_prix = form.save(commit=False)
            variable_prix.id_campus_id = id_campus
            variable_prix.id_cycle_actif_id = id_cycle_actif
            variable_prix.save()
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f"Une erreur est survenue lors de l'enregistrement : {str(e)}"
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': "Méthode non autorisée."
    }, status=405)


@csrf_protect
def save_variable_derogation(request):
    if request.method == 'POST':
        try:
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            id_cycle_actif = request.POST.get('id_cycle_actif')
            id_classe_active = request.POST.get('id_classe_active')
            id_eleve = request.POST.get('id_eleve')
            id_variable = request.POST.get('id_variable')
            date_butoire = request.POST.get('date_butoire')
    

            if not all([id_annee, id_campus, id_cycle_actif, id_classe_active, id_eleve, date_butoire]):
                return JsonResponse({
                    'success': False,
                    'error': 'Tous les champs sont requis.'
                }, status=400)
            
            date_derogation = datetime.strptime(date_butoire, '%Y-%m-%d').date()

            # 🔍 récupérer la date butoire officielle
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
                    'error': "Aucune date butoire définie pour cette variable dans cette classe."
                }, status=400)

            # ❌ Vérification de la règle métier
            if date_derogation < variable_date_butoire.date_butoire:
                return JsonResponse({
                    'success': False,
                    'error': (
                        f"La date de dérogation ({date_derogation}) "
                        f"ne peut pas être inférieure à la date butoire "
                        f"({variable_date_butoire.date_butoire})."
                    )
                })


            if VariableDerogation.objects.filter(
                id_eleve=id_eleve,
                id_annee = id_annee,
                id_classe_active=id_classe_active,
                id_variable = id_variable,
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Cette derogation existe déjà.'
                }, status=400)

            derogation = VariableDerogation(
                id_eleve_id=id_eleve,
                id_campus_id=id_campus,
                id_annee_id=id_annee,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active,
                date_derogation=date_butoire,
                id_variable_id= id_variable
            )
            derogation.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée.'
    }, status=405)


@csrf_protect
def save_variable_date_butoire(request):
    if request.method == 'POST':
        try:
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            id_cycle_actif = request.POST.get('id_cycle_actif')
            id_classe_active = request.POST.get('id_classe_active')
            id_variable = request.POST.get('id_variable')
            date_butoire = request.POST.get('date_butoire')
        
            if not all([id_annee, id_campus, id_cycle_actif, id_classe_active, date_butoire]):
                return JsonResponse({
                    'success': False,
                    'error': 'Tous les champs sont requis.'
                }, status=400)

            if VariableDatebutoire.objects.filter(
                id_annee = id_annee,
                id_classe_active=id_classe_active,
                id_variable= id_variable,
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Cette date butoire  existe déjà.'
                }, status=400)

            derogation = VariableDatebutoire(
                id_campus_id=id_campus,
                id_annee_id=id_annee,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active,
                date_butoire=date_butoire,
                id_variable_id=id_variable
                
            )
            derogation.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée.'
    }, status=405)




@csrf_protect
def save_variable_reduction(request):
    if request.method == 'POST':
        try:
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            id_cycle_actif = request.POST.get('id_cycle_actif')
            id_classe_active = request.POST.get('id_classe_active')
            id_eleve = request.POST.get('id_eleve')
            id_variable = request.POST.get('id_variable')
            pourcentage = request.POST.get('pourcentage')
    

            if not all([id_annee, id_campus, id_cycle_actif, id_classe_active, id_eleve,pourcentage]):
                return JsonResponse({
                    'success': False,
                    'error': 'Tous les champs sont requis.'
                }, status=400)

            if Eleve_reduction_prix.objects.filter(
                id_eleve=id_eleve,
                id_annee = id_annee,
                id_classe_active=id_classe_active,
                id_variable=id_variable
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Cette reduction existe déjà pour le même élève.'
                }, status=400)

            reduction = Eleve_reduction_prix(
                id_eleve_id=id_eleve,
                id_campus_id=id_campus,
                id_annee_id=id_annee,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active,
                pourcentage=pourcentage,
                id_variable_id= id_variable
            )
            reduction.save()

            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f"Erreur dans save_variable_reduction: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée.'
    }, status=405)
    

@csrf_protect
def save_penalite(request):
    if request.method == "POST":
        try:
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            id_cycle_actif = request.POST.get('id_cycle_actif')
            id_classe_active = request.POST.get('id_classe_active')
            id_variable = request.POST.get('id_variable')
            id_annee_trimestre = request.POST.get('id_annee_trimestre')
            type_penalite = request.POST.get('type_penalite')
            valeur = request.POST.get('valeur')
            plafond = request.POST.get('plafond')

            if not all([id_annee, type_penalite, valeur]):
                return JsonResponse({'success': False, 'error': 'Tous les champs obligatoires doivent être remplis.'}, status=400)

            try:
                annee_obj = Annee.objects.get(id_annee=id_annee)
            except Annee.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Année invalide.'}, status=400)

            campus_obj = None
            if id_campus:
                try:
                    campus_obj = Campus.objects.get(id_campus=id_campus)
                except Campus.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Campus invalide.'}, status=400)

            cycle_obj = None
            if id_cycle_actif:
                try:
                    cycle_obj = Classe_cycle_actif.objects.get(id_cycle_actif=id_cycle_actif)
                except Classe_cycle_actif.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Cycle invalide.'}, status=400)

            classe_obj = None
            if id_classe_active:
                try:
                    classe_obj = Classe_active.objects.get(id_classe_active=id_classe_active)
                except Classe_active.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Classe invalide.'}, status=400)

            variable_obj = None
            if id_variable:
                try:
                    variable_obj = Variable.objects.get(id_variable=id_variable)
                except Variable.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Variable invalide.'}, status=400)

            trimestre_obj = None
            if id_annee_trimestre:
                try:
                    trimestre_obj = Annee_trimestre.objects.get(id_trimestre=id_annee_trimestre)
                except Annee_trimestre.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Trimestre invalide.'}, status=400)

            penalite = PenaliteConfig(
                id_annee=annee_obj,
                id_campus=campus_obj,
                id_cycle_actif=cycle_obj,
                id_classe_active=classe_obj,
                id_variable=variable_obj,
                id_annee_trimestre=trimestre_obj,
                type_penalite=type_penalite,
                valeur=valeur,
                plafond=plafond if plafond else None
            )
            penalite.save()

            return JsonResponse({'success': True, 'message': 'Pénalité créée avec succès.'}, status=201)

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)


def delete_paiement(request, id_paiement):
    if request.method == "POST":
        try:
            paiement = Paiement.objects.get(id_paiement=id_paiement)
            paiement.status = False  # on ne supprime pas, on désactive
            paiement.save()
            return JsonResponse({'success': True})
        except Paiement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paiement non trouvé'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


