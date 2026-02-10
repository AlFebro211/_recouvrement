from app.forms.recouvrement_forms import PaiementUpdateForm
from.create_base import *
from app.models import *
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import date



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
                    "id_eleve": p.id_eleve.id_eleve,
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

def get_paiements_for_add_page(request):
    """
    Retourne les paiements filtrés pour la page d'ajout,
    seulement ceux avec status=True
    """
    id_annee = request.GET.get('id_annee')
    id_classe = request.GET.get('id_classe_active')
    id_eleve = request.GET.get('id_eleve')

    paiements = Paiement.objects.filter(status=True)

    if id_annee:
        paiements = paiements.filter(id_annee_id=id_annee)
    if id_classe:
        paiements = paiements.filter(id_classe_active_id=id_classe)
    if id_eleve:
        paiements = paiements.filter(id_eleve_id=id_eleve)

    data = []
    for p in paiements:
        data.append({
            "id": p.id_paiement,
            "eleve": str(p.id_eleve),
            "variable": str(p.id_variable),
            "montant": p.montant,
            "bordereau": p.bordereau.url if p.bordereau else None,
            "date_paie": p.date_paie.strftime("%Y-%m-%d") if p.date_paie else None,
            "status": p.status,
            "is_rejected": p.is_rejected
        })

    return JsonResponse({"success": True, "data": data})


@csrf_exempt
def get_pupils_registred_classe(request):
    id_annee = request.GET.get('id_annee')
    id_campus = request.GET.get('id_campus')
    id_cycle = request.GET.get('id_cycle')
    id_classe = request.GET.get('id_classe_active')

    if not all([id_annee, id_campus, id_cycle, id_classe]):
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        from django.utils.timezone import now
        today = now().date()

        # 🔹 Trimestre en cours
        trimestre_en_cours = Annee_trimestre.objects.filter(
            id_annee=id_annee,
            id_campus=id_campus,
            id_cycle=id_cycle,
            id_classe=id_classe,
            # debut__lte=today,
            # fin__gte=today,
            etat_trimestre='En attente'
        ).first()

        if not trimestre_en_cours:
            return JsonResponse({'success': True, 'data': [], 'count': 0})

        # 🔹 Variables définies pour la classe (source mobile)
        variables_prix = VariablePrix.objects.filter(
            id_annee=id_annee,
            id_campus=id_campus,
            id_cycle_actif=id_cycle,
            id_classe_active=id_classe
        ).select_related('id_variable')

        # 🔹 Élèves inscrits
        inscriptions = Eleve_inscription.objects.filter(
            id_annee=id_annee,
            id_campus=id_campus,
            id_classe_cycle=id_cycle,
            id_classe=id_classe,
            status=1
        ).select_related('id_eleve').distinct()

        pupils_data = []

        for ins in inscriptions:
            eleve = ins.id_eleve
            total_a_payer = 0
            total_paye = 0

            for vp in variables_prix:
                montant = vp.prix

                # 🔻 Réduction éventuelle
                reduction = Eleve_reduction_prix.objects.filter(
                    id_eleve=eleve,
                    id_variable=vp.id_variable,
                    id_annee=id_annee,
                    id_campus=id_campus,
                    id_cycle_actif=id_cycle,
                    id_classe_active=id_classe
                ).first()

                if reduction:
                    montant -= montant * reduction.pourcentage / 100

                total_a_payer += montant

                paye = Paiement.objects.filter(
                    id_eleve=eleve,
                    id_variable=vp.id_variable
                ).aggregate(total=Sum('montant'))['total'] or 0

                total_paye += paye

            # 🔥 IMPORTANT : afficher seulement les débiteurs
            if total_paye < total_a_payer:
                pupils_data.append({
                    'id_eleve': eleve.id_eleve,
                    'nom_complet': f"{eleve.nom} {eleve.prenom}",
                    'reste_a_payer': total_a_payer - total_paye,
                    'trimestre': trimestre_en_cours.trimestre.trimestre
                })

        return JsonResponse({
            'success': True,
            'data': pupils_data,
            'count': len(pupils_data)
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



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


# def get_variables_restant_a_payer(request):
#     eleve_id = request.GET.get('id_eleve')
#     annee_id = request.GET.get('id_annee')
#     campus_id = request.GET.get('id_campus')
#     cycle_id = request.GET.get('id_cycle')
#     classe_id = request.GET.get('id_classe')

#     variables_prix = VariablePrix.objects.filter(
#         id_annee_id=annee_id,
#         id_campus_id=campus_id,
#         id_cycle_actif_id=cycle_id,
#         id_classe_active_id=classe_id
#     ).select_related('id_variable')

#     result = []

#     for vp in variables_prix:
#         variable = vp.id_variable
#         montant_max = vp.prix

#         reduction = Eleve_reduction_prix.objects.filter(
#             id_eleve_id=eleve_id,
#             id_variable_id=variable.id_variable,
#             id_annee_id=annee_id,
#             id_campus_id=campus_id,
#             id_cycle_actif_id=cycle_id,
#             id_classe_active_id=classe_id
#         ).first()

#         if reduction:
#             montant_max -= (montant_max * reduction.pourcentage / 100)

#         total_paye = Paiement.objects.filter(
#             id_eleve_id=eleve_id,
#             id_variable_id=variable.id_variable,
#             id_annee_id=annee_id,
#             id_campus_id=campus_id,
#             id_cycle_actif_id=cycle_id,
#             id_classe_active_id=classe_id
#         ).aggregate(total=Sum('montant'))['total'] or 0

#         reste = max(0, montant_max - total_paye)

#         if reste > 0:
#             result.append({
#                 'id_variable': variable.id_variable,
#                 'nom_variable': variable.variable,
#                 'montant_total': montant_max,
#                 'total_deja_paye': total_paye,
#                 'reste_a_payer': reste,
#                 'reduction': reduction.pourcentage if reduction else 0
#             })

#     return JsonResponse({'success': True, 'variables': result})


def get_variables_restant_a_payer(request):
    eleve_id = request.GET.get('id_eleve')
    annee_id = request.GET.get('id_annee')
    campus_id = request.GET.get('id_campus')
    cycle_id = request.GET.get('id_cycle')
    classe_id = request.GET.get('id_classe')

    # 🔹 Pour l'instant on récupère même si le trimestre est "En attente"
    annee_trimestre = Annee_trimestre.objects.filter(
        id_annee_id=annee_id,
        id_campus_id=campus_id,
        id_cycle_id=cycle_id,
        id_classe_id=classe_id,
        etat_trimestre="En cours"  # 🔹 récupère les trimestres en attente
    ).select_related('trimestre').first()

    # 🔹 DEBUG : afficher tous les trimestres existants pour cette classe
    print("=== DEBUG trimestres disponibles ===")
    trimestres = Annee_trimestre.objects.filter(
        id_annee_id=annee_id,
        id_campus_id=campus_id,
        id_cycle_id=cycle_id,
        id_classe_id=classe_id,
    )
    for t in trimestres:
        print(
            t.trimestre.trimestre,
            t.debut,
            t.fin,
            t.etat_trimestre
        )

    if not annee_trimestre:
        return JsonResponse({
            'success': False,
            'error': 'Aucun trimestre trouvé pour cette classe'
        }, status=400)

    # 🔹 Récupérer toutes les variables liées à ce trimestre
    variables_prix = VariablePrix.objects.filter(
        id_annee_trimestre=annee_trimestre
    ).select_related('id_variable', 'id_variable__id_variable_categorie')
    print("====variables prix trouvées====")
    print(list(variables_prix.values()))


    result = []

    for vp in variables_prix:
        variable = vp.id_variable
        montant_max = vp.prix

        # 🔹 Appliquer réduction si elle existe
        reduction = Eleve_reduction_prix.objects.filter(
            id_eleve_id=eleve_id,
            id_variable_id=variable.id_variable,
            id_annee_id=annee_id,
            id_campus_id=campus_id,
            id_cycle_actif_id=cycle_id,
            id_classe_active_id=classe_id
        ).first()

        if reduction:
            montant_max -= montant_max * reduction.pourcentage / 100

        # 🔹 Somme déjà payée
        total_paye = Paiement.objects.filter(
            id_eleve_id=eleve_id,
            id_variable_id=variable.id_variable,
            id_annee_id=annee_id,
            id_campus_id=campus_id,
            id_cycle_actif_id=cycle_id,
            id_classe_active_id=classe_id
        ).aggregate(total=Sum('montant'))['total'] or 0
        print ("DEBUG total_paye for variable", variable.variable, ":", total_paye)
        print ("DEBUG montant_max for variable", variable.variable, ":", montant_max)
        print ("-----------------------------")

        # 🔹 Calculer le reste à payer
        reste = max(0, montant_max - total_paye)
        print(f"Variable: {variable.variable}, Montant max: {montant_max}, Total payé: {total_paye}, Reste: {reste}")
        print ("DEBUG reste for variable", variable.variable, ":", reste)
        print(variable.variable, montant_max, total_paye, reste)

        if reste > 0:
            result.append({
                'id_variable': variable.id_variable,
                'nom_variable': variable.variable,
                'categorie': variable.id_variable_categorie.nom,
                'montant_total': montant_max,
                'total_deja_paye': total_paye,
                'reste_a_payer': reste,
                'trimestre': annee_trimestre.trimestre.trimestre,
                'id_trimestre': annee_trimestre.trimestre.id_trimestre
            })

    return JsonResponse({
        'success': True,
        'annee_trimestre': {
            'id': annee_trimestre.trimestre.id_trimestre,
            'trimestre': annee_trimestre.trimestre.trimestre,
            'etat': annee_trimestre.etat_trimestre,
            'debut': annee_trimestre.debut,
            'fin': annee_trimestre.fin
        },
        'variables': result
    })



def get_trimestres_by_classe_active(request):
    classe_active_id = request.GET.get('id_classe_active')
    annee_id = request.GET.get('id_annee')
    campus_id = request.GET.get('id_campus')
    cycle_id = request.GET.get('id_cycle')

    if not all([classe_active_id, annee_id, campus_id, cycle_id]):
        return JsonResponse({'success': False, 'error': 'Paramètres manquants'})

    trimestres_qs = Annee_trimestre.objects.filter(
        id_annee_id=annee_id,
        id_classe_id=classe_active_id,
        id_campus_id=campus_id,
        id_cycle_id=cycle_id
    ).select_related('trimestre').order_by('trimestre__trimestre')

    data = [
        {
            'id': t.id_trimestre,  # ✅ IMPORTANT (plus trimestre.id)
            'nom': t.trimestre.trimestre,
            'etat': t.etat_trimestre
        }
        for t in trimestres_qs
    ]

    return JsonResponse({'success': True, 'trimestres': data})



def get_variables_by_trimestre(request):
    # 🔹 Paramètres
    annee_trimestre_id = request.GET.get('id_trimestre')  # id_annee_trimestre
    classe_id = request.GET.get('id_classe')
    annee_id = request.GET.get('id_annee')
    campus_id = request.GET.get('id_campus')
    cycle_id = request.GET.get('id_cycle')

    if not all([annee_trimestre_id, classe_id, annee_id, campus_id, cycle_id]):
        return JsonResponse({
            'success': False,
            'error': 'Paramètres manquants'
        }, status=400)

    # 🔹 Récupérer le trimestre
    annee_trimestre = Annee_trimestre.objects.filter(
        id_trimestre=annee_trimestre_id
    ).select_related('trimestre').first()

    if not annee_trimestre:
        return JsonResponse({
            'success': False,
            'error': 'Trimestre invalide'
        }, status=400)

    # 🔹 Récupérer les VariablePrix liées
    variable_prix_qs = VariablePrix.objects.filter(
        id_annee_trimestre_id=annee_trimestre_id,
        id_classe_active_id=classe_id,
        id_annee_id=annee_id,
        id_campus_id=campus_id,
        id_cycle_actif_id=cycle_id
    ).select_related('id_variable', 'id_variable__id_variable_categorie') \
     .order_by('id_variable_id')

    # 🔹 Préparer la liste des variables avec prix
    variables_data = [
        {
            'id_variable': vp.id_variable.id_variable,
            'nom_variable': vp.id_variable.variable,
            'categorie': vp.id_variable.id_variable_categorie.nom,
            'prix': vp.prix
        }
        for vp in variable_prix_qs
    ]

    return JsonResponse({
        'success': True,
        'annee_trimestre': {
            'id': annee_trimestre.id_trimestre,
            'trimestre': annee_trimestre.trimestre.trimestre,
            'etat': annee_trimestre.etat_trimestre,
            'debut': annee_trimestre.debut,
            'fin': annee_trimestre.fin
        },
        'variables': variables_data
    })


def get_eleves_classe(request):
    id_campus = request.GET.get('id_campus')
    id_cycle_actif = request.GET.get('id_cycle')
    id_classe_active = request.GET.get('id_classe_active')
    id_annee = request.GET.get('id_annee')

    # 1️⃣ récupérer la classe active
    classe_active = Classe_active.objects.filter(
        id_classe_active=id_classe_active,
        id_campus_id=id_campus,
        id_annee_id=id_annee,
        is_active=True
    ).first()

    if not classe_active:
        return JsonResponse([], safe=False)

    # 2️⃣ récupérer les élèves inscrits dans cette classe
    eleves = Eleve_inscription.objects.filter(
        id_campus_id=id_campus,
        id_annee_id=id_annee,
        id_classe_id=id_classe_active,   # ✅ correspondance réelle
        id_classe_cycle_id=id_cycle_actif,
        status=1
    ).select_related('id_eleve').distinct()

    data = [{
        "id_eleve": e.id_eleve.id_eleve,
        "nom": e.id_eleve.nom,
        "prenom": e.id_eleve.prenom
    } for e in eleves]

    return JsonResponse(data, safe=False)


def historique_financier(request):

    def clean(v): 
        return v if v not in ("", None) else None

    id_annee = clean(request.GET.get('annee'))
    id_classe = clean(request.GET.get('classe'))
    id_eleve = clean(request.GET.get('eleve'))
    id_trimestre = clean(request.GET.get('trimestre'))
    id_compte = clean(request.GET.get('compte'))

    paiements_qs = Paiement.objects.select_related(
        'id_eleve',
        'id_variable',
        'id_compte',
        'id_compte__id_banque'
    ).order_by(
        'id_eleve__nom',
        'id_variable__variable',
        'date_paie'
    )

    if id_annee:
        paiements_qs = paiements_qs.filter(id_annee=id_annee)
    if id_classe:
        paiements_qs = paiements_qs.filter(id_classe_active=id_classe)
    if id_eleve:
        paiements_qs = paiements_qs.filter(id_eleve=id_eleve)
    if id_trimestre:
        paiements_qs = paiements_qs.filter(id_variable__trimestre=id_trimestre)
    if id_compte:
        paiements_qs = paiements_qs.filter(id_compte=id_compte)

    rapport = []
    total_general = 0

    for p in paiements_qs:
        total_general += p.montant

        rapport.append({
            "eleve": f"{p.id_eleve.nom} {p.id_eleve.prenom}",
            "variable": p.id_variable.variable,
            "montant": p.montant,
            "date_paie": p.date_paie.strftime('%d/%m/%Y'),
            "banque_compte": f"{p.id_compte.id_banque.banque} - {p.id_compte.compte}"
        })

    return JsonResponse({
        "success": True,
        "rapport": rapport,
        "total_general": total_general
    })

def eleves_en_dette(request):

    id_annee = request.GET.get('annee')
    id_classe = request.GET.get('classe')
    id_trimestre = request.GET.get('trimestre')

    if not id_annee or not id_classe:
        return JsonResponse({
            "success": False,
            "message": "Année et classe obligatoires"
        })

    # 🔹 1. Récupérer les INSCRIPTIONS (BASE)
    inscriptions = Eleve_inscription.objects.select_related(
        'id_eleve',
        'id_classe',
        'id_classe__classe_id'
    ).filter(
        id_annee=id_annee,
        id_classe=id_classe,
        status=True
    )

    if id_trimestre:
        inscriptions = inscriptions.filter(id_trimestre=id_trimestre)

    rapport = []

    for ins in inscriptions:
        eleve = ins.id_eleve

        # Nom classe + groupe
        nom_classe = ins.id_classe.classe_id.classe
        groupe = ins.id_classe.groupe or ""
        classe_info = f"{nom_classe} {groupe}".strip()

        # 🔹 Paiements de l'élève
        paiements = Paiement.objects.filter(
            id_eleve=eleve,
            id_classe_active=id_classe,
            id_annee=id_annee
        )

        # 🔹 Variables attendues pour la classe
        variables = VariablePrix.objects.filter(
            id_classe_active=id_classe,
            id_annee=id_annee
        ).select_related('id_variable')

        details = []
        total_dette = 0

        for vp in variables:
            variable = vp.id_variable

            montant_a_payer = vp.prix

            montant_paye = paiements.filter(
                id_variable=variable
            ).aggregate(total=Sum('montant'))['total'] or 0

            reste = max(montant_a_payer - montant_paye, 0)

            # 🔹 pénalité (simple)
            penalite = 0
            if reste > 0:
                penalite = PenaliteConfig.objects.filter(
                    id_variable=variable,
                    id_classe_active=id_classe,
                    actif=True
                ).aggregate(total=Sum('valeur'))['total'] or 0

            total_variable = reste + penalite
            print("DEBUG dette for variable", variable.variable, ":", total_variable)

            if total_variable > 0:
                details.append({
                    "variable": variable.variable,
                    "montant_a_payer": montant_a_payer,
                    "montant_paye": montant_paye,
                    "reste": reste,
                    "penalite": penalite,
                    "total": total_variable
                })

                total_dette += total_variable

        if total_dette > 0:
            rapport.append({
                "id_eleve": eleve.id_eleve,
                "eleve": f"{eleve.nom} {eleve.prenom}",
                "classe": classe_info,
                "total_dette": total_dette,
                "details": details
            })

    return JsonResponse({
        "success": True,
        "rapport": rapport
    })


def get_penalites(request):
    penalites = PenaliteConfig.objects.select_related(
        'id_annee',
        'id_campus',
        'id_cycle_actif',
        'id_classe_active',
        'id_variable',
        'id_annee_trimestre'
    ).order_by('-id_penalite_regle')

    data = []

    for p in penalites:
        data.append({
            'id_penalite_regle': p.id_penalite_regle,
            'annee': str(p.id_annee) if p.id_annee else '',
            'campus': str(p.id_campus) if p.id_campus else '',
            'cycle': str(p.id_cycle_actif) if p.id_cycle_actif else '',
            'classe': str(p.id_classe_active) if p.id_classe_active else '',
            'variable': str(p.id_variable) if p.id_variable else '',
            'trimestre': str(p.id_annee_trimestre) if p.id_annee_trimestre else '',
            'type_penalite': p.type_penalite,
            'valeur': p.valeur,
            'plafond': p.plafond if p.plafond else '',
            'actif': p.actif
        })

    return JsonResponse({'success': True, 'penalites': data})

@csrf_exempt
def toggle_penalite_actif(request):
    if request.method == 'POST':
        penalite_id = request.POST.get('id_penalite')
        actif = request.POST.get('actif') == 'true'

        try:
            penalite = PenaliteConfig.objects.get(id_penalite_regle=penalite_id)
            penalite.actif = actif
            penalite.save()
            return JsonResponse({'success': True})
        except PenaliteConfig.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pénalité non trouvée'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

from django.http import JsonResponse
from django.db.models import Q

def eleves_en_penalite(request):

    id_campus   = request.GET.get('id_campus')
    id_cycle    = request.GET.get('id_cycle')
    id_classe   = request.GET.get('classe')
    annee       = request.GET.get('annee')
    variable_id = request.GET.get('variable')
    trimestre   = request.GET.get('trimestre')

    if not annee:
        return JsonResponse({'success': False, 'error': 'Veuillez sélectionner une année.'})

    # ================================
    # FILTRE INSCRIPTION ELEVE
    # ================================
    filtre_eleve = Q(id_annee_id=annee, status=True)

    if id_campus:
        filtre_eleve &= Q(id_campus_id=id_campus)

    if id_cycle:
        filtre_eleve &= Q(id_classe_cycle_id=id_cycle)

    if id_classe:
        filtre_eleve &= Q(id_classe_id=id_classe)

    if trimestre:
        filtre_eleve &= Q(id_trimestre_id=trimestre)

    # IMPORTANT : select_related pour performance
    inscriptions = Eleve_inscription.objects.filter(
        filtre_eleve
    ).select_related('id_eleve')

    # ================================
    # FILTRE CONFIG PENALITE
    # ================================
    filtre_config = Q(id_annee_id=annee, actif=True)

    if variable_id:
        filtre_config &= Q(id_variable_id=variable_id)

    if trimestre:
        filtre_config &= Q(id_annee_trimestre_id=trimestre)

    if id_campus:
        filtre_config &= Q(id_campus_id=id_campus)

    if id_cycle:
        filtre_config &= Q(id_cycle_actif_id=id_cycle)

    configs = PenaliteConfig.objects.filter(filtre_config)

    resultats = []

    # ================================
    # LOGIQUE PENALITE
    # ================================
    for config in configs:

        db_obj = VariableDatebutoire.objects.filter(
            id_variable=config.id_variable,
            id_annee=config.id_annee,
            id_campus=config.id_campus,
            id_cycle_actif=config.id_cycle_actif
        ).first()

        if not db_obj:
            continue

        eleves_concernes = inscriptions.filter(
            id_campus=config.id_campus,
            id_classe_cycle=config.id_cycle_actif
        )

        for insc in eleves_concernes:

            eleve = insc.id_eleve   # ✅ LE BON OBJET ELEVE

            # ================= DEROGATION
            derog = VariableDerogation.objects.filter(
                id_eleve=eleve,
                id_variable=config.id_variable,
                id_annee_id=annee
            ).first()

            date_limite = derog.date_derogation if derog else db_obj.date_butoire

            # ================= PAIEMENT
            paiement = Paiement.objects.filter(
                id_eleve=eleve,
                id_variable=config.id_variable,
                id_annee_id=annee,
                status=True
            ).order_by('date_paie').first()

            if paiement and paiement.date_paie and paiement.date_paie <= date_limite:
                continue

            # ================= PRIX
            prix_obj = VariablePrix.objects.filter(
                id_variable=config.id_variable,
                id_annee_id=annee,
                id_campus=config.id_campus,
                id_cycle_actif=config.id_cycle_actif
            ).first()

            montant_base = prix_obj.prix if prix_obj else 0

            reduc = Eleve_reduction_prix.objects.filter(
                id_eleve=eleve,
                id_variable=config.id_variable
            ).first()

            if reduc:
                montant_base -= (montant_base * reduc.pourcentage / 100)

            # ================= PENALITE
            if config.type_penalite == 'FORFAIT':
                montant_p = config.valeur
            else:
                montant_p = (montant_base * config.valeur / 100)
                if config.plafond:
                    montant_p = min(montant_p, config.plafond)

            resultats.append({
                'eleve': f"{eleve.nom} {eleve.prenom}",
                'variable': config.id_variable.variable,
                'date_limite': date_limite.strftime('%d/%m/%Y'),
                'montant_penalite': round(montant_p, 2)
            })

    return JsonResponse({'success': True, 'eleves': resultats})
