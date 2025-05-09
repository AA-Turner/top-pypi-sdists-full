from openfisca_france.model.base import *


class aeeh_niveau_handicap(Variable):
    value_type = int
    entity = Individu
    label = "Catégorie de handicap prise en compte pour l'AEEH"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aeeh(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation de l'enfant handicapé"
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F14809'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2006_01_01(famille, period, parameters):
        '''Allocation d'éducation de l'enfant handicapé.

        Remplace l'allocation d'éducation spéciale (AES) depuis le 1er janvier 2006.
        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.
        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit
        son activité professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        '''
        isole = not_(famille('en_couple', period))
        prestations_familiales = parameters(period).prestations_sociales.prestations_familiales

        base = prestations_familiales.education_presence_parentale.aeeh.base
        complement_d_allocation = prestations_familiales.education_presence_parentale.aeeh.complement_allocation
        majoration = prestations_familiales.education_presence_parentale.aeeh.majoration_parent_isole

        age = famille.members('age', period)
        handicap = famille.members('handicap', period)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)

        # Indicatrice d'isolement pour les indidivus
        isole = famille.project(isole)
        enfant_handicape = handicap * (age < prestations_familiales.education_presence_parentale.aeeh.age_maximum_enfant)
        montant_par_enfant = enfant_handicape * prestations_familiales.bmaf.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation.categorie_1
            + (niveau_handicap == 2) * (complement_d_allocation.categorie_1 + majoration.categorie_2 * isole)
            + (niveau_handicap == 3) * (complement_d_allocation.categorie_2 + majoration.categorie_3 * isole)
            + (niveau_handicap == 4) * (complement_d_allocation.categorie_3 + majoration.categorie_4 * isole)
            + (niveau_handicap == 5) * (complement_d_allocation.categorie_4 + majoration.categorie_5 * isole)
            + (niveau_handicap == 6) * majoration.categorie_6 * isole
            ) + (niveau_handicap == 6) * complement_d_allocation.categorie_6

        montant_total = famille.sum(montant_par_enfant, role = Famille.ENFANT)

        # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
        # versement des prestations familiales.
        # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
        # complément ni avec la majoration de parent isolé.
        # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
        # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
        # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
        # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumises à la CRDS
        return montant_total


class aes(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation spéciale"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    end = '2005-12-31'

    def formula_2002_04_01(famille, period, parameters):
        janvier = period.this_year.first_month
        # isole = not_(famille('en_couple', janvier))
        prestations_familiales = parameters(period).prestations_sociales.prestations_familiales

        base = prestations_familiales.education_presence_parentale.aes.base
        complement_d_allocation = prestations_familiales.education_presence_parentale.aes.complement_d_allocation
        complement_d_allocation.categorie_6 = complement_d_allocation.categorie_6

        age = famille.members('age', janvier)
        handicap = famille.members('handicap', janvier)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)
        # Indicatrice d'isolement pour les indidivus
        # isole = famille.project(isole)

        enfant_handicape = handicap * (age < prestations_familiales.education_presence_parentale.aes.age_maximum_enfant)

        montant_par_enfant = enfant_handicape * prestations_familiales.bmaf.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation.categorie_1
            + (niveau_handicap == 2) * complement_d_allocation.categorie_1
            )

        montant_total = famille.sum(montant_par_enfant, role = Famille.ENFANT)
        return montant_total
