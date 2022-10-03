#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import os
from dotenv import load_dotenv
import urllib.request
import xml.etree.ElementTree as et

# load env file
load_dotenv()

USER_ID = os.getenv("USER_ID")


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


def is_address(addy: str) -> tuple:
    """
    Parses string address value to find street, city, and name

    Inputs:
        addy (str):                 assumed address string

    Return (list):                  returns list containing 3 str elements
                                    containing street, city, state
    """

    pattern = \
        r"(^\d+\s{1}[\s?a-zA-Z0-9\#.]+)\W{1,2}([a-zA-Z\s.]+)\W{1,2}([a-zA-Z]{0,2})"  # noqa: E501

    try:
        parsed = re.findall(pattern, addy)
        print(parsed)

    except TypeError:
        raise TypeError("Value is not an address-like string")

    else:
        if len(parsed) == 0:
            raise ValueError("Unable to parse address")

        else:
            return parsed[0]


def get_single(address: tuple, user_id=USER_ID) -> str:
    request_xml = f'''\
        <?xml version="1"?>
        <AddressValidateRequest USERID="{user_id}">
            <Revision>1</Revision>
            <Address ID="0">
            <Address1>{address[0]}</Address1>
            <Address2></Address2>
            <City>{address[1]}</City>
            <State>{address[2]}</State>
            <Zip5></Zip5>
            <Zip4/>
            </Address>
        </AddressValidateRequest>'''

    print(f"=== GETTING ZIP FOR {address[0]}, {address[1]}, {address[2]} ===")

    request_str = request_xml.replace("\n", "").replace("\t", "")

    request_url = \
        "https://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" \
        + request_str

    response = urllib.request.urlopen(request_url).read()

    root = et.fromstring(response)

    zip5, zip4 = root.findall('Address')[0].find(
        'Zip5').text, root.findall('Address')[0].find('Zip4').text

    return f"{zip5}-{zip4}"
