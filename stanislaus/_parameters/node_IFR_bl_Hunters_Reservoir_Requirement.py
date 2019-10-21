import datetime
import calendar
from parameters import WaterLPParameter

from utilities.converter import convert

class node_IFR_bl_Hunters_Reservoir_Requirement(WaterLPParameter):
    """"""

    def _value(self, timestep, scenario_index):
        if datetime.date(timestep.year,5,1) <= datetime.date(timestep.year,timestep.month,timestep.day) <= datetime.date(timestep.year,10,31):
            ifr_val = 0.042475 # cms (1.5 cfs)
        else:
            ifr_val = 0.014158 #cms (0.5 cfs)

        if self.mode == 'planning':
            ifr_val *= self.days_in_planning_month(timestep, self.month_offset)
        return ifr_val
        
    def value(self, timestep, scenario_index):
        return convert(self._value(timestep, scenario_index), "m^3 s^-1", "m^3 day^-1", scale_in=1, scale_out=1000000.0)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)
        
node_IFR_bl_Hunters_Reservoir_Requirement.register()
print(" [*] node_IFR_bl_Hunters_Reservoir_Requirement successfully registered")
