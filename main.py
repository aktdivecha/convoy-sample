from lib import Shipment
from lib import Cluster
import argparse
import copy

'''Main function'''
def main():
    verbose = False
    shipments = []

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode on\n")
        verbose = True

    if verbose:
        print("Input File: %s" % args.input_file)

    for line in open(args.input_file).readlines():
        parsed = line.split()
        shipment = Shipment.Shipment(parsed[0],parsed[1],parsed[2],parsed[3])
        if verbose:
            shipment.print_shipment()
        shipments.append(shipment)

    shipments.sort()

    if verbose:
        print("\nsorted shipments")
        for shipment in shipments:
            shipment.print_shipment()
        print("\n")

    '''Primary Algorithm'''

    '''This contains list of final clusters'''
    final_cluster_set = []
    final_shipment_set = []

    for shipments_iter in range(0,len(shipments)):
        if verbose:
            print("--- starting at shipment %d ---" % shipments_iter)
        if shipments[shipments_iter] in final_shipment_set:
            if verbose:
                print("shipment already exists in final set. shipment_id - %d ---" %  shipments[shipments_iter].shipment_id)
            continue

        '''Start with Array of empty clusters'''
        working_clusters = [None] * len(shipments)

        '''For the first shipment, add to Cluster at index 0'''
        working_clusters[shipments_iter] = Cluster.Cluster()
        working_clusters[shipments_iter].append_to_cluster(shipments[shipments_iter])

        for i in range(shipments_iter + 1, len(shipments)):
            working_clusters[i] = Cluster.Cluster()
            if verbose:
                print("\n\n[OUTER] at %d shipment - %s" % (i, shipments[i].return_shipment_as_string()))

            '''Ignore if shipment is already in final_cluster_set'''
            if shipments[i] in final_shipment_set:
                if verbose:
                    print("[OUTER] at %d. %s shipment exists in final cluster" % (i, shipments[i].return_shipment_as_string()))
                continue

            '''Inner iteration'''
            for j in range(shipments_iter, i):
                if verbose:
                    print("[INNER] at %d shipment - %s" % (j, shipments[j].return_shipment_as_string()))

                if verbose:
                    print("Inner working cluster - %s" % working_clusters[j].return_shipment_ids_as_string())
                    print("Outer working cluster - %s" % working_clusters[i].return_shipment_ids_as_string())
                    print("[INNER] Inner v/s Outer cluster size %d - %d" % (working_clusters[j].get_cluster_size(), working_clusters[i].get_cluster_size()))
                    if shipments[i].can_follow_shipment(shipments[j]):
                        print("%s can follow %s" % (shipments[i].return_shipment_as_string(), shipments[j].return_shipment_as_string()))

                if working_clusters[j].get_cluster_size() >= working_clusters[i].get_cluster_size():
                    working_clusters[i].fast_copy(working_clusters[j])

                if working_clusters[i].can_append_to_cluster(shipments[i]):
                    working_clusters[i].append_to_cluster(shipments[i])

            if verbose:
                print("Largest cluster for position %d is - %s" % (i,working_clusters[i].return_shipment_ids_as_string()))

        '''Find the overall largest cluster in the current set of working clusters'''
        largest_cluster = None
        for k in working_clusters:
            if not largest_cluster or k.get_cluster_size() > largest_cluster.get_cluster_size():
                largest_cluster = k

        '''Close out iteration by recording the largest cluster for the given position'''
        final_cluster_set.append(largest_cluster)
        for final_shipment in largest_cluster.shipments:
            final_shipment_set.append(final_shipment)

        if verbose:
            print("--- Cluster added to final cluster set - %s ---" % largest_cluster.return_shipment_ids_as_string())


    for cluster in final_cluster_set:
        print("%s" % cluster.return_shipment_ids_as_string())

main()

