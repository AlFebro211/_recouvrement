
from django.contrib import admin
from django.urls import path
from app import views

# RECOUVREMENT :
urlpatterns =[
   path('categorie_variable/', views.ajouter_categorie_variable, name='categorie_variable'),
   path('create_variable_frais/', views.ajouter_variable, name='create_variable_frais'),
   path('update_categorie/<int:categorie_id>/', views.update_categorie, name='update_categorie'),
   path('update_variable/<int:variable_id>/', views.update_variable, name='update_variable'),
   path('get_categories/', views.get_categories, name='get_categories'),
   path('create_banque/', views.ajouter_banque_epargne, name='create_banque'),
   path('create_compte/', views.ajouter_compte_epargne, name='create_compte'),
   path('update_banque/<int:banque_id>/', views.update_banque, name='update_banque'),
   path('get_banques/', views.get_banques, name='get_banques'),
   path('update_compte/<int:compte_id>/', views.update_compte, name='update_compte'),
   path('create_variable_prix', views.ajouter_variable_prix, name='create_variable_prix'),
   path('create_variable_reduction', views.ajouter_reduction_for_pupil, name='create_variable_reduction'),
   path('create_derogation_classe', views.ajouter_variable_derogation, name='create_derogation_classe'),
   path('store_annee_session/', views.store_annee_session, name='store_annee_session'),
   path('get_classes_actives/<int:annee_id>/', views.get_classes_actives, name='get_classes_actives'),
   path('get_classes_actives_with_paie/<int:annee_id>/', views.get_classes_actives_avec_paiement, name='get_classes_actives_with_paie'),
   path('save_variable_prix/', views.save_variable_prix, name='save_variable_prix'),
   path('save_variable_derogation/', views.save_variable_derogation, name='save_variable_derogation'),
   path('save_variable_reduction/', views.save_variable_reduction, name='save_variable_reduction'),
   path('ajouter_date_butoire/', views.ajouter_date_butoire_for_anyclass, name='ajouter_date_butoire'),
   path('save_date_butoire/', views.save_variable_date_butoire, name='save_date_butoire'),
   path('', views.add_paiement_for_anyclass, name='ajouter_paiement'),
   path('get_comptes_banque/<int:id_banque>/', views.get_comptes_banque, name='get_comptes_banque'),
   path('save_paiement/', views.save_paiement, name='save_paiement'),
   path('afficher_paiement_submitted/', views.get_all_paiement_soumises, name='afficher_paiement_submitted'),
   path('paiement_valider/', views.get_all_paiement_soumises, name='paiement_valider'),
   path('get_paiements_submitted/', views.get_paiements_submitted, name='get_paiements_submitted'),
   path('get_paiements_validated/', views.get_paiements_validated, name='get_paiements_validated'),
   path('update_paiement_field/', views.update_paiement_field, name='update_paiement_field'),
   path('generate_invoice/<int:id_paiement>/', views.generate_invoice, name='generate_invoice'),
   path('generate_fiche_paie_classe/', views.generate_fiche_paie_classe, name='generate_fiche_paie_classe'),
   path('get_pupils_registred_classe/', views.get_pupils_registred_classe, name='get_pupils_registred_classe'),
   path('get_variables_restant_a_payer/',views.get_variables_restant_a_payer,name='get_variables_restant_a_payer'),
   path('get_trimestres_by_classe_active/', views.get_trimestres_by_classe_active, name='get_trimestres_by_classe_active'),
   path('get-variables-by-trimestre/',views.get_variables_by_trimestre,name='get_variables_by_trimestre'),
   path('generate_fiche_paie_eleve/', views.generate_fiche_paie_eleve, name='generate_fiche_paie_eleve'),
   path('get_eleves_classe/', views.get_eleves_classe, name='get_eleves_classe'),
   path('get_paiements_eleve/', views.get_paiements_eleve, name='get_paiements_eleve'),


   path('ajouter_penalite/', views.ajouter_penalite, name='ajouter_penalite'),
   path('save_penalite/', views.save_penalite, name='save_penalite'),


   
]