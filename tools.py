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


def get_address_values(addy_list: list) -> list:
    """
    Parses list of string address value to find street, city, and name

    Inputs:
        addy (list):                list structure containing address strings

    Return (list):                  returns list containing 3 str elements
                                    containing street, city, state
    """

    # pattern for parsing address in "street, city, state" format
    # zip codes can be included as it will not cause parsing issues
    # commas are used as delimiters
    pattern = \
        r"(^\d+\s{1}[\s?a-zA-Z0-9\#.]+)\W{1,2}([a-zA-Z\s.]+)\W{1,2}([a-zA-Z]{0,2})"  # noqa: E501

    # creat empty data structure to house output
    parsed_list = []

    # iterate through input list
    for addy in addy_list:

        # try to apply regex, return errors if address string is not compatible
        try:
            parsed = re.findall(pattern, addy)[0]

        except TypeError:
            parsed = "Value is not an address-like string"

        except ValueError:
            parsed = "Unable to parse address"

        except IndexError:
            parsed = \
                "Address value could not be parsed into street, city, state strings"  # noqa: E501

        finally:
            parsed_list.append(parsed)

    return parsed_list


def get_xml(parsed_addresses: list, user_id=USER_ID) -> str:
    """
    Uses values from tuple containing address to make a single API call
    for zip5 and zip4 values

    Inputs:
        address (list):                 list of tuples containing \
            street, city, state \
                values in str format
        user_id (str):                  default argument for user \
            id for api endpoint

    Return (str):                       returns string containing \
        zip5 and zip4 values
    """

    xml_addys = f'<?xml version="1"?>\n\t<AddressValidateRequest USERID="{user_id}">\n\t\t<Revision>1</Revision>'  # noqa: E501
    counter = 0

    for addy in parsed_addresses:

        if isinstance(addy, tuple):
            mini_xml = f'''\
                <Address ID="{counter}">
                    <Address1>{addy[0]}</Address1>
                    <Address2></Address2>
                    <City>{addy[1]}</City>
                    <State>{addy[2]}</State>
                    <Zip5></Zip5>
                    <Zip4/>
                </Address>'''

            xml_addys = xml_addys + mini_xml
            counter += 1

        else:
            counter += 1

    xml_addys = xml_addys + '\n</AddressValidateRequest>'

    xml_formatted_addys = xml_addys.replace("\n", "").replace("\t", "")

    return xml_formatted_addys


def get_zips(xml_str: str) -> list:

    # parse
    quoted_request_str = urllib.parse.quote_plus(xml_str)

    # create variable containing request url
    request_url = \
        "https://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + quoted_request_str  # noqa: E501

    # make request
    response = urllib.request.urlopen(request_url)

    # read response contents into variable
    contents = response.read()

    # read xml response structure
    root = et.fromstring(contents)

    # create output list
    output = []

    # parse out zip5 and zip4 values and add to output list
    for struct in root.findall("Address"):
        output.append(f"{struct.find('Zip5').text}-{struct.find('Zip4').text}")

    return output
