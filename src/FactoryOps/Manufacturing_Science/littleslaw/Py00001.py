class LittlesLaw:
    """
    A class to calculate factory dynamics using Little's Law.
    Includes strict input validation to ensure physical feasibility.
    """

    @staticmethod
    def _validate_input(value, name, allow_zero=True):
        """
        Internal helper to validate that inputs are numbers and non-negative.
        
        Args:
            value: The input to check.
            name (str): The name of the variable for error messages.
            allow_zero (bool): If False, raises error for 0 values (for denominators).
        """
        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid type for '{name}'. Expected int or float, got {type(value).__name__}.")
        
        if value < 0:
            raise ValueError(f"Invalid value for '{name}'. Value cannot be negative ({value}).")
            
        if not allow_zero and value == 0:
            raise ValueError(f"Invalid value for '{name}'. Value cannot be zero (dividing by zero).")

    @staticmethod
    def calculate_wip(throughput, cycle_time):
        """
        Calculates Expected Work In Process (WIP).
        Formula: WIP = TH * CT
        """
        LittlesLaw._validate_input(throughput, "throughput")
        LittlesLaw._validate_input(cycle_time, "cycle_time")
        
        return throughput * cycle_time

    @staticmethod
    def calculate_cycle_time(wip, throughput):
        """
        Calculates Cycle Time (CT).
        Formula: CT = WIP / TH
        """
        LittlesLaw._validate_input(wip, "wip")
        # Throughput is the denominator, so it cannot be zero
        LittlesLaw._validate_input(throughput, "throughput", allow_zero=False)
        
        return wip / throughput

    @staticmethod
    def calculate_throughput(wip, cycle_time):
        """
        Calculates Throughput (TH).
        Formula: TH = WIP / CT
        """
        LittlesLaw._validate_input(wip, "wip")
        # Cycle time is the denominator, so it cannot be zero
        LittlesLaw._validate_input(cycle_time, "cycle_time", allow_zero=False)
        
        return wip / cycle_time

    @staticmethod
    def calculate_station_utilization(station_throughput, station_cycle_time, number_of_machines):
        """
        Calculates Station Utilization.
        Formula: (TH * CT) / Machines
        """
        LittlesLaw._validate_input(station_throughput, "station_throughput")
        LittlesLaw._validate_input(station_cycle_time, "station_cycle_time")
        # Machines must be a positive integer
        if not isinstance(number_of_machines, int) or number_of_machines <= 0:
            raise ValueError(f"Number of machines must be a positive integer. Got {number_of_machines}.")
        
        # Step 1: Calculate expected WIP at the station
        station_wip = station_throughput * station_cycle_time
        
        # Step 2: Calculate utilization
        utilization = station_wip / number_of_machines
        
        if utilization > 1.0:
            # While mathematically possible to return > 1, practically this means the station is unstable
            # We return it but warn if using a logger, here we simply compute the value.
            pass

        return {
            "station_wip": station_wip,
            "utilization": utilization,
            "utilization_pct": utilization * 100
        }

    @staticmethod
    def calculate_inventory_turns(throughput, wip, fgi=0):
        """
        Calculates Inventory Turns.
        Formula: TH / (WIP + FGI)
        """
        LittlesLaw._validate_input(throughput, "throughput")
        LittlesLaw._validate_input(wip, "wip")
        LittlesLaw._validate_input(fgi, "fgi")
        
        total_inventory = wip + fgi
        
        if total_inventory == 0:
            raise ValueError("Total inventory (WIP + FGI) cannot be zero when calculating turns.")
        
        return throughput / total_inventory

    @staticmethod
    def calculate_planned_inventory(throughput, planned_days):
        """
        Calculates required Finished Goods Inventory (FGI).
        Formula: FGI = n * TH
        """
        LittlesLaw._validate_input(throughput, "throughput")
        LittlesLaw._validate_input(planned_days, "planned_days")
        
        return planned_days * throughput

    @staticmethod
    def financial_cycle_time(wip_value, cost_of_goods_sold):
        """
        Calculates Cycle Time using financial units.
        Formula: CT = WIP($) / COGS($)
        """
        LittlesLaw._validate_input(wip_value, "wip_value")
        LittlesLaw._validate_input(cost_of_goods_sold, "cost_of_goods_sold", allow_zero=False)
        
        return wip_value / cost_of_goods_sold