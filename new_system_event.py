#!/usr/bin/env python3

# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved
import json

from lib.sensilla import SensillaClient

if __name__ == "__main__":
    # Initialize the Sensilla Client
    sc = SensillaClient()

    description = "HVAC - Malfunction of moisture sensor"
    data = {"source": "The coolest HVAC in the building", "severity": "fatal", "firmware_version": "3.x.y"}

    event_data = json.dumps(data)

    res = sc.create_system_event(224, description, event_data)

    print(f"New external system event created with event_id: {res}")
