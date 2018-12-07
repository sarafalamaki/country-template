# -*- coding: utf-8 -*-

import pandas as pds
import numpy as np

# from openfisca_core.simulations import Simulation
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_country_template import CountryTaxBenefitSystem

tax_benefit_system = CountryTaxBenefitSystem()

data = pds.read_csv('./data_persons.csv')
n = len(data)

simulation = SimulationBuilder().build_default_simulation(tax_benefit_system, n)


# SIMPLE CASE > income_tax
# ------------------------
# Cas d'usage de Joan : Ok, lets get some variable value from a CSV file
# Let’s get some variable value using pandas

period = '2017-01'

# match data from 'person_salary' column
# with 'salary' variable of the tax and benefit system
simulation.set_input('salary', period, np.array(data.person_salary))

income_tax = simulation.calculate('income_tax', period)

print(data.person_id.values)
print(income_tax)
print(income_tax.item(2))

# TWO ENTITIES > total_taxes
# --------------------------
# and how to build households ?

data_households = pds.read_csv('./data_households.csv')

data_households_values = data_households.household_id.values
households = np.sort(np.unique(data_households_values))
data_households_indexes = np.searchsorted(households, data_households_values)

simulation.household.members_entity_id = data_households_indexes

data_roles = data_households.role.values
roles = simulation.household.roles  # defined in the tax & benefit system
simulation.household._members_role = data_roles

total_taxes = simulation.calculate('total_taxes', period)  # ou total_benefits ?


# Calcul du disposable_income maximal par household suite à l'association des deux CSV
simulation.set_input('age', period, np.array(data.person_age))
disposable_income = simulation.calculate('disposable_income', period)

nb_persons = simulation.household.nb_persons()


# What if there are 200 fields? 
# salary_m1 / salary_m2 / salary_m3

#could be a helper: simulation.household.set_ids() 
#could be a helper: simulation.household.set_roles() 

# simulation.household.members_role = ... 
# roles = simulation.household.roles
# simulation.household_role = np.select([data.role == role for role in roles], roles)



# describe 'survey' in documentation
# parallel map on pandas ?
# "don't know"/none values in csv > filter
