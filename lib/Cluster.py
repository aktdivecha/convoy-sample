from lib import Shipment
import copy

class Cluster:

    def __init__(self):
        self.shipments = []

    def get_first_shipment(self):
        if self.shipments:
            return self.shipments[0]
        else:
            raise IndexError("Cannot get shipment. Cluster is Empty")

    def get_final_shipment(self):
        if self.shipments:
            return self.shipments[-1]
        else:
            raise IndexError("Cannot get shipment. Cluster is Empty")

    def can_append_to_cluster(self, shipment):
        if shipment.can_follow_shipment(self.get_final_shipment()):
            return True
        else:
            return False

    def append_to_cluster(self, shipment):
        self.shipments.append(copy.deepcopy(shipment))
        return True

    def print_shipment_ids(self):
        for shipment in self.shipments:
            print("%d" % shipment.shipment_id, end=" ")

    def return_shipment_ids_as_string(self):
        return " ".join(str(shipment.shipment_id) for shipment in self.shipments)

    def get_cluster_size(self):
        return len(self.shipments)

    def is_shipment_in_cluster(self, shipment):
        for i in self.shipments:
            if i.shipment_id == shipment.shipment_id:
                return True
        return False





