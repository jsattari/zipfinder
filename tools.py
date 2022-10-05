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

        parsed_list.append(parsed)

    return parsed_list


def get_xml(parsed_addresses: list) -> list:
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

    # create a counter to determine version number
    counter = 0
    output = [0] * len(parsed_addresses)

    # loop through parsed address input list
    for key, value in enumerate(parsed_addresses):

        # if current value is a tuple, add xml structure to string
        if isinstance(value, tuple):
            mini_xml = f'''\
                <Address ID="{counter}">
                    <Address1>{value[0]}</Address1>
                    <Address2></Address2>
                    <City>{value[1]}</City>
                    <State>{value[2]}</State>
                    <Zip5></Zip5>
                    <Zip4/>
                </Address>'''

            # append xml structure to output xml string
            # increment counter
            output[key] = mini_xml
            counter += 1

        else:
            output[key] = value

    return output


def get_zips(xml_str: list, user_id=USER_ID) -> list:
    """
    Parses xml string input and makes request to api for zip codes

    Inputs
        xml_str (list):                 list of unformatted xml strings \
            with newlines and tab spaces removed

    Return (list):                      list of api responses\
        that are zip codes
    """
    # create output list
    output = [0] * len(xml_str)

    # begin xml structured string
    xml_addys = \
        f'<?xml version="1"?>\n\t<AddressValidateRequest USERID="{user_id}">\n\t\t<Revision>1</Revision>'  # noqa: E501

    for key, value in enumerate(xml_str):
        if "\n" in value:
            xml_addys = xml_addys + value

        else:
            output[key] = value

    # close xml string
    xml_addys = xml_addys + '\n</AddressValidateRequest>'

    # format xml to remove newlines and tab spaces
    xml_formatted_addys = xml_addys.replace("\n", "").replace("\t", "")

    # parse xml
    quoted_request_str = urllib.parse.quote_plus(xml_formatted_addys)

    # create variable containing request url
    request_url = \
        "https://production.shippingapis.com/ShippingAPI.dll?API=Verify&XML=" + quoted_request_str  # noqa: E501

    # make request
    response = urllib.request.urlopen(request_url)

    # read response contents into variable
    contents = response.read()

    # read xml response structure
    root = et.fromstring(contents)

    # create counter to iterate through root xml response
    # create variable to house iteration of Address response
    counter = 0
    zips = root.findall("Address")

    # loop through values in length of output array
    for num in range(0, len(output)):

        # if element is 0, then replace it with
        # the 9 digit zip code
        if output[num] == 0:
            output[num] = f"{zips[counter].find('Zip5').text}" + \
                "-" + f"{zips[counter].find('Zip4').text}"
            # increment counter
            counter += 1

        else:
            # else element should already have an error string
            # associated with it
            continue

    return output
