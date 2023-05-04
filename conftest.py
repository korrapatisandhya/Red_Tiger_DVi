import pytest
from Common_steps import game_configs
import logging


def pytest_addoption(parser):
    """

    :type parser: object
    """

    # parser.addoption("--dvi", action="store", default="all", required=False, help="description")
    parser.addoption("--dvi", action="store", default=game_configs.get_dvi(),
                     help="Name of the dvi config file to pass to test functions")
    parser.addoption("--dvi_games", action="store", default="1", help="Number of games to pass to test functions")
    parser.addoption("--regulations", action="store", default="0", help="Regulations: 0, 1, 2 etc")


@pytest.fixture()
def user_account(worker_id):
    workers = ['gw%d' % i for i in range(0, 10)]
    players = game_configs.get_players()
    """ use a different account in each xdist worker """
    if worker_id in workers:
        print(players[workers.index(worker_id)])
        return players[workers.index(worker_id)]


def log():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)
    logger.setLevel(logging.INFO)
    pass


log()


# def pytest_addoption(parser):
#     """
#
#     :type parser: object
#     """
#
#     # parser.addoption("--dvi", action="store", default="all", required=False, help="description")
#     parser.addoption("--dvi", action="store", default=get_dvi(),
#                      help="Name of the dvi config file to pass to test functions")
#     parser.addoption("--dvi_games", action="store", default="1", help="Number of games to pass to test functions")
#
#
#
#
#
# @pytest.fixture()
# def user_account(worker_id):
#     workers = ['gw%d' % i for i in range(0, 10)]
#     Players = get_Players()
#     """ use a different account in each xdist worker """
#     if worker_id in workers:
#         return Players[workers.index(worker_id)]
