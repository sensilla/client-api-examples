# Copyright (C) Sensilla Technologies S.A. - All Rights Reserved
import logging

from lib.config import DEBUG

logfmt = "%(levelname)-7s - %(filename)s:%(lineno)d (%(funcName)s) : %(message)s"

if DEBUG:
    logging.basicConfig(
        format=logfmt,
        filename="output.log",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format=logfmt,
        filename="output.log",
        level=logging.INFO,
    )

logging.getLogger("urllib3").propagate = False
