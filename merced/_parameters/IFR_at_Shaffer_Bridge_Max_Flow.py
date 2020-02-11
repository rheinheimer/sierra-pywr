from parameters import CustomParameter


class IFR_at_Shaffer_Bridge_Max_Flow(CustomParameter):
    """
    This policy calculates instream flow requirements in the Merced River below the Merced Falls powerhouse.
    """

    def _value(self, timestep, scenario_index):
        ifr_val = 250 / 35.31  # cfs to cms (16.5 cfs)
        ifr_range = self.get_ifr_range(timestep, scenario_index, initial_value=ifr_val, rate=0.25)

        return ifr_range * 0.0864

    def value(self, timestep, scenario_index):
        try:
            return self._value(timestep, scenario_index)
        except Exception as err:
            print('\nERROR for parameter {}'.format(self.name))
            print('File where error occurred: {}'.format(__file__))
            print(err)

    @classmethod
    def load(cls, model, data):
        return cls(model, **data)


IFR_at_Shaffer_Bridge_Max_Flow.register()
print(" [*] IFR_at_Shaffer_Bridge_Max_Flow successfully registered")
