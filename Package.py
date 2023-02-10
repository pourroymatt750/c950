# Package class that initializes all associated variables
class Package:
    def __init__(self, ID, address, city, state, zip_code, deadline, weight, delivery_status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = delivery_status

        self.delivery_time = None
        self.departure_time = None
        self.truck_id = None

    def __str__(self):
        # return "%s, %s, %s, %s, %s, %s, %s, %s, %s Truck ID: %s" % (
        #     self.ID, self.address, self.city, self.state, self.zip_code,
        #     self.deadline, self.delivery_time, self.weight,
        #     self.delivery_status, self.truck_id)

        return "%s, %s, %s, %s, %s, %s, Truck ID: %s, Departure Time: %s, %s , Deadline: %s" % (
            self.ID, self.address, self.city, self.state, self.zip_code, self.weight,
            self.truck_id, self.departure_time, self.delivery_status, self.deadline)

    # Updates delivery time based on where truck is
    def update_status(self, input_time):
        if self.delivery_time is None:
            self.delivery_status = "HUB"
        elif input_time < self.delivery_time:
            self.delivery_status = "En Route"
        else:
            self.delivery_status = "Delivered %s" % self.delivery_time
