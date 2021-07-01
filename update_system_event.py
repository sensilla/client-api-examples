#!/usr/bin/env python3

# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved
import sys
from pprint import pprint

from lib.sensilla import SensillaClient

if __name__ == "__main__":
    # Initialize the Sensilla Client
    sc = SensillaClient()

    event_id = sys.argv[1]
    res = sc.update_system_event(event_id)

    print("External system event updated")
    pprint(res)
