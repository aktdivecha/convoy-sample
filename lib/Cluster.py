from lib import Shipment


class Cluster:

    def __init__(self):
        self.shipments = []
        self.size = 0

    '''This function cheats the python built-in copy.copy() and optimizes Cluster copying by more than 10x'''
    def fast_copy(self, other_cluster):
        self.shipments = list(other_cluster.shipments)
        self.size = other_cluster.size

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
        self.shipments.append(shipment)
        self.size += 1
        return True

    def print_shipment_ids(self):
        for shipment in self.shipments:
            print("%d" % shipment.shipment_id, end=" ")

    def return_shipment_ids_as_string(self):
        return " ".join(str(shipment.shipment_id) for shipment in self.shipments)

    def get_cluster_size(self):
        return self.size

    def is_shipment_in_cluster(self, shipment):
        for i in self.shipments:
            if i.shipment_id == shipment.shipment_id:
                return True
        return False

    def is_empty(self):
        if len(self.shipments) == 0:
            return True
        else:
            return False





