#!/usr/bin/env python3
"""
EU ETS and FuelEU Maritime Calculator Input Handler
Python 3.13 Compatible

This module provides a comprehensive data collection system for maritime emissions
calculations under EU ETS and FuelEU Maritime regulations.

Usage:
    python eu_ets_fueleu_calculator.py

Author: Generated for Maritime Emissions Compliance
Date: August 2025
"""

from datetime import datetime
from typing import Dict, Any, Union, Optional
import re
import json
import csv

class EUETSFuelEUCalculator:
    """
    EU ETS and FuelEU Maritime Calculator Input Handler
    Handles data collection for maritime emissions calculations
    """
    
    def __init__(self):
        self.voyage_data = {}
        self.fuel_types = [
            "LFO", "HFO", "MGO",
            "LPG(P)", "LPG(B)", "LNG Otto MS", "LNG Otto SS", 
            "LNG Diesel SS", "LNG LBSI", "BioFuel 1", "BioFuel 2", "BioFuel 3"
        ]
        self.engine_types = ["ME", "AE", "Others", "Off-hire"]
    
    def validate_imo_number(self, imo: str) -> bool:
        """Validate IMO number format (7 digits)"""
        return bool(re.match(r'^\d{7}$', imo))
    
    def validate_date(self, date_str: str, format_type: str = "dd/mm/yyyy") -> bool:
        """Validate date format"""
        try:
            if format_type == "dd/mm/yyyy":
                datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def validate_time(self, time_str: str) -> bool:
        """Validate time format (hh:mm)"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def validate_percentage(self, value: str) -> bool:
        """Validate percentage (0, 50, or 100)"""
        try:
            val = float(value)
            return val in [0, 50, 100]
        except ValueError:
            return False
    
    def get_input_with_validation(self, prompt: str, validation_func=None, required=True) -> str:
        """Get input with optional validation"""
        while True:
            value = input(f"{prompt}: ").strip()
            
            if not required and not value:
                return value
            
            if required and not value:
                print("This field is required. Please enter a value.")
                continue
            
            if validation_func and not validation_func(value):
                print("Invalid input. Please try again.")
                continue
            
            return value
    
    def get_float_input(self, prompt: str, required=True) -> float:
        """Get float input with validation"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not required and not value:
                    return 0.0
                return float(value)
            except ValueError:
                print("Please enter a valid number.")
    
    def get_choice_input(self, prompt: str, choices: list, required=True) -> str:
        """Get input from predefined choices"""
        choices_str = "/".join(choices)
        while True:
            value = input(f"{prompt} ({choices_str}): ").strip()
            
            if not required and not value:
                return value
            
            if value in choices:
                return value
            
            print(f"Please choose from: {choices_str}")
    
    def collect_basic_voyage_info(self):
        """Collect basic voyage information"""
        print("=== BASIC VOYAGE INFORMATION ===")
        
        self.voyage_data['imo_number'] = self.get_input_with_validation(
            "IMO No", self.validate_imo_number
        )
        
        self.voyage_data['vessel'] = self.get_input_with_validation("Vessel")
        
        self.voyage_data['application_year'] = self.get_input_with_validation("Application Year")
        
        self.voyage_data['emission_statement_number'] = self.get_input_with_validation(
            "Emission Statement Number"
        )
        
        self.voyage_data['voyage_number'] = self.get_input_with_validation("Voyage no.")
        
        self.voyage_data['condition'] = self.get_choice_input(
            "Condition", ["Laden", "Ballast"]
        )
    
    def collect_route_info(self):
        """Collect route information"""
        print("\\n=== ROUTE INFORMATION ===")
        
        self.voyage_data['from_port'] = self.get_input_with_validation("From (port)")
        self.voyage_data['from_port_eu_status'] = self.get_choice_input(
            "From port EU/Non-EU", ["EU", "Non-EU"]
        )
        
        self.voyage_data['to_port'] = self.get_input_with_validation("To (port)")
        self.voyage_data['to_port_eu_status'] = self.get_choice_input(
            "To port EU/Non-EU", ["EU", "Non-EU"]
        )
        
        self.voyage_data['eu_ets_voyage_percentage'] = self.get_input_with_validation(
            "Applicable EU ETS Voyage Type % (0-50-100)", self.validate_percentage
        )
        
        self.voyage_data['fueleu_voyage_percentage'] = self.get_input_with_validation(
            "Applicable FuelEU Voyage Type % (0-50-100)", self.validate_percentage
        )
    
    def collect_sailing_schedule(self):
        """Collect sailing schedule information"""
        print("\\n=== SAILING SCHEDULE ===")
        
        self.voyage_data['departure_date'] = self.get_input_with_validation(
            "Departure Date from last berth/(anchor for STS) (UTC) (dd/mm/yyyy)", 
            self.validate_date
        )
        
        self.voyage_data['departure_time'] = self.get_input_with_validation(
            "Departure Time from last berth/(anchor for STS) (UTC) (hh:mm)", 
            self.validate_time
        )
        
        self.voyage_data['arrival_date'] = self.get_input_with_validation(
            "Arrival Date at first berth/(anchor for STS) (UTC) (dd/mm/yyyy)", 
            self.validate_date
        )
        
        self.voyage_data['arrival_time'] = self.get_input_with_validation(
            "Arrival time at first berth/(anchor for STS) (UTC) (hh:mm)", 
            self.validate_time
        )
        
        self.voyage_data['distance_nm'] = self.get_float_input("Distance (Nm)")
    
    def collect_sailing_fuel_consumption(self):
        """Collect fuel consumption data for sailing"""
        print("\\n=== SAILING FUEL CONSUMPTION ===")
        
        self.voyage_data['sailing_fuel'] = {}
        
        for fuel_type in self.fuel_types:
            print(f"\\n--- {fuel_type} ---")
            fuel_data = {}
            
            for engine_type in self.engine_types:
                fuel_data[engine_type] = self.get_float_input(
                    f"{engine_type} {fuel_type} Sailing", required=False
                )
            
            self.voyage_data['sailing_fuel'][fuel_type] = fuel_data
    
    def collect_port_info(self):
        """Collect port information"""
        print("\\n=== PORT INFORMATION ===")
        
        self.voyage_data['arrival_port'] = self.get_input_with_validation("Arrival port")
        
        self.voyage_data['port_activity'] = self.get_choice_input(
            "Port Activity", ["Load", "Discharge", "Other"]
        )
        
        self.voyage_data['arrival_port_eu_status'] = self.get_choice_input(
            "Arrival Port EU or Non-EU", ["EU", "Non-EU"]
        )
        
        self.voyage_data['port_arrival_date'] = self.get_input_with_validation(
            "Arrival Date at first berth/(anchor for STS) (UTC) (dd/mm/yyyy)", 
            self.validate_date
        )
        
        self.voyage_data['port_arrival_time'] = self.get_input_with_validation(
            "Arrival time at first berth/(anchor for STS) (UTC) (hh:mm)", 
            self.validate_time
        )
        
        self.voyage_data['port_departure_date'] = self.get_input_with_validation(
            "Departure Date from last berth/(anchor for STS) (UTC) (dd/mm/yyyy)", 
            self.validate_date
        )
        
        self.voyage_data['port_departure_time'] = self.get_input_with_validation(
            "Departure time from last berth/(anchor for STS) (UTC) (hh:mm)", 
            self.validate_time
        )
        
        self.voyage_data['port_limits'] = self.get_choice_input(
            "Within port limits or outside port limits", 
            ["Within port limits", "Outside port limits"]
        )
        
        self.voyage_data['total_stay_hours'] = self.get_float_input("Total Stay (hrs)")
    
    def collect_port_fuel_consumption(self):
        """Collect fuel consumption data for port operations"""
        print("\\n=== PORT FUEL CONSUMPTION ===")
        
        self.voyage_data['port_fuel'] = {}
        
        for fuel_type in self.fuel_types:
            print(f"\\n--- {fuel_type} ---")
            fuel_data = {}
            
            for engine_type in self.engine_types:
                fuel_data[engine_type] = self.get_float_input(
                    f"{engine_type} {fuel_type} Port", required=False
                )
            
            self.voyage_data['port_fuel'][fuel_type] = fuel_data
    
    def collect_all_data(self) -> Dict[str, Any]:
        """Collect all required data for EU ETS and FuelEU calculations"""
        print("EU ETS and FuelEU Maritime Calculator")
        print("=====================================")
        
        self.collect_basic_voyage_info()
        self.collect_route_info()
        self.collect_sailing_schedule()
        self.collect_sailing_fuel_consumption()
        self.collect_port_info()
        self.collect_port_fuel_consumption()
        
        return self.voyage_data
    
    def display_summary(self):
        """Display a summary of collected data"""
        print("\\n" + "="*50)
        print("DATA COLLECTION SUMMARY")
        print("="*50)
        
        print(f"Vessel: {self.voyage_data.get('vessel', 'N/A')}")
        print(f"IMO Number: {self.voyage_data.get('imo_number', 'N/A')}")
        print(f"Voyage: {self.voyage_data.get('voyage_number', 'N/A')}")
        print(f"Route: {self.voyage_data.get('from_port', 'N/A')} → {self.voyage_data.get('to_port', 'N/A')}")
        print(f"Distance: {self.voyage_data.get('distance_nm', 0)} Nm")
        print(f"EU ETS Applicable %: {self.voyage_data.get('eu_ets_voyage_percentage', 0)}%")
        print(f"FuelEU Applicable %: {self.voyage_data.get('fueleu_voyage_percentage', 0)}%")
        
        print("\\nData collection completed successfully!")
    
    def save_to_json(self, filename: str = None):
        """Save collected data to JSON file"""
        if not filename:
            filename = f"voyage_data_{self.voyage_data.get('voyage_number', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.voyage_data, f, indent=2, default=str)
            
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
    
    def save_to_csv(self, filename: str = None):
        """Save collected data to CSV file (flattened structure)"""
        if not filename:
            filename = f"voyage_data_{self.voyage_data.get('voyage_number', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            flattened_data = self._flatten_dict(self.voyage_data)
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Field', 'Value'])
                for key, value in flattened_data.items():
                    writer.writerow([key, value])
            
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving CSV file: {e}")
    
    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        """Flatten nested dictionary for CSV export"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def load_from_json(self, filename: str) -> bool:
        """Load data from JSON file"""
        try:
            with open(filename, 'r') as f:
                self.voyage_data = json.load(f)
            print(f"Data loaded from {filename}")
            return True
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return False
    
    def get_fuel_summary(self) -> Dict[str, float]:
        """Get summary of total fuel consumption by type"""
        summary = {}
        
        # Sailing fuel
        if 'sailing_fuel' in self.voyage_data:
            for fuel_type, engines in self.voyage_data['sailing_fuel'].items():
                total = sum(engines.values())
                summary[f"{fuel_type}_sailing"] = total
        
        # Port fuel
        if 'port_fuel' in self.voyage_data:
            for fuel_type, engines in self.voyage_data['port_fuel'].items():
                total = sum(engines.values())
                summary[f"{fuel_type}_port"] = total
        
        return summary
    
    def validate_data_completeness(self) -> Dict[str, list]:
        """Validate that all required data is present"""
        required_fields = [
            'imo_number', 'vessel', 'application_year', 'voyage_number',
            'from_port', 'to_port', 'departure_date', 'arrival_date', 'distance_nm'
        ]
        
        missing_fields = []
        present_fields = []
        
        for field in required_fields:
            if field not in self.voyage_data or not self.voyage_data[field]:
                missing_fields.append(field)
            else:
                present_fields.append(field)
        
        return {
            'missing': missing_fields,
            'present': present_fields,
            'complete': len(missing_fields) == 0
        }

# Batch processing functionality
class BatchProcessor:
    """Handle multiple voyage calculations"""
    
    def __init__(self):
        self.voyages = []
    
    def add_voyage(self, voyage_data: Dict[str, Any]):
        """Add a voyage to the batch"""
        self.voyages.append(voyage_data)
    
    def export_batch_csv(self, filename: str = None):
        """Export all voyages to a single CSV file"""
        if not filename:
            filename = f"batch_voyages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not self.voyages:
            print("No voyages to export")
            return
        
        try:
            # Flatten all voyage data
            flattened_voyages = []
            for voyage in self.voyages:
                calc = EUETSFuelEUCalculator()
                calc.voyage_data = voyage
                flattened = calc._flatten_dict(voyage)
                flattened_voyages.append(flattened)
            
            # Get all unique keys
            all_keys = set()
            for voyage in flattened_voyages:
                all_keys.update(voyage.keys())
            
            # Write CSV
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                writer.writeheader()
                writer.writerows(flattened_voyages)
            
            print(f"Batch data exported to {filename}")
        except Exception as e:
            print(f"Error exporting batch CSV: {e}")

# Example usage and testing functions
def demo_data() -> Dict[str, Any]:
    """Generate demo data for testing"""
    return {
        'imo_number': '1234567',
        'vessel': 'MV Test Ship',
        'application_year': '2025',
        'emission_statement_number': 'ES001',
        'voyage_number': 'V001',
        'condition': 'Laden',
        'from_port': 'Rotterdam',
        'from_port_eu_status': 'EU',
        'to_port': 'Singapore',
        'to_port_eu_status': 'Non-EU',
        'eu_ets_voyage_percentage': '50',
        'fueleu_voyage_percentage': '50',
        'departure_date': '01/01/2025',
        'departure_time': '08:00',
        'arrival_date': '15/01/2025',
        'arrival_time': '18:00',
        'distance_nm': 8500.0,
        'sailing_fuel': {
            'VLSFO LFO (<80Cst)': {'ME': 150.0, 'AE': 25.0, 'Others': 5.0, 'Off-hire': 0.0}
        },
        'port_fuel': {
            'VLSFO LFO (<80Cst)': {'ME': 10.0, 'AE': 15.0, 'Others': 2.0, 'Off-hire': 0.0}
        }
    }

def main():
    """Main function to run the calculator"""
    calculator = EUETSFuelEUCalculator()
    
    print("Choose an option:")
    print("1. Enter new voyage data")
    print("2. Load demo data")
    print("3. Load from JSON file")
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            # Collect all data
            voyage_data = calculator.collect_all_data()
        elif choice == '2':
            # Load demo data
            calculator.voyage_data = demo_data()
            voyage_data = calculator.voyage_data
            print("Demo data loaded successfully!")
        elif choice == '3':
            # Load from file
            filename = input("Enter JSON filename: ").strip()
            if calculator.load_from_json(filename):
                voyage_data = calculator.voyage_data
            else:
                return None
        else:
            print("Invalid choice")
            return None
        
        # Display summary
        calculator.display_summary()
        
        # Validate data
        validation = calculator.validate_data_completeness()
        if not validation['complete']:
            print(f"\\nWarning: Missing required fields: {validation['missing']}")
        
        # Show fuel summary
        fuel_summary = calculator.get_fuel_summary()
        if fuel_summary:
            print("\\nFuel Consumption Summary:")
            for fuel, amount in fuel_summary.items():
                if amount > 0:
                    print(f"  {fuel}: {amount:.2f} MT")
        
        # Save options
        print("\\nSave options:")
        print("1. Save to JSON")
        print("2. Save to CSV")
        print("3. Both")
        print("4. Skip saving")
        
        save_choice = input("Enter choice (1-4): ").strip()
        
        if save_choice in ['1', '3']:
            calculator.save_to_json()
        if save_choice in ['2', '3']:
            calculator.save_to_csv()
        
        return voyage_data
        
    except KeyboardInterrupt:
        print("\\n\\nData collection interrupted by user.")
        return None
    except Exception as e:
        print(f"\\nAn error occurred: {e}")
        return None

if __name__ == "__main__":
    collected_data = main()
