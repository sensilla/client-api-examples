# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved

from datetime import datetime

import requests

from lib.config import API_PASSWORD, API_URL, API_USERNAME
from lib.logger import logging

logging.basicConfig()


class SensillaClient:
    def __init__(self):
        logging.info("Initializing Sensilla Client")
        self.api_url = API_URL
        self.api_username = API_USERNAME
        self.api_password = API_PASSWORD
        self.api_token = self.get_token()
        logging.debug(f"JWT received: {self.api_token}")

    def __exec_query(self, query, variables):
        """Execute query or mutation on Sensilla backend"""
        headers = {"Authorization": f"Bearer {self.api_token}"}

        payload = dict()
        payload["query"] = query
        if variables:
            payload["variables"] = variables

        res = requests.post(self.api_url, headers=headers, json=payload)

        logging.debug("Query header >>> {}".format(res.request.headers))
        logging.info("Query body >>> {}".format(res.request.body))

        data = res.json()

        logging.info("Query result <<< {}".format(data))

        return data

    def get_token(self):
        """Get an JSON web token from Sensilla backend"""
        mutation = """
        mutation authenticateUser($password: String!, $username: String!) {
            authenticateUser(password: $password, username: $username) {
                bearerToken
            }
        }
        """

        variables = {
            "username": self.api_username,
            "password": self.api_password,
        }

        payload = dict()
        payload["query"] = mutation
        if variables:
            payload["variables"] = variables

        res = requests.post(self.api_url, json=payload)

        logging.debug("Auth header >>> {}".format(res.request.headers))
        logging.info("Auth body >>> {}".format(res.request.body))

        data = res.json()

        logging.info("Auth result <<< {}".format(data))

        return data["data"]["authenticateUser"]["bearerToken"]

    def list_projects(self):
        """List all projects inside account"""
        query = """
        query {
            groups {
                id
                name
            }
        }
        """
        variables = {}

        data = self.__exec_query(query, variables)

        return data["data"]["groups"]

    def list_project_details(self, projectId):
        """Used to get al project details including locations and sensor devices"""

        query = """
        query group($id: String) {
            group(id: $id) {
                id
                name
                externallocation {
                    extLocationName
                    extLocationId
                    activeParameters
                }
                locationSet {
                    id
                    name
                    lastMeasurement
                    hasActiveMonitoringMeasurement
                    sensorSet{
                        externalId
                    }
                }
            }
        }
        """

        variables = {"id": projectId}

        data = self.__exec_query(query, variables)

        return data["data"]["group"]

    def get_measurements_by_location(self, locationId, start="15m-ago", end="now"):
        """Query measurements by location"""
        query = """
        query measurements($location: Int, $start: String, $end: String) {
            measurements(location: $location, start: $start, end: $end) {
                timestamp
                environmentalTemperature
                environmentalRelativeHumidity
                co2Concentration
            }
        }
        """
        variables = {"location": int(locationId), "start": start, "end": end}

        data = self.__exec_query(query, variables)

        return data["data"]["measurements"]

    def create_system_event(self, projectId, description, event_data=None, start=None, end=None):
        """Submit new system event"""
        if start is None:
            start = int(datetime.utcnow().strftime("%s"))

        mutation = """
        mutation addSystemEvent($description: String!, $end: Int, $eventData: String, $groupId: Int!, $location: Int, $metric: String, $notes: String, $sensor: Int, $start: Int!) {
            addSystemEvent(description: $description, end: $end, eventData: $eventData, groupId: $groupId, location: $location, metric: $metric, notes: $notes, sensor: $sensor, start: $start) {
                event {
                    id
                }
            }
        }
        """
        variables = {"groupId": projectId, "start": start, "description": description}

        if end is not None:
            variables["end"] = end

        if event_data is not None:
            variables["eventData"] = event_data

        data = self.__exec_query(mutation, variables)

        return data["data"]["addSystemEvent"]["event"]["id"]

    def update_system_event(self, eventId, end=None):
        """Set end date on existing system event"""
        if end is None:
            end = int(datetime.utcnow().strftime("%s"))

        mutation = """
        mutation updateSystemEvent($end: Int!, $eventId: String!) {
            updateSystemEvent(end: $end, eventId: $eventId) {
                event {
                    id
                    description
                    notes
                    eventType
                    eventData
                    startTimestamp
                    endTimestamp
                }
            }
        }
        """
        variables = {"eventId": eventId, "end": end}

        data = self.__exec_query(mutation, variables)

        return data["data"]["updateSystemEvent"]["event"]
