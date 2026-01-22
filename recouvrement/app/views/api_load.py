from.create_base import *
from app.models import Annee, Eleve_inscription, VariablePrix, Paiement, Eleve_reduction_prix
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum


def get_banques(request):
    banques = Banque.objects.all().values('id_banque', 'banque')
    return JsonResponse({'banques': list(banques)})


def get_categories(request):
    categories = VariableCategorie.objects.all().values('id_variable_categorie', 'nom')
    return JsonResponse({'categories': list(categories)})


@csrf_protect
def store_annee_session(request):
    if request.method == 'POST':
        try:
            annee_id = request.POST.get('id_annee')
            if not annee_id:
                return JsonResponse({'success': False, 'error': 'Aucune année sélectionnée.'})
            request.session['selected_annee_id'] = int(annee_id)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée.'})



def get_classes_actives(request, annee_id):
    try:
        
        if not Annee.objects.filter(id_annee=annee_id).exists():
            return JsonResponse({
                'success': False,
                'error': 'Année scolaire non trouvée.'
            }, status=404)

        classes = (
            Classe_active.objects.filter(
                id_annee=annee_id,
                is_active=True,
                eleve_inscription__status=1  
            )
            .select_related('id_campus', 'cycle_id__cycle_id', 'classe_id')
            .values(
                'id_classe_active',
                'id_campus__campus',
                'cycle_id__cycle_id__cycle',
                'classe_id__classe',
                'groupe',
                'id_campus__id_campus',
                'cycle_id__id_cycle_actif',
            )
            .distinct() 
        )

        formatted_classes = [
            {
                'id_classe_active': classe['id_classe_active'],
                'campus_nom': classe['id_campus__campus'],
                'cycle_nom': classe['cycle_id__cycle_id__cycle'],
                'classe_nom': classe['classe_id__classe'],
                'groupe': classe['groupe'] or '',
                'id_campus': classe['id_campus__id_campus'],
                'id_cycle': classe['cycle_id__id_cycle_actif'],
            }
            for classe in classes
        ]

        if not formatted_classes:
            return JsonResponse({
                'success': True,
                'classes': [],
                'message': 'Aucune classe active avec des inscrits trouvée pour cette année scolaire.'
            })

        return JsonResponse({
            'success': True,
            'classes': formatted_classes,
        })

    except Exception as e:
        logger.error(f"Erreur dans get_classes_actives pour annee_id={annee_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Une erreur est survenue lors de la récupération des classes.'
        }, status=500)



def get_classes_actives_avec_paiement(request, annee_id):
    try:
        if not Annee.objects.filter(id_annee=annee_id).exists():
            return JsonResponse({
                'success': False,
                'error': 'Année scolaire non trouvée.'
            }, status=404)

        classes = (
            Classe_active.objects.filter(
                id_annee=annee_id,
                is_active=True,
                paiement__id_annee=annee_id,
                paiement__status = 1
            )
            .select_related('id_campus', 'cycle_id__cycle_id', 'classe_id')
            .values(
                'id_classe_active',
                'id_campus__campus',
                'cycle_id__cycle_id__cycle',
                'classe_id__classe',
                'groupe',
                'id_campus__id_campus',
                'cycle_id__id_cycle_actif',
            )
            .distinct()
        )

        formatted_classes = [
            {
                'id_classe_active': classe['id_classe_active'],
                'campus_nom': classe['id_campus__campus'],
                'cycle_nom': classe['cycle_id__cycle_id__cycle'],
                'classe_nom': classe['classe_id__classe'],
                'groupe': classe['groupe'] or '',
                'id_campus': classe['id_campus__id_campus'],
                'id_cycle': classe['cycle_id__id_cycle_actif'],
            }
            for classe in classes
        ]

        if not formatted_classes:
            return JsonResponse({
                'success': True,
                'classes': [],
                'message': 'Aucune classe active avec des paiements trouvée pour cette année scolaire.'
            })

        return JsonResponse({
            'success': True,
            'classes': formatted_classes,
        })

    except Exception as e:
        logger.error(f"Erreur dans get_classes_actives pour annee_id={annee_id}: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Une erreur est survenue lors de la récupération des classes.'
        }, status=500)



def get_comptes_banque(request, id_banque):
    try:
        comptes = Compte.objects.filter(id_banque_id=id_banque).values('id_compte', 'compte')
        formatted_comptes = [
            {
                'id_compte': compte['id_compte'],
                'compte': compte['compte']
            } for compte in comptes
        ]
        return JsonResponse({'success': True, 'comptes': formatted_comptes})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



#
def get_all_paiement_soumises(request):
    
    form = VariableDateButoireForm()
    all_paiement_soumises = Paiement.objects.all()
    return render(request, 'recouvrement/index_recouvrement.html', {
        'paiement_list':all_paiement_soumises,
        'form_paiement_validation': form,
        'form_type': 'validation_form',
       

    })



@csrf_exempt
def get_paiements_submitted(request):

    if request.method == "GET":
        try:
            id_campus = request.GET.get("id_campus")
            id_cycle_actif = request.GET.get("id_cycle")
            id_classe_active = request.GET.get("id_classe_active")
            id_annee = request.GET.get("id_annee")

            if not all([id_campus, id_cycle_actif, id_classe_active, id_annee]):
                return JsonResponse({
                    "success": False,
                    "error": "Paramètres requis manquants."
                }, status=400)

            paiements = Paiement.objects.filter(
                id_campus_id=id_campus,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active,
                id_annee_id=id_annee,
                status = 0,
                is_rejected = 0
                
            ).select_related("id_eleve", "id_variable")

            data = []
            for p in paiements:
                data.append({
                    "id_paiement": p.id_paiement,
                    "id_variable": p.id_variable.id_variable,
                    "variable": p.id_variable.variable,
                    "montant": p.montant,
                    "bordereau": p.bordereau.name if p.bordereau else "",
                    "status": p.status,
                    "eleve_nom": p.id_eleve.nom,
                    "eleve_prenom": p.id_eleve.prenom,
                })

            return JsonResponse({"success": True, "data": data}, safe=False)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Erreur serveur : {str(e)}"
            }, status=500)

    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)



@csrf_exempt
def get_paiements_validated(request):
  
    if request.method == "GET":
        try:
            id_campus = request.GET.get("id_campus")
            id_cycle_actif = request.GET.get("id_cycle")
            id_classe_active = request.GET.get("id_classe_active")
            id_annee = request.GET.get("id_annee")

            if not all([id_campus, id_cycle_actif, id_classe_active, id_annee]):
                return JsonResponse({
                    "success": False,
                    "error": "Paramètres requis manquants."
                }, status=400)

            paiements = Paiement.objects.filter(
                id_campus_id=id_campus,
                id_cycle_actif_id=id_cycle_actif,
                id_classe_active_id=id_classe_active,
                id_annee_id=id_annee,
                status = 1,
                
            ).select_related("id_eleve", "id_variable")

            data = []
            for p in paiements:
                data.append({
                    "id_paiement": p.id_paiement,
                    "id_variable": p.id_variable.id_variable,
                    "variable": p.id_variable.variable,
                    "montant": p.montant,
                    "bordereau": p.bordereau.name if p.bordereau else "",
                    "status": p.status,
                    "eleve_nom": p.id_eleve.nom,
                    "eleve_prenom": p.id_eleve.prenom,
                })

            return JsonResponse({"success": True, "data": data}, safe=False)

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Erreur serveur : {str(e)}"
            }, status=500)

    return JsonResponse({"success": False, "error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def get_pupils_registred_classe(request):
    id_annee = request.GET.get('id_annee')
    id_campus = request.GET.get('id_campus')
    id_cycle = request.GET.get('id_cycle')
    id_classe = request.GET.get('id_classe_active')

    if not all([id_annee, id_campus, id_cycle, id_classe]):
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        variables_prix = VariablePrix.objects.filter(
            id_annee_id=id_annee,
            id_campus_id=id_campus,
            id_cycle_actif_id=id_cycle,
            id_classe_active_id=id_classe
        ).select_related('id_variable')

        inscriptions = Eleve_inscription.objects.filter(
            id_annee=id_annee,
            id_campus=id_campus,
            id_classe_cycle=id_cycle,
            id_classe=id_classe,
            status=1
        ).select_related('id_eleve')

        pupils_data = []

        for inscription in inscriptions:
            eleve = inscription.id_eleve

            total_a_payer = 0
            total_paye = 0

            for vp in variables_prix:
                variable = vp.id_variable
                montant_variable = vp.prix

                reduction = Eleve_reduction_prix.objects.filter(
                    id_eleve_id=eleve.id_eleve,
                    id_variable_id=variable.id_variable,
                    id_annee_id=id_annee,
                    id_campus_id=id_campus,
                    id_cycle_actif_id=id_cycle,
                    id_classe_active_id=id_classe
                ).first()

                if reduction:
                    montant_variable -= (montant_variable * reduction.pourcentage / 100)

                total_a_payer += montant_variable

                paye = Paiement.objects.filter(
                    id_eleve_id=eleve.id_eleve,
                    id_variable_id=variable.id_variable
                ).aggregate(total=Sum('montant'))['total'] or 0

                total_paye += paye

            if total_paye < total_a_payer:
                pupils_data.append({
                    'id_eleve': eleve.id_eleve,
                    'nom_complet': f"{eleve.nom} {eleve.prenom}",
                    'total_a_payer': total_a_payer,
                    'total_paye': total_paye,
                    'reste_a_payer': total_a_payer - total_paye,
                    'status': inscription.status,
                    'redoublement': inscription.redoublement
                })

        return JsonResponse({
            'success': True,
            'data': pupils_data,
            'count': len(pupils_data)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# @csrf_exempt
# def get_pupils_registred_classe(request):
#     id_annee = request.GET.get('id_annee')
#     id_campus = request.GET.get('id_campus')
#     id_cycle = request.GET.get('id_cycle')
#     id_classe = request.GET.get('id_classe_active')

#     if not all([id_annee, id_campus, id_cycle, id_classe]):
#         return JsonResponse({'error': 'Paramètres manquants'}, status=400)
    

#     try:
#         inscriptions = Eleve_inscription.objects.filter(
#             Q(id_annee=id_annee) &
#             Q(id_campus=id_campus) &
#             Q(id_classe_cycle=id_cycle) &
#             Q(id_classe=id_classe), 
#             Q(status=1)
#         ).select_related('id_eleve').order_by('id_eleve')

#         seen_eleve_ids = set()
#         pupils_data = []
#         for inscription in inscriptions:
#             eleve = inscription.id_eleve
#             if eleve.id_eleve not in seen_eleve_ids:
#                 seen_eleve_ids.add(eleve.id_eleve)
#                 pupils_data.append({
#                     'id_eleve': eleve.id_eleve,
#                     'status': inscription.status, 
#                     'redoublement': inscription.redoublement,
#                     'nom_complet': f"{eleve.nom} {eleve.prenom}"
#                 })

#         return JsonResponse({
#             'success': True,
#             'data': pupils_data,
#             'count': len(pupils_data)
#         })

#     except Exception as e:
#         return JsonResponse({
#             'error': str(e),
#             'success': False
#         }, status=500)


def get_variables_restant_a_payer(request):
    eleve_id = request.GET.get('id_eleve')
    annee_id = request.GET.get('id_annee')
    campus_id = request.GET.get('id_campus')
    cycle_id = request.GET.get('id_cycle')
    classe_id = request.GET.get('id_classe')

    variables_prix = VariablePrix.objects.filter(
        id_annee_id=annee_id,
        id_campus_id=campus_id,
        id_cycle_actif_id=cycle_id,
        id_classe_active_id=classe_id
    ).select_related('id_variable')

    result = []

    for vp in variables_prix:
        variable = vp.id_variable
        montant_max = vp.prix

        reduction = Eleve_reduction_prix.objects.filter(
            id_eleve_id=eleve_id,
            id_variable_id=variable.id_variable,
            id_annee_id=annee_id,
            id_campus_id=campus_id,
            id_cycle_actif_id=cycle_id,
            id_classe_active_id=classe_id
        ).first()

        if reduction:
            montant_max -= (montant_max * reduction.pourcentage / 100)

        total_paye = Paiement.objects.filter(
            id_eleve_id=eleve_id,
            id_variable_id=variable.id_variable,
            id_annee_id=annee_id,
            id_campus_id=campus_id,
            id_cycle_actif_id=cycle_id,
            id_classe_active_id=classe_id
        ).aggregate(total=Sum('montant'))['total'] or 0

        reste = max(0, montant_max - total_paye)

        if reste > 0:
            result.append({
                'id_variable': variable.id_variable,
                'nom_variable': variable.variable,
                'montant_total': montant_max,
                'total_deja_paye': total_paye,
                'reste_a_payer': reste,
                'reduction': reduction.pourcentage if reduction else 0
            })

    return JsonResponse({'success': True, 'variables': result})








