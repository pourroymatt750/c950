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
# Creates instance of the 3 truck objects: Truck 1, Truck 2, Truck 3
truck1 = Truck(1, truck1_packages, datetime.timedelta(hours=8, minutes=10))
truck2 = Truck(2, truck2_packages, datetime.timedelta(hours=9, minutes=10))
truck3 = Truck(3, truck3_packages, None)


# Loads data from packages_table.csv, space-time complexity is O(N)
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

            # package object
            p = Package(p_ID, p_address, p_city, p_state, p_zip_code, p_deadline, p_weight)

            # Insert statement to insert packages into the "myHash" hash table
            myHash.insert(p_ID, p)

            """
            Uses conditional statements to put packages with special requirements in the right truck. Certain packages
            are required to be on certain trucks. Packages are put into one of three nested lists: truck1_packages, 
            truck2_packages, truck3_packages. After packages with special requests are inserted into the proper trucks,
            the rest of the packages are inserted into the 3 trucks at random as long any given truck does NOT have more
            than 16 packages. 
            """

            if p_ID in [13, 14, 15, 16, 19, 20, 29, 31, 34, 37, 40]:
                truck1_packages.append(p)
                continue

            if p_ID in [1, 3, 6, 18, 28, 30, 32, 36, 38]:
                truck2_packages.append(p)
                continue

            if p_ID == 9 or p_ID == 25:
                truck3_packages.append(p)
                continue

            if len(truck1_packages) < 5:
                truck1_packages.append(p)
            elif len(truck2_packages) < 9:
                truck2_packages.append(p)
            else:
                truck3_packages.append(p)


# ** Section  F **  ---------------------------------------------------------------------------------------------
# Load packages to Hash Table
load_package_data("wgups/packages_table.csv")

# Creates a list to store the data from the distance_table.csv
distances = []
with open("wgups/distance_table.csv") as distance_table:
    distance_data = csv.reader(distance_table, delimiter=',')
    for row in distance_data:
        distances.append(row)


print(len(truck1_packages))
print(len(truck2_packages))
print(len(truck3_packages))

# Function to get index of the given address to be able to find it in the distance_table.csv
def get_index_for_address(address):
    row_index = -1
    for i in distances:
        row_index += 1
        if i[0] == address:
            return row_index
    return row_index


# Function that calculates the distance between two addresses and returns a float
def get_distance_diff(address1, address2):
    col = get_index_for_address(address1)
    row = get_index_for_address(address2)
    if col > row:
        return float(distances[col][row + 1])
    return float(distances[row][col + 1])


"""
"deliver_packages(truck)" is a function that will deliver all packages and has a O(N^2) space-time complexity because 
first the function has a "while" loop the continually iterates until all the packages in the truck.package_list
(list that holds all the packages for all 3 trucks) is empty. The space-time complexity for the "while" loop which runs 
until "n" packages are delivered, which is O(N). Next, there is a nested "for" loop that iterates through each package 
in each truck and the "greedy" algorithm then compares each distances of each potential next package and goes with the 
smallest distance.
"""


def deliver_packages(truck):
    # Keeps track of and calculates current miles driven
    total_miles = 0.0
    # Current time of the truck
    curr_time = truck.start_time

    # print(f"Truck {truck.truck_id} Departure: {curr_time}")

    # Initializes the closest address to "HUB" because that's the first place a truck starts
    closest_address = "HUB"
    # "while" loop, O(N), iterates until there are no more packages left in any of the trucks
    while len(truck.package_list) > 0:
        closest_distance = 20.0
        closest_package = None
        prev_address = closest_address
        for t in truck.package_list:
            curr_address = t.address
            # Two variables, one to hold address1(prev_address), address2(curr_address) to calculate distance
            curr_distance = get_distance_diff(prev_address, curr_address)
            if float(curr_distance) < float(closest_distance):
                """
                Current distance is less than the closest distance, so current distance becomes the new closest 
                distance. Closest package becomes the package that had the smallest distance. 
                """
                closest_distance = curr_distance
                closest_package = t
                closest_address = curr_address
        # More packages delivered
        """
        More packages delivered. Current time is calculated by taking the closest distance because that is the path the
        truck will follow, and it divides it by 18 because the trucks move at 18 mph. The package departure time and 
        Truck ID are recorded to make the list of packages easier to read when printed. 
        """
        curr_time = curr_time + datetime.timedelta(hours=closest_distance / 18)
        closest_package.delivery_time = curr_time
        closest_package.delivery_status = 'Delivered'
        closest_package.departure_time = truck.start_time
        closest_package.truck_id = truck.truck_id
        # Removes a package from the truck once it's delivered
        truck.package_list.remove(closest_package)
        # Adds the closest distance to total miles
        total_miles += closest_distance
    return curr_time, total_miles


"""
Calls the truck with all 3 truck objects and waits to call Truck 3 until Truck 1 finishes due to the fact that there is 
only 2 drivers so Truck 3 can't leave until the driver from Truck 1 and takeover and drive Truck 3. 
"""
truck1_completed, truck1_total_miles = deliver_packages(truck1)
truck2_completed, truck2_total_miles = deliver_packages(truck2)
truck3.start_time = truck1_completed
truck3_completed, truck3_total_miles = deliver_packages(truck3)
total_miles = truck1_total_miles + truck2_total_miles + truck3_total_miles

print("1: All package information")
print("2: Enter a time to see all packages at that time")
print("3: Enter a Time and Package ID to see information at that time")

choice = input("Select 1-3: ")

if choice == '1':
    package_ids = range(1, 41)
    for package_id in package_ids:
        package = myHash.search(package_id)
        print(str(package))
    # Prints total miles driven
    print(f"Total Miles: {math.ceil(total_miles)}")
if choice == '2':
    h, m = input("Enter a start time (hh:mm)").split(':')
    input_time = datetime.timedelta(hours=int(h), minutes=int(m))
    package_ids = range(1, 41)

    for package_id in package_ids:
        package = myHash.search(package_id)
        package.update_status(input_time)
        if input_time < package.departure_time:
            print("%s, %s, %s, %s, %s, %s, Truck %s, Departure Time: %s, Delivery Time:, Delivery Status: HUB, "
                  "Deadline: %s" % (
                      package.ID, package.address, package.city, package.state, package.zip_code, package.weight,
                      package.truck_id, package.departure_time, package.deadline))
        elif package.departure_time < input_time < package.delivery_time:
            print("%s, %s, %s, %s, %s, %s, Truck %s, Departure Time: %s, Delivery Time:, Delivery Status: En Route, "
                  "Deadline: %s" % (
                      package.ID, package.address, package.city, package.state, package.zip_code, package.weight,
                      package.truck_id, package.departure_time, package.deadline))
        else:
            print(package)
if choice == '3':
    h, m = input("Enter a start time (hh:mm)").split(':')
    input_time = datetime.timedelta(hours=int(h), minutes=int(m))

    """
    Try: Looks for a Package ID that entered, if it finds it, it returns the Package with that ID, 
    Except: otherwise returns all packages within time frame entered along with total miles traveled by all the trucks. 
    """
    try:
        package_ids = [int(input("Enter a Package ID: "))]
    except:
        package_ids = range(1, 41)
        print(f"Truck 1 Departure: {truck1.start_time}")
        print(f"Truck 2 Departure: {truck2.start_time}")
        print(f"Truck 3 Departure: {truck3.start_time}")
    for package_id in package_ids:
        package = myHash.search(package_id)
        package.update_status(input_time)
        print(str(package))

