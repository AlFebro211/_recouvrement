from .create_base import *
from datetime import datetime, date
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

            # Interdire les dates inférieures à aujourd'hui
            if date_derogation < date.today():
                return JsonResponse({
                    'success': False,
                    'error': f"La date de dérogation ({date_derogation}) ne peut pas être inférieure à la date du jour ({date.today()})."
                }, status=400)

            # Récupérer la date butoire officielle (optionnel)
            variable_date_butoire = VariableDatebutoire.objects.filter(
                id_variable_id=id_variable,
                id_annee_id=id_annee,
                id_campus_id=id_campus,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active
            ).first()

            # Vérification de la règle métier (seulement si date butoire existe)
            if variable_date_butoire and date_derogation < variable_date_butoire.date_butoire:
                return JsonResponse({
                    'success': False,
                    'error': (
                        f"La date de dérogation ({date_derogation}) "
                        f"ne peut pas être inférieure à la date butoire "
                        f"({variable_date_butoire.date_butoire})."
                    )
                })

            # update_or_create : si existe déjà, on met à jour la date
            obj, created = VariableDerogation.objects.update_or_create(
                id_eleve_id=id_eleve,
                id_annee_id=id_annee,
                id_classe_active_id=id_classe_active,
                id_variable_id=id_variable,
                defaults={
                    'id_campus_id': id_campus,
                    'id_cycle_actif_id': id_cycle_actif,
                    'date_derogation': date_butoire,
                }
            )

            msg = 'Dérogation mise à jour avec succès !' if not created else 'Dérogation enregistrée avec succès !'
            return JsonResponse({'success': True, 'message': msg, 'updated': not created})
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

            # Interdire les dates inférieures à aujourd'hui
            date_butoire_parsed = datetime.strptime(date_butoire, '%Y-%m-%d').date()
            if date_butoire_parsed < date.today():
                return JsonResponse({
                    'success': False,
                    'error': f"La date butoire ({date_butoire_parsed}) ne peut pas être inférieure à la date du jour ({date.today()})."
                }, status=400)

            # update_or_create : si existe déjà, on met à jour la date
            obj, created = VariableDatebutoire.objects.update_or_create(
                id_annee_id=id_annee,
                id_classe_active_id=id_classe_active,
                id_variable_id=id_variable,
                defaults={
                    'id_campus_id': id_campus,
                    'id_cycle_actif_id': id_cycle_actif,
                    'date_butoire': date_butoire,
                }
            )

            msg = 'Date butoire mise à jour avec succès !' if not created else 'Date butoire enregistrée avec succès !'
            return JsonResponse({'success': True, 'message': msg, 'updated': not created})
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
    

            if not all([id_annee, id_campus, id_cycle_actif, id_classe_active, id_eleve, pourcentage]):
                return JsonResponse({
                    'success': False,
                    'error': 'Tous les champs sont requis.'
                }, status=400)

            # update_or_create : si existe déjà, on met à jour le pourcentage
            obj, created = Eleve_reduction_prix.objects.update_or_create(
                id_eleve_id=id_eleve,
                id_annee_id=id_annee,
                id_classe_active_id=id_classe_active,
                id_variable_id=id_variable,
                defaults={
                    'id_campus_id': id_campus,
                    'id_cycle_actif_id': id_cycle_actif,
                    'pourcentage': pourcentage,
                }
            )

            msg = 'Réduction mise à jour avec succès !' if not created else 'Réduction enregistrée avec succès !'
            return JsonResponse({'success': True, 'message': msg, 'updated': not created})
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


@csrf_protect
def save_categorie_operation(request):
    """
    Vue pour enregistrer une catégorie d'opération via AJAX
    Similaire à save_penalite
    """
    if request.method == "POST":
        try:
            # Récupération des données du formulaire
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            type_operation = request.POST.get('type_operation')
            nom = request.POST.get('nom')
            description = request.POST.get('description', '')

            # Logging pour débogage
            logger.info(f"Tentative de création catégorie - Année: {id_annee}, Campus: {id_campus}, Type: {type_operation}, Nom: {nom}")

            # Validation des champs obligatoires
            if not all([id_annee, id_campus, type_operation, nom]):
                missing_fields = []
                if not id_annee: missing_fields.append("Année")
                if not id_campus: missing_fields.append("Campus")
                if not type_operation: missing_fields.append("Type d'opération")
                if not nom: missing_fields.append("Nom")
                
                return JsonResponse({
                    'success': False, 
                    'error': f'Champs obligatoires manquants : {", ".join(missing_fields)}'
                }, status=400)

            # Validation du type d'opération
            if type_operation not in ['ENTREE', 'SORTIE']:
                return JsonResponse({
                    'success': False, 
                    'error': 'Le type d\'opération doit être "ENTREE" ou "SORTIE".'
                }, status=400)

            # Récupération et validation de l'année
            try:
                annee_obj = Annee.objects.get(id_annee=id_annee)
            except Annee.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'error': f'Année avec ID {id_annee} introuvable.'
                }, status=400)

            # Récupération et validation du campus
            try:
                campus_obj = Campus.objects.get(id_campus=id_campus)
            except Campus.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'error': f'Campus avec ID {id_campus} introuvable.'
                }, status=400)

            # Vérification de l'unicité (type + nom) pour cette année et ce campus
            existing_categorie = CategorieOperation.objects.filter(
                id_annee=annee_obj,
                id_campus=campus_obj,
                type_operation=type_operation,
                nom__iexact=nom  # Case-insensitive
            ).first()
            
            if existing_categorie:
                return JsonResponse({
                    'success': False,
                    'error': f'Une catégorie "{nom}" de type {type_operation} existe déjà pour {annee_obj.annee} - {campus_obj.campus}.'
                }, status=400)

            # Création de la catégorie
            categorie = CategorieOperation(
                id_annee=annee_obj,
                id_campus=campus_obj,
                type_operation=type_operation,
                nom=nom,
                description=description,
                est_active=True
            )
            
            # Sauvegarde
            categorie.save()
            
            # Logging de succès
            logger.info(f"Catégorie créée avec succès: {categorie.nom} (ID: {categorie.id_categorie})")

            # Préparation de la réponse
            response_data = {
                'success': True,
                'message': f'Catégorie "{nom}" créée avec succès.',
                'data': {
                    'id': categorie.id_categorie,
                    'nom': categorie.nom,
                    'type_operation': categorie.type_operation,
                    'description': categorie.description,
                    'est_active': categorie.est_active,
                    'annee': {
                        'id': annee_obj.id_annee,
                        'nom': annee_obj.annee
                    },
                    'campus': {
                        'id': campus_obj.id_campus,
                        'nom': campus_obj.campus
                    },
                    'date_creation': categorie.date_creation.strftime('%d/%m/%Y %H:%M') if categorie.date_creation else None
                }
            }
            
            return JsonResponse(response_data, status=201)

        except Exception as e:
            logger.error(f"Erreur lors de la création de la catégorie: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue lors de l\'enregistrement : {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée. Utilisez POST.'
    }, status=405)


def get_annees_actives(request):
    """Retourne la liste des années actives"""
    try:
        annees = Annee.objects.filter(is_active=True).values('id_annee', 'annee').order_by('-annee')
        return JsonResponse({
            'success': True,
            'annees': list(annees)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_campus_actifs(request):
    """Retourne la liste des campus actifs"""
    try:
        campus = Campus.objects.filter(is_active=True).values('id_campus', 'campus').order_by('campus')
        return JsonResponse({
            'success': True,
            'campus': list(campus)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_categories_filtrees(request):
    """Retourne les catégories filtrées par année et campus"""
    try:
        annee = request.GET.get('annee')
        campus = request.GET.get('campus')
        
        categories = CategorieOperation.objects.filter(est_active=True)
        
        if annee:
            categories = categories.filter(id_annee_id=annee)
        if campus:
            categories = categories.filter(id_campus_id=campus)
        
        categories = categories.select_related('id_annee', 'id_campus').order_by('-date_creation')
        
        data = []
        for cat in categories:
            data.append({
                'id': cat.id_categorie,
                'nom': cat.nom,
                'type_operation': cat.type_operation,
                'description': cat.description,
                'annee': cat.id_annee.annee if cat.id_annee else '',
                'campus': cat.id_campus.campus if cat.id_campus else '',
                'date_creation': cat.date_creation.strftime('%d/%m/%Y') if cat.date_creation else ''
            })
        
        return JsonResponse({
            'success': True,
            'categories': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_protect
def get_categories_operations(request):
    """Retourne la liste des catégories d'opérations"""
    try:
        # Récupération des paramètres de filtrage
        annee_id = request.GET.get('annee')
        campus_id = request.GET.get('campus')
        type_operation = request.GET.get('type')  # ENTREE ou SORTIE
        
        # Construction de la requête
        categories = CategorieOperation.objects.filter(est_active=True)
        
        if annee_id:
            categories = categories.filter(id_annee_id=annee_id)
        if campus_id:
            categories = categories.filter(id_campus_id=campus_id)
        if type_operation:
            categories = categories.filter(type_operation=type_operation)
        
        # Tri par date de création (plus récent d'abord)
        categories = categories.select_related('id_annee', 'id_campus').order_by('-date_creation')
        
        # Formatage des données
        data = []
        for cat in categories:
            data.append({
                'id': cat.id_categorie,
                'nom': cat.nom,
                'type_operation': cat.type_operation,
                'description': cat.description or '',
                'est_active': cat.est_active,
                'annee': cat.id_annee.annee if cat.id_annee else '',
                'annee_id': cat.id_annee.id_annee if cat.id_annee else '',
                'campus': cat.id_campus.campus if cat.id_campus else '',
                'campus_id': cat.id_campus.id_campus if cat.id_campus else '',
                'date_creation': cat.date_creation.strftime('%d/%m/%Y %H:%M') if cat.date_creation else '',
                'date_creation_raw': cat.date_creation.isoformat() if cat.date_creation else ''
            })
        
        # Calcul des statistiques
        stats = {
            'total': len(data),
            'entrees': sum(1 for cat in data if cat['type_operation'] == 'ENTREE'),
            'sorties': sum(1 for cat in data if cat['type_operation'] == 'SORTIE')
        }
        
        return JsonResponse({
            'success': True,
            'categories': data,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erreur dans get_categories_operations: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def liste_operations(request):
    """Affiche la liste des opérations financières"""
    form = OperationCaisseForm()
    annees = Annee.objects.filter(is_active=True)
    campus_list = Campus.objects.filter(is_active=True)
    
    return render(request, 'recouvrement/index_recouvrement.html', {
        'liste_operations_form': form,
        'form_type': 'liste_operations_form',
        'annees': annees,
        'campus_list': campus_list,
    })

@csrf_protect
def save_operation_caisse(request):
    if request.method == "POST":
        try:
            # Récupération des données
            id_annee = request.POST.get('id_annee')
            id_campus = request.POST.get('id_campus')
            categorie = request.POST.get('categorie')
            montant = request.POST.get('montant')
            date_operation = request.POST.get('date_operation')  # C'est une string au format 'YYYY-MM-DD'
            description = request.POST.get('description', '')
            source_beneficiaire = request.POST.get('source_beneficiaire', '')
            mode_paiement = request.POST.get('mode_paiement')
            reference = request.POST.get('reference', '')
            justificatif = request.FILES.get('justificatif')

            logger.info(f"Tentative de création opération - Année: {id_annee}, Campus: {id_campus}, Catégorie: {categorie}, Montant: {montant}")

            # Validation des champs obligatoires
            if not all([id_annee, id_campus, categorie, montant, date_operation, mode_paiement]):
                missing_fields = []
                if not id_annee: missing_fields.append("Année")
                if not id_campus: missing_fields.append("Campus")
                if not categorie: missing_fields.append("Catégorie")
                if not montant: missing_fields.append("Montant")
                if not date_operation: missing_fields.append("Date")
                if not mode_paiement: missing_fields.append("Mode de paiement")
                
                return JsonResponse({
                    'success': False, 
                    'error': f'Champs obligatoires manquants : {", ".join(missing_fields)}'
                }, status=400)

            # Récupération des objets
            try:
                annee_obj = Annee.objects.get(id_annee=id_annee)
            except Annee.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Année introuvable'}, status=400)

            try:
                campus_obj = Campus.objects.get(id_campus=id_campus)
            except Campus.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Campus introuvable'}, status=400)

            try:
                categorie_obj = CategorieOperation.objects.get(id_categorie=categorie, est_active=True)
            except CategorieOperation.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Catégorie introuvable'}, status=400)

            # Validation du montant
            try:
                montant = float(montant)
                if montant <= 0:
                    return JsonResponse({'success': False, 'error': 'Le montant doit être positif'}, status=400)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Montant invalide'}, status=400)

            # Convertir la date string en objet date
            from datetime import datetime
            try:
                date_obj = datetime.strptime(date_operation, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Format de date invalide'}, status=400)

            # Création de l'opération avec l'objet date
            operation = OperationCaisse(
                id_annee=annee_obj,
                id_campus=campus_obj,
                categorie=categorie_obj,
                montant=montant,
                date_operation=date_obj,  # Utiliser l'objet date, pas la string
                description=description,
                source_beneficiaire=source_beneficiaire,
                mode_paiement=mode_paiement,
                reference=reference,
                justificatif=justificatif,
            )
            
            operation.save()
            
            logger.info(f"Opération créée avec succès: ID {operation.id_operation}, Montant: {montant}")

            return JsonResponse({
                'success': True,
                'message': 'Opération enregistrée avec succès',
                'data': {
                    'id': operation.id_operation,
                    'montant': str(operation.montant),
                    'date_operation': operation.date_operation.strftime('%d/%m/%Y'),  # Maintenant c'est un objet date
                    'type_operation': categorie_obj.type_operation,
                }
            }, status=201)

        except Exception as e:
            logger.error(f"Erreur lors de la création de l'opération: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue : {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée'
    }, status=405)
@csrf_protect
def get_operations_caisse(request):
    """Retourne la liste des opérations de caisse filtrées"""
    try:
        annee_id = request.GET.get('annee')
        campus_id = request.GET.get('campus')
        categorie_id = request.GET.get('categorie')
        type_operation = request.GET.get('type')
        
        operations = OperationCaisse.objects.all().select_related(
            'id_annee', 'id_campus', 'categorie'
        ).order_by('-date_operation', '-id_operation')
        
        if annee_id:
            operations = operations.filter(id_annee_id=annee_id)
        if campus_id:
            operations = operations.filter(id_campus_id=campus_id)
        if categorie_id:
            operations = operations.filter(categorie_id=categorie_id)
        if type_operation:
            operations = operations.filter(categorie__type_operation=type_operation)
        
        data = []
        total_montant = 0
        total_entrees = 0
        total_sorties = 0
        
        for op in operations:
            montant = float(op.montant)
            total_montant += montant
            if op.categorie.type_operation == 'ENTREE':
                total_entrees += montant
            else:
                total_sorties += montant
                
            # Formater la date de création si elle existe
            date_creation_formatted = ''
            if hasattr(op, 'date_creation') and op.date_creation:
                date_creation_formatted = op.date_creation.strftime('%d/%m/%Y %H:%M')
                
            data.append({
                'id': op.id_operation,
                'date': op.date_operation.strftime('%d/%m/%Y'),  # date_operation est un objet date
                'date_raw': op.date_operation.isoformat(),
                'categorie': op.categorie.nom if op.categorie else '',
                'categorie_id': op.categorie.id_categorie if op.categorie else '',
                'type_operation': op.categorie.type_operation if op.categorie else '',
                'montant': montant,
                'montant_formatted': f"{montant:,.0f}".replace(',', ' '),
                'source_beneficiaire': op.source_beneficiaire or '-',
                'mode_paiement': op.get_mode_paiement_display() if op.mode_paiement else '-',
                'description': op.description or '-',
                'reference': op.reference or '-',
                'annee': op.id_annee.annee if op.id_annee else '',
                'campus': op.id_campus.campus if op.id_campus else '',
                'justificatif': op.justificatif.url if op.justificatif else None,
                'date_creation': date_creation_formatted,
            })
        
        stats = {
            'total': len(data),
            'montant_total': total_montant,
            'entrees': total_entrees,
            'sorties': total_sorties,
        }
        
        return JsonResponse({
            'success': True,
            'operations': data,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erreur dans get_operations_caisse: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_protect
def get_categories_by_filters(request):
    """Retourne les catégories filtrées par année et campus"""
    try:
        annee_id = request.GET.get('annee')
        campus_id = request.GET.get('campus')
        
        categories = CategorieOperation.objects.filter(est_active=True)
        
        if annee_id:
            categories = categories.filter(id_annee_id=annee_id)
        if campus_id:
            categories = categories.filter(id_campus_id=campus_id)
        
        data = [{
            'id': cat.id_categorie,
            'nom': cat.nom,
            'type_operation': cat.type_operation
        } for cat in categories.order_by('nom')]
        
        return JsonResponse({
            'success': True,
            'categories': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_protect
def delete_operation(request, id_operation):
    """Supprimer (désactiver) une opération"""
    if request.method == 'POST':
        try:
            operation = OperationCaisse.objects.get(id_operation=id_operation)
            operation.est_active = False
            operation.save()
            return JsonResponse({'success': True})
        except OperationCaisse.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Opération non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)