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

simulation.set_input('salary', period, np.array(data.salary))
simulation.set_input('age', period, np.array(data.age))
result = simulation.calculate('income_tax', period)

print(result)
