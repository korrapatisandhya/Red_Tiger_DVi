import pytest_check as check
import hashlib
import shortuuid as suid
import time
import requests
import logging


class GameSteps:

    @staticmethod
    def response_basicauth_financial(req_name, arg_url, req_data, req_headers, username, password):
        # Sending Request to api by using Url,Req data and headers from particular defined request and basic auth
        response = requests.post(arg_url, json=req_data, headers=req_headers, auth=(username, password))
        # validating Response code
        status_code = response.status_code
        check.equal(status_code, 200, "Fail: Incorrect Status Code")
        try:
            # If Status Code is 200 The response will be generated in json format and logging then
            # if not the key error occurs and pass the execution.
            response = response.json()
            logging.info(req_name + ' Request: ' + '\n' + str(req_data) + '\n')
            logging.info('\n' + '-' * 30 + '\n')
            logging.info(req_name + ' Response: ' + '\n' + str(response) + '\n')
            logging.info('\n' + '-' * 30 + '\n')
            logging.info(req_name + ' Status: ' + '\n' + str(status_code))
            logging.info('\n' + '-' * 30 + '\n')
        except KeyError:
            pass
        return response

    @staticmethod
    def create_header(req_data):
        # Hard coding static values of KEY and Api secret from Documentation
        key = "PaWedSvY1fDgtBikQvaT9Fn8i5sNiyab"
        api_secret = "J2inygKCh1IJTdNGaKoTfHxs106KCYuQ"
        d = str(req_data)
        message = d + api_secret
        hash_value = hashlib.md5(message.encode()).hexdigest()
        data_header = {"key": key, "hash": hash_value}
        return data_header

    @staticmethod
    def get_ids():
        txn_id = suid.ShortUUID().random(length=13)
        r_id = round(time.time())
        return txn_id, r_id


gs = GameSteps()
