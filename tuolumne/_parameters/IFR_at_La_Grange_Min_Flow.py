import numpy as np
from parameters import MinFlowParameter

from utilities.converter import convert


class IFR_at_La_Grange_Min_Flow(MinFlowParameter):
    """"""

    def _value(self, timestep, scenario_index):

        month_day = (timestep.month, timestep.day)

        if (4, 1) <= month_day <= (4, 15):
            return self.model.nodes["IFR at La Grange"].prev_flow[scenario_index.global_id] / 0.0864  # convert to cms

        SJVI = self.get("San Joaquin Valley WYI", timestep, scenario_index)
        schedule = self.model.tables["IFR at La Grange/IFR Schedule"]
        thresholds = [1.500, 2.000, 2.200, 2.400, 2.700, 3.100]
        lookup_col = sum([1 for t in thresholds if SJVI >= t]) + 1  # there is also a "days" column

        should_interpolate = 1.5 < SJVI < 3.1 and SJVI not in thresholds

        if (10, 1) <= month_day <= (10, 15):
            lookup_row = 0
        elif month_day >= (10, 16) or month_day <= (5, 31):
            lookup_row = 2
        else:
            lookup_row = 4

        base_ifr_cfs = schedule.iat[lookup_row, lookup_col]

        # For the outmigration pulse flow, divide equally across April and June for now
        outmigration_season = (4, 15) < month_day <= (5, 15)
        outmigration_pulse_flow_af = 0
        if outmigration_season:
            outmigration_pulse_flow_af = schedule.iat[3, lookup_col]

        # Interpolate between WYT thresholds
        if should_interpolate:
            low_threshold = thresholds[lookup_col - 2]
            high_threshold = thresholds[lookup_col - 1]
            xp = [low_threshold, high_threshold]

            base_ifr_cfs_next = schedule.iat[lookup_row, lookup_col + 1]
            base_ifr_fp = [base_ifr_cfs, base_ifr_cfs_next]
            base_ifr_cfs = np.interp([SJVI], xp, base_ifr_fp)[0]

            if outmigration_season:
                outmigration_pulse_flow_af_next = schedule.iat[3, lookup_col + 1]
                outmigration_fp = [outmigration_pulse_flow_af, outmigration_pulse_flow_af_next]
                outmigration_pulse_flow_af = np.interp([SJVI], xp, outmigration_fp)[0]

        outmigration_pulse_flow_cms = outmigration_pulse_flow_af / 1000 * 1.2335 / 0.0864 / 30  # divide into 30 days
        ifr_cms = max(base_ifr_cfs / 35.31, outmigration_pulse_flow_cms, 100 / 35.31)

        return ifr_cms

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


IFR_at_La_Grange_Min_Flow.register()
