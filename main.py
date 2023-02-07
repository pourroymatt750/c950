# Matthew Pourroy - 001523178

import csv
import datetime
import math

from Package import Package
from hash_table import ChainingHashTable

# Hash table instance
myHash = ChainingHashTable()

# Truck class that holds parameters truck_id, package_list, start_time
class Truck:
    def __init__(self, truck_id, package_list, start_time):
        self.truck_id = truck_id
        self.package_list = package_list
        self.start_time = start_time


# ** Section  E **  ---------------------------------------------------------------------------------------------
# Creates empty list for the 3 trucks
truck1_packages = []
truck2_packages = []
truck3_packages = []
truck1 = Truck(1, truck1_packages, datetime.timedelta(hours=8))
truck2 = Truck(2, truck2_packages, datetime.timedelta(hours=9, minutes=10))
truck3 = Truck(3, truck3_packages, None)


def load_package_data(filename):
    with open(filename) as package_table:
        package_data = csv.reader(package_table, delimiter=',')
        for package in package_data:
            p_ID = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip_code = package[4]
            p_deadline = package[5]
            p_weight = package[6]
            p_note = package[7]

            # package object
            p = Package(p_ID, p_address, p_city, p_state, p_zip_code, p_deadline, p_weight, p_note)

            """
            Uses conditional statements to put packages with special requirements in the right truck. Certain packages
            are required to be on certain trucks. Packages are put into one of three nested lists: truck1_packages, 
            truck2_packages, truck3_packages.
            """

            myHash.insert(p_ID, p)

            if p_ID in [13, 14, 15, 16, 19, 20, 29, 31, 34, 37, 40]:
                truck1_packages.append(p)
                continue

            if p_ID in [1, 3, 9, 18, 28, 32, 36, 38]:
                truck2_packages.append(p)
                continue

            if p_ID == 25:
                truck3_packages.append(p)
                continue

            if len(truck1_packages) < 5:
                truck1_packages.append(p)
            elif len(truck2_packages) < 10:
                truck2_packages.append(p)
            else:
                truck3_packages.append(p)


# ** Section  F **  ---------------------------------------------------------------------------------------------
# Load packages to Hash Table
load_package_data("wgups/packages_table.csv")

distances = []
with open("wgups/distance_table.csv") as distance_table:
    distance_data = csv.reader(distance_table, delimiter=',')
    for row in distance_data:
        distances.append(row)


def get_index_for_address(address):
    row_index = -1
    for i in distances:
        row_index += 1
        if i[0] == address:
            return row_index
    return row_index


def get_distance_diff(address1, address2):
    col = get_index_for_address(address1)
    row = get_index_for_address(address2)
    if col > row:
        return float(distances[col][row + 1])
    return float(distances[row][col + 1])


# Function that will deliver all packages.
def deliver_packages(truck):
    # Keeps track of and calculates current miles driven
    total_miles = 0.0
    curr_time = truck.start_time
    print(truck.start_time)

    closest_address = "HUB"
    while len(truck.package_list) > 0:
        closest_distance = 20.0
        closest_package = None
        prev_address = closest_address
        for t in truck.package_list:
            curr_address = t.address
            # Two variables, one to hold address1(prev_address), address2(curr_address) to calculate distance
            curr_distance = get_distance_diff(prev_address, curr_address)
            if float(curr_distance) < float(closest_distance):
                closest_distance = curr_distance
                closest_package = t
                closest_address = curr_address
        # More packages delivered
        curr_time = curr_time + datetime.timedelta(hours=closest_distance / 18)
        closest_package.delivery_time = curr_time
        closest_package.departure_time = truck.start_time
        closest_package.truck_id = truck.truck_id
        print(curr_time, closest_distance, closest_package)
        truck.package_list.remove(closest_package)
        total_miles += closest_distance
    return curr_time, total_miles


truck1_completed, truck1_total_miles = deliver_packages(truck1)
truck2_completed, truck2_total_miles = deliver_packages(truck2)
truck3.start_time = truck1_completed
truck3_completed, truck3_total_miles = deliver_packages(truck3)
total_miles = truck1_total_miles + truck2_total_miles + truck3_total_miles

# Prints total miles driven
print(f"Total Miles: {math.ceil(total_miles)}")

h, m = input("Enter a time (hh:mm)").split(':')
input_time = datetime.timedelta(hours=int(h), minutes=int(m))

try:
    package_ids = [int(input("Enter a Package ID: "))]
except:
    package_ids = range(1, 41)
for package_id in package_ids:
    package = myHash.search(package_id)
    package.update_status(input_time)
    print(str(package))
