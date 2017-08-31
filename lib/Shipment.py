from lib import OrderedEnum


class ShipmentDay(OrderedEnum.OrderedEnum):
    M = 1
    T = 2
    W = 3
    R = 4
    F = 5


class Shipment:
    def __init__(self, shipment_id, source, dest, ship_date):
        self.shipment_id = int(shipment_id)
        self.source = source
        self.dest = dest
        self.date = self.get_date(ship_date)

    '''private'''
    def get_date(self,ship_date):
        if ship_date == "M":
            return ShipmentDay.M
        elif ship_date == "T":
            return ShipmentDay.T
        elif ship_date == "W":
            return ShipmentDay.W
        elif ship_date == "R":
            return ShipmentDay.R
        elif ship_date == "F":
            return ShipmentDay.F
        else:
            raise ValueError("Shipment date for shipment_id %d not within acceptable range. Possible values are M/T/W/R/F" % self.shipment_id)

    def print_shipment(self):
        print("%d %s %s %s" % (self.shipment_id, self.source, self.dest, self.date.value))

    def return_shipment_as_string(self):
        return "%d %s %s %s" % (self.shipment_id, self.source, self.dest, self.date.value)

    def print_shipment_id(self):
        print("%d " % self.shipment_id)

    '''A shipment can only follow a predecessor shipment if 
        1) The shipment source is same as predecessor's destination
        2) Predecessor shipment does not start on a Friday 
        3) The shipment date immediately follows the predecessor's date'''
    def can_follow_shipment(self,predecessor):
        if self.source == predecessor.dest and predecessor.date is not ShipmentDay.F and (self.date.value - predecessor.date.value == 1):
            return True
        else:
            return False

    def __lt__(self,other):
        return self.date < other.date

    def __gt__(self,other):
        return self.date > other.date

    def __eq__(self,other):
        return self.shipment_id == other.shipment_id

    def __ne__(self,other):
        return self.shipment_id != other.shipment_id


