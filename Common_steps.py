import logging
import os
import json

import requests


class GameConfig:

    def __init__(self, game_file_suffix='_DVI_Config.json', main_config_file='Main_Config.json'):
        self.game_file_suffix = game_file_suffix
        self.main_config_file = main_config_file
        self.game_config, self.game_prefix, self.config_path = self.get_game_config()
        self.main_config = self.get_main_config()
        self.players = self.get_players()

    @staticmethod
    def read_json_file(request):
        json_input = json.dumps(request)
        request_json = json.loads(json_input)
        return request_json

    @staticmethod
    def response_financial(req_name, arg_url, req_data):
        response = requests.post(arg_url, json=req_data)
        status_code = response.status_code
        try:
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

    def get_game_config(self):
        config_files = [f for f in os.listdir('config') if f.endswith(self.game_file_suffix)]
        if len(config_files) == 0:
            raise ValueError('No matching config file found')
        game_file = config_files[0]
        config_path = os.path.join('config', game_file)
        with open(config_path, 'r') as file:
            game_config = json.load(file)
        game_prefix = game_config['Game_Prefix']
        return game_config, game_prefix, config_path

    def get_main_config(self):
        with open(f'config/{self.main_config_file}', 'r') as file:
            main_config = json.load(file)
        return main_config

    def get_players(self):
        P = self.main_config['Players']
        K = list((P.keys()))
        for j in range(len(P)):
            globals()[f"P{j + 1}"] = P[K[j]]["Id"]
            globals()[f"P{j + 1}_User"] = P[K[j]]["User"]
            globals()[f"P{j + 1}_Pwd"] = P[K[j]]["Password"]

        Players = []
        for j in range(len(P)):
            Players.append((globals()[f'P{j + 1}'], globals()[f'P{j + 1}_User'], globals()[f'P{j + 1}_Pwd']))
        return Players

    def get_dvi(self):
        return self.game_config['Name']

    def get_config(self, dvi, dvi_games, regulations=None):

        config = []
        if dvi == self.get_dvi():
            g_codes = self.game_config['Game_Codes'][:int(dvi_games)]
            debit = self.game_config['Debit_Amount']
            credit = self.game_config['Credit_Amount']

            if regulations is not None:
                Regulation = regulations
            else:
                Regulation = self.game_config['PlayerRegulation']
            for code in g_codes:
                if 'Username' not in self.game_config or 'Password' not in self.game_config:
                    config.append((code, debit, credit, Regulation))
                else:
                    username = self.game_config['Username']
                    password = self.game_config['Password']
                    config.append((code, debit, credit, username, password, Regulation))
        return config

    def get_urls(self):
        base_url = self.main_config['Base_Url']
        launch_url = self.main_config['Launch_Url']
        operator_url = self.main_config['Operator_Url']
        home_url = self.main_config['HomeUrl']
        launch_uri = self.main_config['Launch_URI']
        vendor_uri = self.game_config['Vendor_URI']
        create_token_uri = self.main_config['CreateToken_URI']
        auth_uri = self.game_config["Auth_URI"]
        stake_uri = self.game_config['Stake_URI']
        payout_uri = self.game_config['Payout_URI']
        refund_uri = self.game_config['Refund_URI']
        LaunchGame_Url = launch_url + launch_uri
        CreateToken_Url = operator_url + create_token_uri
        Auth_Url = base_url + vendor_uri + auth_uri
        Stake_URl = base_url + vendor_uri + stake_uri
        Payout_URl = base_url + vendor_uri + payout_uri
        Refund_URl = base_url + vendor_uri + refund_uri

        return LaunchGame_Url, CreateToken_Url, Auth_Url, Stake_URl, Payout_URl, Refund_URl


game_configs = GameConfig()
url = game_configs.get_urls()
