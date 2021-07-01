# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved
import os

DEBUG = os.environ.get("SENSILLA_DEBUG", "off") == "on"
API_URL = os.environ.get("SENSILLA_API_URL", "https://api.sensilla.tech/graphql/")
API_USERNAME = os.environ["SENSILLA_API_USERNAME"]
API_PASSWORD = os.environ["SENSILLA_API_PASSWORD"]
