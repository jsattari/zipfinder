#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re


def allowed_file(filename: str, verification_list: list) -> bool:
    """
    Verifies if file extension is in list of acceptable extensions

    Inputs:
        filename (str):             filename that requires verification
        verification_list (list):   list of acceptable file extensions

    Return (bool):                  returns True extension is in
                                    verification_list otherwise false
    """

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in verification_list


def is_address(addy: str) -> list:
    """
    Parses string address value to find street, city, and name

    Inputs:
        addy (str):                 assumed address string

    Return (list):                  returns list containing 3 str elements
                                    containing street, city, state
    """

    pattern = \
        r"(^\d+\s{1}[\s?a-zA-Z0-9\#]+)\W{2}([a-zA-Z\s]+)\W{2}([a-zA-Z]{0,2})"

    try:
        street, city, state = re.findall(pattern, addy)[0]
        return [street, city, state]

    except ValueError:
        raise ValueError("String is not recognized as an address")
