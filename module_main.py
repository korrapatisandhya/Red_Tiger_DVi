import re
import logging
import pytest_check as check
from Common_steps import GameConfig


class LaunchToken(GameConfig):

    def response_game_launch(self, arg_url, req_data, game_code, player_id, arg_reg):
        game_launch_req = self.read_json_file(req_data)
        game_launch_req["GameCode"] = game_code
        game_launch_req['PlayerId'] = player_id
        game_launch_req['PlayerRegulation'] = arg_reg
        game_launch_response = self.response_financial('GameLaunch', arg_url, game_launch_req)
        try:
            token = game_launch_response['Token']
            url = game_launch_response['Url']
            expression = r"(?<=token=)([^&]*)(?=&)?"
            client_token = re.findall(expression, url)[0]
        except KeyError:
            print("KeyError: GameLaunch Transaction Response Error")
            logging.info("KeyError: GameLaunch Transaction Response Error")
            assert False
        return token, client_token

    def response_create_token(self, arg_url, req_data, game_code, token, player_id, username, password):
        create_token_req = self.read_json_file(req_data)
        create_token_req['GameCode'] = game_code
        create_token_req['Token'] = token
        create_token_req['PlayerId'] = player_id
        create_token_req['Account']['UserName'] = username
        create_token_req['Account']['Password'] = password
        create_token_response = self.response_financial('CreateToken', arg_url, create_token_req)
        error = create_token_response['Error']
        check.equal(error, None, "Error in the Create Token Response")


lc = LaunchToken()
