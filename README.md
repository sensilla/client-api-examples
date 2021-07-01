# Sensilla Client API examples

This repository uses the Sensilla client API as documented at https://docs.sensilla.tech/public

The example code is written in [Python](https://python.org) and uses only one single library, [requests](https://docs.python-requests.org/en/master/)

The purpose of the example code is to introduce use how to consume the Sensilla client API by fetching measurements 
time-series and sending external system events.

If you run any of the scripts, they append to a log file called `output.log` that contains all communication with
the API including request headers and responses. On standard output you will receive some API responses and the
measurements for each location.

To run any of the examples, you need to configure some environment variables or modify the `lib/config.py` file.

## Environment variables

```
SENSILLA_DEBUG=off
SENSILLA_API_URL='https://api.sensilla.tech/graphql/'
SENSILLA_API_USERNAME='your user account'
SENSILLA_API_PASSWORD='your password'
```

## measurements.py

The measurements example first reads the complete project structure and then iterates over each location to get the 
datapoints from the last 15 minutes for the following metrics:
- temperature
- relative humidity
- CO2 
  
The result is printed in CSV format on the console.

Be aware to **limit the scope** in measurements.py if you have access to many projects and locations before running the
script.

### Example output

```
#############################################
##### Project details for Id: 41
#############################################
{   'id': '41',
    'name': 'RTH',
    'externallocation': {   'extLocationName': 'LU0109A',
                            'extLocationId': 9642,
                            'activeParameters': ['co', 'pm25', 'pm10', 'no2']},
    'locationSet': [   {   'id': '91',
                           'name': 'test',
                           'lastMeasurement': '2021-06-10T09:21:07+00:00',
                           'hasActiveMonitoringMeasurement': False,
                           'sensorSet': []},
                       {   'id': '79',
                           'name': 'Office',
                           'lastMeasurement': '2021-07-01T14:50:07+00:00',
                           'hasActiveMonitoringMeasurement': True,
                           'sensorSet': [{'externalId': 'device-2009000226'}]},
                       {   'id': '70',
                           'name': 'Living',
                           'lastMeasurement': '2021-07-01T14:50:07+00:00',
                           'hasActiveMonitoringMeasurement': True,
                           'sensorSet': [   {   'externalId': 'device-2009000118'}]}]}

#############################################
##### Measurements for location Id: 91
#############################################
No measurements in the selected time range



#############################################
##### Measurements for location Id: 79
#############################################
timestamp,temperature,humidity,co2
1625150407,24.789777755737305,45.22905349731445,371.0882873535156
1625150707,24.75977897644043,44.86451721191406,368.62957763671875
1625151007,24.739778518676758,44.702545166015625,371.3011474609375



#############################################
##### Measurements for location Id: 70
#############################################
timestamp,temperature,humidity,co2
1625150407,26.40884780883789,44.99882125854492,457.8241882324219
1625150707,26.428848266601562,45.42505645751953,501.16973876953125
1625151007,26.40884780883789,45.140018463134766,510.1171569824219
```

The project details can also be used to synchronise to another system, see project ID and each location ID in 
locationSet. The locationSet also includes a sensorSet to report the physical devices ID's.

## new_system_event.py

Used to create a new event from an external system such as a building management system.

In case the external system reports an event where the end date is not yet known, the event id must be stored for 
later updating the end timestamp.

Use case: a window open and window close event

### Example output

```New external system event created with event_id: f3bb39a8-9f7f-4014-af74-c9ddc2731fa0```

## update_system_event.py

Used to set the end timestamp on an event.

### Example output

```
External system event updated
{'description': 'HVAC - Malfunction of moisture sensor',
 'endTimestamp': '2021-07-01T13:01:14+00:00',
 'eventData': '{"source": "The coolest HVAC in the building", "severity": '
              '"fatal", "firmware_version": "3.x.y"}',
 'eventType': 'EXTERNAL_SYSTEM_EVENT',
 'id': 'f3bb39a8-9f7f-4014-af74-c9ddc2731fa0',
 'notes': None,
 'startTimestamp': '2021-07-01T13:00:05+00:00'}
 ```
