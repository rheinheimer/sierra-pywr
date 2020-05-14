from parameters import MinFlowParameter

from utilities.converter import convert

class IFR_bl_Balsam_Forebay_Min_Flow(MinFlowParameter):
    """"""

    def _value(self, timestep, scenario_index):

        if 6 <= self.datetime.month <= 9:  # Jun - Sep
            ifr_cfs = 1
        else:
            ifr_cfs = 0.5
        ifr_cfs += 0.1  # add factor of safety

        if self.model.mode == "planning":
            ifr_cfs *= self.days_in_month
        
        return ifr_cfs / 35.315
        
    def value(self, *args, **kwargs):
        try:
            ifr = self.get_ifr(*args, **kwargs)
            if ifr is not None:
                return ifr
            else:
                ifr = self._value(*args, **kwargs)
                return ifr # unit is already mcm
        except Exception as err:
            print('\nERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)

    @classmethod
    def load(cls, model, data):
        try:
            return cls(model, **data)
        except Exception as err:
            print('File where error occurred: {}'.format(__file__))
            print(err)
            raise
        
IFR_bl_Balsam_Forebay_Min_Flow.register()
