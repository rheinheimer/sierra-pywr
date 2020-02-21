from parameters import WaterLPParameter


class New_Melones_WYT(WaterLPParameter):
    """"""
    wyt = 3

    def _value(self, timestep, scenario_index):

        month = self.datetime.month
        year = self.datetime.year

        # Only calculate the index anew the 1st of Mar-Jun.
        if month < 3 or month > 6 or self.datetime.day != 1:
            return self.wyt

        # Step 1: Calculate New Melones Index (NMI), sum of Mar-Sep runoff and end-of-month storage

        # Get the Mar-Sep FNF runoff in AF
        fnf_fcst_table = self.model.tables['Full Natural Flow Forecast']
        fnf_fcst_mcm = fnf_fcst_table.at[(year, month), ("sum", "50")]

        # Estimate end-of-Feb (Mar 1) storage
        # TODO: update regression to go to Feb 28/29, not Mar 1; okay for now
        if self.model.mode == 'scheduling':
            NML_Mar1_storage_mcm = self.model.nodes["New Melones Lake"].volume(timestep, scenario_index)
        else:
            if timestep.month >= 3 and month <= 6 and year == timestep.year:
                # we should already know the end-of-Feb storage
                NML_storage = self.model.scheduling.recorders["New Melones Lake/storage"].to_dataframe()
                NML_Mar1_storage_mcm = NML_storage.to_dataframe().at['{}-02-28'.format(year), tuple(scenario_index.indices)]
            else:
                NML_initial_storage = self.model.nodes["New Melones Lake [input]"].prev_flow[scenario_index.global_id]
                regr = self.model.tables["New Melones Storage Regression"]
                NML_Mar1_storage_mcm = NML_initial_storage * regr.at[timestep.month, 'm'] + regr.at[timestep.month, 'b']

        NMI = (fnf_fcst_mcm + NML_Mar1_storage_mcm) / 1.2335  # convert to TAF

        # Step 2: Get the WYT based on typical thresholds
        thresholds = [1000, 1400, 1726, 2178, 2387, 2762]
        WYT = sum([1 for threshold in thresholds if NMI >= threshold])

        # save the WYT
        self.wyt = WYT

        return WYT

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


New_Melones_WYT.register()
print(" [*] New_Melones_WYT successfully registered")
