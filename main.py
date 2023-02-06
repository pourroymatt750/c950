import csv
import datetime
import math

from Package import Package
from hash_table import ChainingHashTable

# Hash table instance
myHash = ChainingHashTable()


class Truck:
    def __init__(self, truck_id, package_list, start_time):
        self.truck_id = truck_id
        self.package_list = package_list
        self.start_time = start_time


# ** Section A ** ---------------------------------------------------------------------------------------------
"""
A: The self-adjusting algorithm that is used is the "Greedy Algorithm", which is is an algorithm that,
when presented with a list of options, chooses the option that is optimal at that point in time.
The choice of option does not consider additional subsequent options, and may or may not lead to an optimal
solution (Zybooks, "Greedy algorithms, 3.3"). For my algorithm, it compares the distances of each package from 
where the truck is at the current moment and goes with whatever is the smallest distance. 
"""

# ** Section  B ** ---------------------------------------------------------------------------------------------
# B1:

# B2: The programming environment used is PyCharm Community Edition, Version: 2022.3.2, Build: 223.8617.48.

# B3: See code

"""
B4: My solution unfortunately will not be scalable due to the fact that the greedy algorithm that I used to sort which
package would be delivered next has a runtime complexity of O(N^2). The reason that the runtime is O(N^2) is because
first the function has a "while" loop the continually iterates until all the packages in the truck.package_list (list
that holds all the packages for all 3 trucks) is empty. The runtime complexity for the "while" loop which runs until "n" \
packages are delivered, which is O(N). Next, there is a nested "for" loop that iterates through each package in each 
truck and the "greedy" algorithm then compares each distances of each potential next package and goes with the smallest
distance. This works fine with an input of 40 packages, but if the input size was something much larger, say 4,000, then
the algorithm would be far to inefficient to use on a dataset of that size. 
"""

"""
B5: The software is efficient and easy to maintain due to the fact that inheritance is frequently used, which makes it
easy to make changes because all one has to do is change the code once and to changes everywhere that it is inherited. 
Some examples of inheritance in the code is creating a "Truck" object that allows the program to hold data from all 3
trucks all in one object. Another is creating only one "for" loop and iterating all the trucks through that one loop. 
"""

# B6:

# ** Section  C **  ---------------------------------------------------------------------------------------------
# C1: Matthew Pourroy - 001523178

# C2: See code
# ** Section  D **  ---------------------------------------------------------------------------------------------
"""
D1: A hash table is a self-adjusting data structure that can be used to store package data. This data structure
    accounts for the relationship between the data points I am storing by assigning a "hash", or unique key, that
    allows the data entry to be stored in the hash table, and it uses a method called "chaining" that prevents any data
    entry from accidentally repeating the same unique key.
"""

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

            if p_ID == 13 or p_ID == 14 or p_ID == 15 or p_ID == 16 or p_ID == 20 or p_ID == 29 or p_ID == 31 or p_ID == 34 or p_ID == 37 or p_ID == 40:
                truck1_packages.append(p)

            if p_ID == 1 or p_ID == 3 or p_ID == 18 or p_ID == 25 or p_ID == 28 or p_ID == 32 or p_ID == 36 or p_ID == 38:
                truck2_packages.append(p)

            if p_ID == 9:
                truck3_packages.append(p)

            # insert it into the hash table
            myHash.insert(p_ID, p)


# ** Section  F **  ---------------------------------------------------------------------------------------------
# Load packages to Hash Table
load_package_data("wgups/packages_table.csv")

for i in truck3_packages:
    # print(i)
    pass
# print(len(truck1_packages) + len(truck2_packages) + len(truck3_packages))
# print(len(truck2_packages))

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


# deliver_packages(truck, total_miles=0)
def deliver_packages(truck):
    # Keeps track of and calculates current miles driven
    total_miles = 0.0
    curr_time = truck.start_time
    print(truck.start_time)

    while len(truck.package_list) > 0:
        closest_distance = 20.0
        closest_package = None
        closest_address = "HUB"
        prev_address = closest_address
        print(prev_address)
        for t in truck.package_list:
            # Converts object to string
            str_t = str(t)
            # Splits string in order to obtain just the address
            split_t = str_t.split(', ')
            # Gets just the address from the string
            curr_address = split_t[1]
            # Two variables, one to hold address1(prev_address), address2(curr_address) to calculate distance
            curr_distance = get_distance_diff(prev_address, curr_address)
            if float(curr_distance) < float(closest_distance):
                closest_distance = curr_distance
                closest_package = t
                closest_address = curr_address
        print(closest_address)
        # More packages delivered
        curr_time = curr_time + datetime.timedelta(hours=closest_distance / 18)
        closest_package.delivery_time = curr_time
        print(curr_time, closest_distance, closest_package)
        truck.package_list.remove(closest_package)
        total_miles += closest_distance
    return curr_time, total_miles


truck1_completed, truck1_total_miles = deliver_packages(truck1)
# truck2_completed, truck2_total_miles = deliver_packages(truck2)
# truck3.start_time = truck1_completed
# truck3_completed, truck3_total_miles = deliver_packages(truck3)
# total_miles = truck1_total_miles + truck2_total_miles + truck3_total_miles
total_miles = truck1_total_miles

# Prints total miles driven
print(f"Total Miles: {math.ceil(total_miles)}")

# Fetch data from Hash Table
# for i in range(1, 41):
#     print("Package: {}".format(myHash.search(i)))

# ** Section  G **  ---------------------------------------------------------------------------------------------
# G1:

# G2:

# G3:

# ** Section H **  ---------------------------------------------------------------------------------------------

# ** Section I **  ---------------------------------------------------------------------------------------------
# I1:

# I2:

# I3:

# I3A:

# ** Section J **  ---------------------------------------------------------------------------------------------
# J:

# ** Section K **  ---------------------------------------------------------------------------------------------
# K1A:

# K1B:

# K1C:

# K2:

# K2A:

# ** Section L **  ---------------------------------------------------------------------------------------------
# L:
