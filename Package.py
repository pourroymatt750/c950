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

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip_code,
                                                       self.deadline, self.delivery_time, self.weight,
                                                       self.delivery_status)
