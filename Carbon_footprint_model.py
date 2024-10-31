import pandas as pd
import matplotlib.pyplot as plt
import csv


class CarbonFootprintCalculator:
    def __init__(self, emission_factors_file):
        self.emission_factors = pd.read_csv(emission_factors_file)

    def calculate_travel_emissions(self, mode, distance):
        # Check the types before performing the multiplication
        print(f"Calculating travel emissions for mode: {mode}, distance: {distance} (type: {type(distance)})")

        # Ensure that emission_factor is retrieved correctly
        emission_factor = \
        self.emission_factors.loc[self.emission_factors['activity'] == mode, 'emission_factor'].values[0]

        # Ensure distance is a number before multiplication
        if isinstance(distance, (int, float)):
            return emission_factor * distance
        else:
            raise ValueError(f"Distance should be a number, got {type(distance)} instead.")

    def calculate_energy_emissions(self, energy_type, consumption):
        emission_factor = \
        self.emission_factors.loc[self.emission_factors['activity'] == energy_type, 'emission_factor'].values[0]
        return emission_factor * consumption

    def total_emissions(self, travel_data, energy_data):
        total = 0
        for mode, distance in travel_data.items():
            total += self.calculate_travel_emissions(mode, distance)

        for energy_type, consumption in energy_data.items():
            total += self.calculate_energy_emissions(energy_type, consumption)

        return total


def plot_emissions(travel_data, energy_data, total_emissions, calculator):
    labels = list(travel_data.keys()) + list(energy_data.keys())
    values = [travel_data[mode] * calculator.calculate_travel_emissions(mode, 1) for mode in travel_data]
    values += [energy_data[energy_type] * calculator.calculate_energy_emissions(energy_type, 1) for energy_type in
               energy_data]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.axhline(y=total_emissions, color='red', linestyle='--', label='Total Emissions')
    plt.title('Carbon Emissions by Activity')
    plt.xlabel('Activity')
    plt.ylabel('Emissions (kg CO2)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def save_results(travel_data, energy_data, total_emissions):
    with open('carbon_footprint_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Activity', 'Distance/Consumption', 'Emissions (kg CO2)'])

        for mode, distance in travel_data.items():
            emissions = calculator.calculate_travel_emissions(mode, distance)
            writer.writerow([mode, distance, emissions])

        for energy_type, consumption in energy_data.items():
            emissions = calculator.calculate_energy_emissions(energy_type, consumption)
            writer.writerow([energy_type, consumption, emissions])

        writer.writerow(['Total Emissions', '', total_emissions])


def compare_with_averages(total_emissions):
    average_emissions = 16.2  # Example average for an individual per year in kg CO2
    print(f"\nAverage annual emissions per person: {average_emissions:.2f} kg CO2")
    if total_emissions > average_emissions:
        print("You are above the average carbon emissions.")
    else:
        print("You are below the average carbon emissions.")


def reduction_suggestions(total_emissions):
    if total_emissions > 20:
        print("Consider reducing your carbon footprint by using public transportation or biking.")
    elif total_emissions > 10:
        print("Consider reducing meat consumption or switching to renewable energy sources.")
    else:
        print("Great job! Keep maintaining a low carbon footprint.")


def main():
    global calculator
    calculator = CarbonFootprintCalculator('emission_factors.csv')

    travel_data = {}
    print("Enter your travel data:")
    while True:
        mode = input("Enter travel mode (or type 'done' to finish): ").lower()
        if mode == 'done':
            break
        try:
            distance = float(input(f"Enter distance traveled by {mode} (in miles): "))  # Ensure this is float
            travel_data[mode] = distance
        except ValueError:
            print("Please enter a valid number for distance.")

    energy_data = {}
    print("\nEnter your energy consumption data:")
    while True:
        energy_type = input("Enter energy type (or type 'done' to finish): ").lower()
        if energy_type == 'done':
            break
        try:
            consumption = float(
                input(f"Enter consumption for {energy_type} (in kWh or therms): "))  # Ensure this is float
            energy_data[energy_type] = consumption
        except ValueError:
            print("Please enter a valid number for consumption.")

    total_emissions = calculator.total_emissions(travel_data, energy_data)
    print(f"\nTotal Carbon Emissions: {total_emissions:.2f} kg CO2")

    # Save results to a CSV file
    save_results(travel_data, energy_data, total_emissions)

    # Plot emissions
    plot_emissions(travel_data, energy_data, total_emissions, calculator)

    # Comparison and suggestions
    compare_with_averages(total_emissions)
    reduction_suggestions(total_emissions)


if __name__ == "__main__":
    main()
