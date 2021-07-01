#!/usr/bin/env python3

# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved

from pprint import pprint

from lib.sensilla import SensillaClient

if __name__ == "__main__":
    # Initialize the Sensilla Client
    sc = SensillaClient()

    # Get a list of all projects you have access to
    projects = sc.list_projects()

    for project in projects:
        details = sc.list_project_details(project["id"])
        print("#" * 45)
        print("##### Project details for Id: {}".format(project["id"]))
        print("#" * 45)
        pprint(details, indent=4, sort_dicts=False, compact=False, width=79)

        # Get measurements for all locations
        for location in details["locationSet"]:
            measurements = sc.get_measurements_by_location(location["id"])

            print("\n" + "#" * 45)
            print("##### Measurements for location Id: {}".format(location["id"]))
            print("#" * 45)

            if len(measurements):
                print("timestamp,temperature,humidity,co2")
                for measurement in measurements:
                    print(
                        "{},{},{},{}".format(
                            measurement["timestamp"],
                            measurement["environmentalTemperature"],
                            measurement["environmentalRelativeHumidity"],
                            measurement["co2Concentration"],
                        )
                    )
            else:
                print("No measurements in the selected time range")
            print("\n")
        print("\n\n")
