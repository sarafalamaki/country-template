# -*- coding: utf-8 -*-

import pandas as pds
import numpy as np

from openfisca_core.simulations import Simulation
from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_country_template import CountryTaxBenefitSystem

tax_benefit_system = CountryTaxBenefitSystem()

data = pds.read_csv('./openfisca.csv')
n = len(data)

simulation = SimulationBuilder().build_default_simulation(tax_benefit_system, n)
period = '2017-01'

# What if there are 200 fields? 
# salary_m1 / salary_m2 / salary_m3
simulation.set_input('salary', period, np.array(data.salary))
simulation.set_input('age', period, np.array(data.age))
result = simulation.calculate('income_tax', period)

household_id = data.household_id.values

#could be a helper: simulation.household.set_ids() 
# unique = np.unique(household_id).tolist()
# household_index = np.array([unique.index(value) for value in household_id])

households = np.sort(np.unique(household_id))
household_index = np.searchsorted(households, household_id)
simulation.household.members_entity_id = household_index

#could be a helper: simulation.household.set_roles() 
# simulation.household.members_role = ... 
# roles = simulation.household.roles
# simulation.household_role = np.select([data.role == role for role in roles], roles)

print(result)
