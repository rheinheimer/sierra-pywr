import pyximport

pyximport.install(language_level=3)

from .cython_parameters import CustomParameter
from .custom_parameters import WaterLPParameter
