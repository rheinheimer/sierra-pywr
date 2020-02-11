import pandas as pd
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from pywr.parameters._parameters cimport Parameter
# from pywr._core cimport Timestep, ScenarioIndex

cdef class CustomParameter(Parameter):
    cdef unicode res_class
    cdef unicode res_name
    cdef unicode res_name_full
    cdef unicode attr_name
    cdef int block
    cdef int month
    cdef int year
    cdef int month_offset
    cdef unicode month_suffix
    cdef unicode demand_constant_param
    cdef unicode elevation_param
    cdef int operational_water_year

    def __cinit__(self, model):
        super().__init__(model)

        self.attr_name = ''
        self.res_name = 'network'
        self.month_offset = 0

    cpdef setup(self):
        super(CustomParameter, self).setup()

        self.attr_name = ''
        self.res_name = 'network'
        self.month_offset = 0

        name_parts = self.name.split('/')
        self.res_name = name_parts[0]

        if len(name_parts) >= 2:
            self.attr_name = name_parts[1]

        if self.model.mode == 'scheduling':
            if len(name_parts) == 3:
                self.block = int(name_parts[2])
        else:
            if len(name_parts) >= 2:
                self.month_offset = int(name_parts[-1]) - 1
            if len(name_parts) == 4:
                self.block = int(name_parts[-2])

        if self.month_offset is not None:
            self.month_suffix = '/' + str(self.month_offset + 1)

        try:
            node = self.model.nodes[self.res_name + self.month_suffix]
        except:
            node = None

        if node and 'level' in node.component_attrs or self.attr_name == 'Storage Value':
            self.elevation_param = '{}/Elevation'.format(self.res_name) + self.month_suffix

    cpdef before(self):
        super(CustomParameter, self).before()
        self.datetime = self.model.timestepper.current.datetime
        if self.model.mode == 'planning':
            if self.month_offset:
                self.datetime += relativedelta(months=+self.month_offset)

            self.year = self.datetime.year
            self.month = self.datetime.month

        if 4 <= self.datetime.month <= 12:
            self.operational_water_year = self.datetime.year
        else:
            self.operational_water_year = self.datetime.year - 1

    cpdef double get(self, param, timestep=None, scenario_index=None):
        return self.model.parameters[param].value(timestep or self.model.timestep, scenario_index)

    cpdef int days_in_month(self, year=None, month=None):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        return monthrange(year, month)[1]

    cpdef list dates_in_month(self, year=None, month=None):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        return pd.date_range(pd.datetime(year, month, 1), periods=monthrange(year, month)[1]).tolist()

    cpdef double get_down_ramp_ifr(self, timestep, scenario_index, value, initial_value=None, rate=0.25):
        """

        :param timestep:
        :param scenario_index:
        :param value: cubic meters per second
        :param initial_value: cubic meters per second
        :param rate:
        :return:
        """

        cdef double Qp

        if timestep.index == 0:
            if initial_value is not None:
                Qp = initial_value
            else:
                Qp = value
        else:
            Qp = self.model.nodes[self.res_name].prev_flow[scenario_index.global_id] / 0.0864  # convert to cms
        return max(value, Qp * (1 - rate))

    cpdef double get_up_ramp_ifr(self, timestep, scenario_index, initial_value=None, rate=0.25, max_flow=None):

        cdef double Qp
        cdef double qmax

        if self.model.mode == 'scheduling':
            if initial_value is None:
                raise Exception('Initial maximum ramp up rate cannot be None')
            if timestep.index == 0:
                Qp = initial_value  # should be in cms
            else:
                Qp = self.model.nodes[self.res_name].prev_flow[scenario_index.global_id] / 0.0864  # convert to cms
            qmax = Qp * (1 + rate)
        else:
            qmax = 1e6

        if max_flow is not None:
            qmax = min(qmax, max_flow)

        return qmax

    cpdef double get_ifr_range(self, timestep, scenario_index, initial_value=None, rate=0.25, max_flow=None):

        cdef char param_name
        cdef double min_ifr
        cdef double max_ifr
        cdef double ifr_range

        param_name = self.res_name + '/Min Requirement' + self.month_suffix
        # min_ifr = self.model.parameters[param_name].get_value(scenario_index) / 0.0864  # convert to cms
        min_ifr = self.model.parameters[param_name].value(timestep, scenario_index) / 0.0864  # convert to cms
        max_ifr = self.get_up_ramp_ifr(timestep, scenario_index,
                                       initial_value=initial_value, rate=rate, max_flow=max_flow)

        ifr_range = max(max_ifr - min_ifr, 0.0)

        return ifr_range

CustomParameter.register()
