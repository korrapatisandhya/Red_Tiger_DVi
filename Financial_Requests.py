from random import choice
from Common_steps import *
from game_steps import *


class FinancialReq(GameConfig, GameSteps):

    # This is a sub function to create headers based on documentation of dvi

    # This is a sub function to send request to api and get response for financial Requests\
    # like Authentication,Debit,Credit,Cancel

    def response_authentication(self, arg_url, arg_req, arg_username, arg_password, arg_client_token):
        auth_req = self.read_json_file(arg_req)
        auth_req['token'] = arg_client_token
        arg_headers = self.create_header(auth_req)
        auth_response = self.response_basicauth_financial('Authenticate', arg_url, auth_req, arg_headers, arg_username,
                                                          arg_password)
        try:
            auth_balance = auth_response['result']['balance']['cash']
            assert True
        except KeyError:
            print("KeyError :Authentication Response Error")
            logging.info("KeyError :Authentication Response Error")
            assert False
        return auth_balance

    def response_debit(self, arg_url, arg_req, arg_client_token, arg_userId, txn_id, arg_debit, arg_username,
                       arg_password):
        debit_request = self.read_json_file(arg_req)
        debit_request['token'] = arg_client_token
        debit_request['userId'] = arg_userId
        txn_id, r_id = self.get_ids()
        debit_request['transaction']['id'] = txn_id
        amount = choice(arg_debit)
        debit_request['transaction']['stake'] = amount
        debit_request['round']['id'] = r_id
        arg_headers = self.create_header(debit_request)

        stake_amount = float()  # Initialize with a default value
        stake_balance = float()
        stake_res = self.response_basicauth_financial('Stake', arg_url, debit_request, arg_headers, arg_username,
                                                      arg_password)
        try:
            if stake_res is not None and isinstance(stake_res, dict) and 'result' in stake_res and \
                    isinstance(stake_res['result'], dict) and 'stake' in stake_res['result'] and \
                    isinstance(stake_res['result']['stake'], dict) and 'balance' in stake_res['result'] \
                    and isinstance(stake_res['result']['balance'], dict) and 'cash' in stake_res['result']['stake'] \
                    and 'cash' in stake_res['result']['balance']:
                stake_amount = stake_res['result']['stake']['cash']
                stake_balance = stake_res['result']['balance']['cash']
        except KeyError:
            print("KeyError: Debit Response Error")
            logging.info("KeyError: Debit Response Error")
        return stake_amount, stake_balance, txn_id, r_id

    def response_credit(self, arg_url, arg_req, arg_client_token,  arg_userId, txn_id, arg_credit, round_id,
                        arg_username, arg_password):
        credit_request = self.read_json_file(arg_req)
        credit_request['token'] = arg_client_token
        credit_request['userId'] = arg_userId
        txn_id, r_id = self.get_ids()
        credit_request['transaction']['id'] = txn_id
        amount = choice(arg_credit)
        credit_request['transaction']['payout'] = amount
        credit_request['round']['id'] = round_id
        arg_headers = self.create_header(credit_request)
        payout_amount = float()
        payout_balance = float()
        credit_res = self.response_basicauth_financial('Payout', arg_url, credit_request, arg_headers, arg_username,
                                                       arg_password)
        try:

            if credit_res is not None and isinstance(credit_res, dict) and 'result' in credit_res and \
                    isinstance(credit_res['result'], dict) and 'payout' in credit_res['result'] and \
                    isinstance(credit_res['result']['payout'], dict) and 'balance' in credit_res['result'] \
                    and isinstance(credit_res['result']['balance'], dict) and 'cash' in credit_res['result']['payout'] \
                    and 'cash' in credit_res['result']['balance']:
                payout_amount = credit_res['result']['payout']['cash']
                payout_balance = credit_res['result']['balance']['cash']
        # Perform further operations with Payout_Amount as needed
        except KeyError:
            print("KeyError: Debit Response Error")
            logging.info("KeyError: Debit Response Error")
        return payout_amount, payout_balance

    def response_cancel_transaction(self, arg_url, arg_req, arg_client_token, arg_userId,
                                    arg_ref_txn_id, arg_stake, arg_r_id,
                                    arg_username, arg_password):
        cancel_req = self.read_json_file(arg_req)
        cancel_req['token'] = arg_client_token
        cancel_req['userId'] = arg_userId
        cancel_req['transaction']['id'] = arg_ref_txn_id
        cancel_req['transaction']['stake'] = arg_stake
        cancel_req['round']['id'] = arg_r_id
        arg_headers = self.create_header(cancel_req)
        balance = float()
        cancel_response = self.response_basicauth_financial('Refund', arg_url, cancel_req, arg_headers, arg_username,
                                                            arg_password)
        try:
            if cancel_response is not None and isinstance(cancel_response, dict) and 'result' in cancel_response and \
                    isinstance(cancel_response['result'], dict) and 'balance' in cancel_response['result'] and\
                    isinstance(cancel_response['result']['balance'], dict) and 'cash' in cancel_response['result'][
                    'balance']:
                balance = cancel_response['result']['balance']['cash']
        except KeyError:
            print("KeyError: Debit Response Error")
            logging.info("KeyError: Debit Response Error")
        return balance


fr = FinancialReq()
