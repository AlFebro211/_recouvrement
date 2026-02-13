
import json
from .create_base import *
from django.views.decorators.http import require_POST




@login_required
@csrf_protect
def update_paiement_field(request):
    if request.method == 'POST':
        try:
            id_paiement = request.POST.get('id_paiement')
            field = request.POST.get('field')
            value = request.POST.get('value') == 'true'  

            if not id_paiement or not field:
                return JsonResponse({
                    'success': False,
                    'error': 'ID de paiement ou champ manquant.'
                }, status=400)

            if field not in ['status', 'is_rejected']:
                return JsonResponse({
                    'success': False,
                    'error': 'Champ non valide.'
                }, status=400)

            try:
                paiement = Paiement.objects.get(id_paiement=id_paiement)
            except Paiement.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Paiement non trouvé.'
                }, status=404)

            if field == 'status':
                paiement.status = value
            elif field == 'is_rejected':
                paiement.is_rejected = value

            paiement.save()

            logger.info(f"Paiement mis à jour: id={id_paiement}, {field}={value}")

            return JsonResponse({'success': True})

        except Exception as e:
            logger.error(f"Erreur dans update_paiement_field pour id_paiement={id_paiement}, field={field}: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Une erreur est survenue : {str(e)}'
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Méthode non autorisée.'
    }, status=405)


@login_required
@csrf_protect
def update_categorie(request, categorie_id):
    if request.method == 'POST':
        try:
            categorie = get_object_or_404(VariableCategorie, id_variable_categorie=categorie_id)
            new_name = request.POST.get('nom')
            if not new_name:
                return JsonResponse({'success': False, 'error': 'Le nom ne peut pas être vide.'})
            categorie.nom = new_name
            categorie.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})


@login_required
@csrf_protect
def update_compte(request, compte_id):
    if request.method == 'POST':
        try:
            compte = get_object_or_404(Compte, id_compte=compte_id)
            new_compte = request.POST.get('compte')
            banque_id = request.POST.get('banque_id')

            if not new_compte or not banque_id:
                return JsonResponse({'success': False, 'error': 'Les champs ne peuvent pas être vides.'})

            banque = get_object_or_404(Banque, id_banque=banque_id)

            if Compte.objects.filter(
                id_banque=banque,
                compte=new_compte
            ).exclude(id_compte=compte_id).exists():
                return JsonResponse({'success': False, 'error': 'Un compte avec ce numéro existe déjà pour cette banque.'})

            compte.compte = new_compte
            compte.id_banque = banque
            compte.save()

            return JsonResponse({
                'success': True,
                'banque_nom': banque.banque
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})

@login_required
@csrf_protect
def update_banque(request, banque_id):
    if request.method == 'POST':
        try:
            banque = get_object_or_404(Banque, id_banque=banque_id)
            new_banque = request.POST.get('banque')
            new_sigle = request.POST.get('sigle')

            if not new_banque or not new_sigle:
                return JsonResponse({'success': False, 'error': 'Les champs ne peuvent pas être vides.'})

            if Banque.objects.filter(banque=new_banque).exclude(id_banque=banque_id).exists():
                return JsonResponse({'success': False, 'error': 'Une banque avec ce nom existe déjà.'})
            if Banque.objects.filter(sigle=new_sigle).exclude(id_banque=banque_id).exists():
                return JsonResponse({'success': False, 'error': 'Un sigle identique existe déjà.'})

            banque.banque = new_banque
            banque.sigle = new_sigle
            banque.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})

@login_required
@csrf_protect
def update_variable(request, variable_id):
    if request.method == 'POST':
        try:
            variable = get_object_or_404(Variable, id_variable=variable_id)
            categorie_id = request.POST.get('categorie_id')
            new_variable = request.POST.get('variable')

            if not categorie_id or not new_variable:
                return JsonResponse({'success': False, 'error': 'Les champs ne peuvent pas être vides.'})

            categorie = get_object_or_404(VariableCategorie, id_variable_categorie=categorie_id)

            if Variable.objects.filter(
                id_variable_categorie=categorie,
                variable=new_variable
            ).exclude(id_variable=variable_id).exists():
                return JsonResponse({'success': False, 'error': 'Une variable avec ce nom existe déjà dans cette catégorie.'})

            variable.id_variable_categorie = categorie
            variable.variable = new_variable
            variable.save()

            return JsonResponse({
                'success': True,
                'categorie_nom': categorie.nom
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})


@csrf_protect
def update_paiement(request, id_paiement):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)

    try:

        paiement = get_object_or_404(Paiement, id_paiement=id_paiement)

        montant = request.POST.get('montant')
        date_paie = request.POST.get('date_paie')
        bordereau = request.FILES.get('bordereau')

        if not montant:
            return JsonResponse({'success': False, 'error': 'Montant obligatoire.'})

        montant = int(montant)

        # ========================== RECUPERATION CONTEXTE ==========================
        id_variable = paiement.id_variable_id
        id_eleve = paiement.id_eleve_id
        id_annee = paiement.id_annee_id
        id_campus = paiement.id_campus_id
        id_cycle_actif = paiement.id_cycle_actif_id
        id_classe_active = paiement.id_classe_active_id

        # ========================== VERIF DATE ==========================
        if date_paie:
            date_paie = datetime.datetime.strptime(date_paie, "%Y-%m-%d").date()

            today = datetime.date.today()

            if date_paie > today:
                return JsonResponse({
                    'success': False,
                    'error': f"La date de paiement ({date_paie}) ne peut pas être future."
                })
        else:
            date_paie = paiement.date_paie

        # ========================== DATE BUTOIRE ==========================
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
            })

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

        # ========================== PRIX VARIABLE ==========================
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
            })

        prix_max = variable_prix.prix

        # ========================== REDUCTION ==========================
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
            montant_reduction = (prix_max * reduction.pourcentage) / 100
            montant_autorise = prix_max - montant_reduction

        # ========================== VERIFICATION CUMUL ==========================
        total_deja_paye = Paiement.objects.filter(
            id_eleve_id=id_eleve,
            id_variable_id=id_variable,
            status=True
        ).exclude(id_paiement=id_paiement).aggregate(total=Sum('montant'))['total'] or 0

        if total_deja_paye + montant > montant_autorise:

            montant_restant = montant_autorise - total_deja_paye

            message = (
                f"Le paiement dépasse le montant autorisé.\n"
                f"Montant à payer : {montant_autorise}\n"
                f"Déjà payé : {total_deja_paye}\n"
                f"Montant restant : {montant_restant}"
            )

            if reduction:
                message = (
                    f"L'élève bénéficie d'une réduction de {reduction.pourcentage}%.\n"
                    f"Montant autorisé : {montant_autorise}\n"
                    f"Déjà payé : {total_deja_paye}\n"
                    f"Reste : {montant_restant}"
                )

            return JsonResponse({'success': False, 'error': message})

        # ========================== SAVE ==========================
        paiement.montant = montant
        paiement.date_paie = date_paie

        if bordereau:
            file_extension = os.path.splitext(bordereau.name)[1]
            new_filename = f"{bordereau.name}_{paiement.id_paiement}"
            paiement.bordereau.save(new_filename, bordereau, save=False)
            paiement.bordereau.name = new_filename

        paiement.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erreur update paiement : {str(e)}'
        })


# ===============================
# UPDATE REDUCTION
# ===============================
@require_POST
def suivi_reduction_update(request, id):

    try:
        reduction = Eleve_reduction_prix.objects.get(id_reduction_prix=id)

        statut = request.POST.get('statut')

        if not statut:
            return JsonResponse({'success': False, 'error': 'Valeur vide.'})

        reduction.pourcentage = statut
        reduction.save()

        return JsonResponse({'success': True})

    except Eleve_reduction_prix.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Réduction introuvable.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ===============================
# UPDATE DEROGATION
# ===============================
@require_POST
def suivi_derogation_update(request, id):

    try:
        derogation = VariableDerogation.objects.get(id_derogation=id)

        statut = request.POST.get('statut')

        if not statut:
            return JsonResponse({'success': False, 'error': 'Valeur vide.'})

        derogation.date_derogation = statut
        derogation.save()

        return JsonResponse({'success': True})

    except VariableDerogation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dérogation introuvable.'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    


@require_POST
def update_date_butoire(request, id):

    try:
        date_butoire = request.POST.get('date_butoire')

        obj = VariableDatebutoire.objects.get(id_datebutoire=id)
        obj.date_butoire = date_butoire
        obj.save()

        return JsonResponse({
            "success": True
        })

    except VariableDatebutoire.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Date butoire introuvable"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })
    

@csrf_exempt
def update_variable_obligatoire(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            variable_id = data.get('id_variable')
            est_obligatoire = data.get('estObligatoire', False)

            variable = Variable.objects.get(id_variable=variable_id)
            variable.estObligatoire = est_obligatoire
            variable.save()

            return JsonResponse({'success': True})
        except Variable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Variable non trouvée'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
