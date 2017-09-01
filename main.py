from lib import Shipment
from lib import Bundle
import argparse
import copy

'''Main function'''
def main():
    verbose = False
    shipments = []
    final_bundle_set = []
    final_shipment_set = []

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("Verbose mode on\n")
        verbose = True

    '''Read file'''
    if verbose:
        print("Input File: %s" % args.input_file)
    for line in open(args.input_file).readlines():
        parsed = line.split()
        shipment = Shipment.Shipment(parsed[0],parsed[1],parsed[2],parsed[3])
        if verbose:
            shipment.print_shipment()
        shipments.append(shipment)

    '''Sort shipments based on day of week - M>T>W>R>F'''
    shipments.sort()
    if verbose:
        print("\nsorted shipments")
        for shipment in shipments:
            shipment.print_shipment()
        print("\n")

    '''Primary Algorithm'''
    for shipments_iter in range(0,len(shipments)):
        if verbose:
            print("--- starting at shipment %d ---" % shipments_iter)

        '''Skip if shipment is already bundled'''
        if shipments[shipments_iter] in final_shipment_set:
            if verbose:
                print("Shipment is already bundled. Skipping. Shipment_id - %d ---" %  shipments[shipments_iter].shipment_id)
            continue

        '''Each working bundle will correspond to the largest possible bundle at shipment_iter position'''
        working_bundles = [None] * len(shipments)


        '''For the first shipment, add to bundle at index 0'''
        working_bundles[shipments_iter] = Bundle.Bundle()
        working_bundles[shipments_iter].append_to_bundle(shipments[shipments_iter])

        '''Some crazy dynamic programming going on below'''
        '''Iterate over the remaining shipments'''
        for i in range(shipments_iter + 1, len(shipments)):
            working_bundles[i] = Bundle.Bundle()
            if verbose:
                print("\n\n[OUTER] at %d shipment - %s" % (i, shipments[i].return_shipment_as_string()))

            '''Skip if shipment is already in final_bundle_set'''
            if shipments[i] in final_shipment_set:
                if verbose:
                    print("[OUTER] at %d. %s shipment exists in final bundle" % (i, shipments[i].return_shipment_as_string()))
                continue

            '''Loop below finds the largest bundle for shipment at shipments_iter up until position i'''
            for j in range(shipments_iter, i):
                if verbose:
                    print("[INNER] at %d shipment - %s" % (j, shipments[j].return_shipment_as_string()))

                if verbose:
                    print("Inner working bundle - %s" % working_bundles[j].return_shipment_ids_as_string())
                    print("Outer working bundle - %s" % working_bundles[i].return_shipment_ids_as_string())
                    print("[INNER] Inner v/s Outer bundle size %d - %d" % (working_bundles[j].get_bundle_size(), working_bundles[i].get_bundle_size()))
                    if shipments[i].can_follow_shipment(shipments[j]):
                        print("%s can follow %s" % (shipments[i].return_shipment_as_string(), shipments[j].return_shipment_as_string()))

                if working_bundles[j].get_bundle_size() >= working_bundles[i].get_bundle_size():
                    working_bundles[i].fast_copy(working_bundles[j])

                if working_bundles[i].can_append_to_bundle(shipments[i]):
                    working_bundles[i].append_to_bundle(shipments[i])

            if verbose:
                print("Largest bundle for position %d is - %s" % (i,working_bundles[i].return_shipment_ids_as_string()))

        '''Find the overall largest bundle in the current set of working bundles'''
        largest_bundle = None
        for k in working_bundles:
            if not largest_bundle or k.get_bundle_size() > largest_bundle.get_bundle_size():
                largest_bundle = k

        '''Close out iteration by recording the largest bundle for the given position'''
        final_bundle_set.append(largest_bundle)
        for final_shipment in largest_bundle.shipments:
            final_shipment_set.append(final_shipment)

        if verbose:
            print("--- bundle added to final bundle set - %s ---" % largest_bundle.return_shipment_ids_as_string())

    for bundle in final_bundle_set:
        print("%s" % bundle.return_shipment_ids_as_string())

main()

