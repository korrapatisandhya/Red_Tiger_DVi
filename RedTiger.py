import pytest
import Request_Body as VendorDVI
import allure
from Financial_Requests import *
from module_main import *
from Common_steps import game_configs as common
from assertpy import assert_that


def pytest_generate_tests(metafunc):
    dvi = metafunc.config.getoption("--dvi")
    dvi_games = metafunc.config.getoption("--dvi_games")
    regulations = metafunc.config.getoption("--regulations")
    #
    # only parametrize tests with the correct parameters
    dvi_config = common.get_config(dvi, dvi_games, regulations)
    if dvi and dvi_games:
        metafunc.parametrize('Game_Code, Debit, Credit ,Username,Password , regulations',
                             dvi_config)


@allure.suite('DVI')
@allure.sub_suite('RedTiger')
@allure.title("Debit - Credit Test Case for {Game_Code}")
@pytest.mark.Functional
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_Debit_Credit_VendorDVI(Game_Code, Debit, Credit, Username, Password, regulations, user_account):
    if user_account is not None:
        (P_Id, User, Pwd) = user_account

    else:
        P_Id, User, Pwd = 20451, 'ta1', 'ta1'

    P_Id = str(P_Id)

    LaunchGame_Url, CreateToken_Url, Auth_Url, Stake_Url, Payout_Url, Refund_Url = game_configs.get_urls()

    Token, Client_Token = lc.response_game_launch(LaunchGame_Url, VendorDVI.LaunchGame_Request,
                                                  Game_Code, P_Id, regulations)
    print("Launch Game Successful")

    lc.response_create_token(CreateToken_Url, VendorDVI.CreateToken_Request, Game_Code, Token,
                             P_Id, User, Pwd)
    print("Create Token Successful")

    Auth_Balance = fr.response_authentication(Auth_Url, VendorDVI.Auth_Request, Username, Password,
                                              Client_Token)

    print("Authentication Successful")
    txn_Id = 0
    Stake_Amount, Stake_Balance, trn_id, r_id = fr.response_debit(Stake_Url, VendorDVI.Stake_Request,
                                                                  Client_Token, P_Id, txn_Id, Debit, Username, Password)
    Actual_Debit = float(Auth_Balance) - float(Stake_Balance)

    print("Debit Successful")
    txn_id = 0
    Credit_Amount, Credit_Balance = fr.response_credit(Payout_Url, VendorDVI.Payout_Request,
                                                       Client_Token, P_Id, txn_id, Credit, r_id, Username, Password)
    Actual_Credit = float(Credit_Amount) - float(Actual_Debit)

    assert_that(float(Actual_Credit), float(Credit_Balance) - float(Auth_Balance)), Credit_Balance
    print("Credit Successful")


@allure.suite('DVI')
@allure.sub_suite('RedTiger')
@allure.title("Debit - Cancel Test Case for {Game_Code}")
@pytest.mark.Functional
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_Debit_Cancel_VendorDVI(Game_Code, Debit, Credit, Username, Password, regulations, user_account):
    if user_account is not None:
        (P_Id, User, Pwd) = user_account
    else:
        P_Id, User, Pwd = 20451, 'ta1', 'ta1'

    P_Id = str(P_Id)

    # (LaunchGame_Url, CreateToken_Url, Auth_Url, Bet_Url, Cancel_Url, Win_Url) = mainConfig()

    LaunchGame_Url, CreateToken_Url, Auth_Url, Stake_Url, Payout_Url, Refund_Url = game_configs.get_urls()

    Token, Client_Token = lc.response_game_launch(LaunchGame_Url, VendorDVI.LaunchGame_Request,
                                                  Game_Code, P_Id, regulations)
    print("Launch Game Successful")

    lc.response_create_token(CreateToken_Url, VendorDVI.CreateToken_Request, Game_Code, Token,
                             P_Id, User, Pwd)
    print("Create Token Successful")

    Auth_Balance = fr.response_authentication(Auth_Url, VendorDVI.Auth_Request, Username, Password,
                                              Client_Token)

    print("Authentication Successful")
    txn_Id = 0
    Stake_Amount, Stake_Balance, trn_id, r_id = fr.response_debit(Stake_Url, VendorDVI.Stake_Request,
                                                                  Client_Token, P_Id, txn_Id, Debit, Username, Password)
    assert_that(float(Auth_Balance), float(Stake_Balance) + float(Stake_Amount))
    print("Debit Successful")

    REF_TRAN_ID = trn_id
    REF_r_id = r_id
    REF_stake = Stake_Amount
    Cancel_Balance = fr.response_cancel_transaction(Refund_Url, VendorDVI.Refund_Request,
                                                    Client_Token, P_Id, REF_TRAN_ID, REF_stake, REF_r_id,
                                                    Username, Password)
    assert_that(float(Auth_Balance), float(Cancel_Balance))
    print("Cancel Successful")


@allure.suite('DVI')
@allure.sub_suite('RedTiger')
@allure.title("Multiple Debit - Cancel Test Case for {Game_Code}")
@pytest.mark.Functional
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_Multiple_Debit_Cancel_VendorDVI(Game_Code, Debit, Credit, Username, Password, regulations, user_account):
    if user_account is not None:
        (P_Id, User, Pwd) = user_account
    else:

        P_Id, User, Pwd = 20451, 'ta1', 'ta1'

    P_Id = str(P_Id)
    LaunchGame_Url, CreateToken_Url, Auth_Url, Stake_Url, Payout_Url, Refund_Url = game_configs.get_urls()

    Token, Client_Token = lc.response_game_launch(LaunchGame_Url, VendorDVI.LaunchGame_Request,
                                                  Game_Code, P_Id, regulations)
    print("Launch Game Successful")

    lc.response_create_token(CreateToken_Url, VendorDVI.CreateToken_Request, Game_Code, Token,
                             P_Id, User, Pwd)
    print("Create Token Successful")

    Auth_Balance = fr.response_authentication(Auth_Url, VendorDVI.Auth_Request, Username, Password,
                                              Client_Token)

    print("Authentication Successful")

    Stake_Balance = 0
    m_txn_id = 0
    Debit_Transactions = []
    Total_Deb_amount = 0
    for i in range(5):
        Stake_Amount, Stake_Balance, m_txn_id, round_id = fr.response_debit(Stake_Url, VendorDVI.Stake_Request,
                                                                            Client_Token, P_Id, m_txn_id, Debit,
                                                                            Username,
                                                                            Password)
        Deb_Amount = Stake_Amount
        Debit_Transactions.append((Deb_Amount, Stake_Balance, m_txn_id, round_id))
        Total_Deb_amount = float(Total_Deb_amount) + float(Deb_Amount)
    Final_Balance = Stake_Balance

    Actual_Debit = float(Auth_Balance) - float(Final_Balance)
    assert_that(float(Actual_Debit), float(Total_Deb_amount))

    print("Multiple Debit Successful")

    (Deb_Amount, Stake_Balance, m_txn_id_id, round_id) = choice(Debit_Transactions)

    fr.response_cancel_transaction(Refund_Url, VendorDVI.Refund_Request,
                                   Client_Token, P_Id, m_txn_id, Deb_Amount, round_id, Username,
                                   Password)
    s = assert_that(float(Auth_Balance), float(Final_Balance) + float(Total_Deb_amount))
    assert_that(s, 'Fail:Incorrect balance after refund')

    print("Random Cancel Successful")
