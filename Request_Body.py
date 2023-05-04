LaunchGame_Request = {
    "GameCode": "RTG_HTML5_ElvenMagic",
    "PlayerId": "20451",
    "PlayerIP": "31.13.216.156",
    "CountryCode": "GB",
    "CurrencyCode": "GBP",
    "LanguageCode": "en-US",
    "Nickname": "",
    "HomeUrl": "https://operator.hub.stage.pariplaygames.com/Redirections/HomeUrl",
    "CashierUrl": "http://operator.hub.stage.pariplaygames.com/Redirections/CashierUrl",
    "Gender": 2,
    "PlayerRegulation": 2,
    "HistoryUrl": "http://operator.hub.stage.pariplaygames.com/Redirections/HistoryUrl",
    "IpAddress": "93.175.245.42",
    "IsMobile": False,
    "DebugMode": False,
    "IsNewWindow": False,
    "MiniGame": False,
    "Account": {"UserName": "t", "Password": "t"}
}


CreateToken_Request = {
  "Token": "ECA2873C18184EA09778AAA258309417",
  "PlayerId": "20451",
  "GameCode": "RTG_HTML5_DragonsFire",
  "Account": {
    "UserName": "ta1",
    "Password": "ta1"
  }
}


Auth_Request = {
  "token": "PPT_RTG-FS_6593DCF4B5F84FF0846932462A10AC2D",
  "casino": "PPT",
  "userId": "20451",
  "currency": "GBP",
  "ip": "3113216156",
  "channel": "mobile",
  "affiliate": ""
}

Stake_Request = {
  "token": "PPT_RTG-FS_6593DCF4B5F84FF0846932462A10AC2D",
  "userId": "204",
  "casino": "PPT",
  "currency": "GBP",
  "transaction": {
    "id": "osrd5d816jg",
    "stake": 400
  },
  "round": {
    "id": "325590",
    "starts": True,
    "ends": False
  },
  "game": {
    "type": "lines"
  }
}

Payout_Request = {
  "token": "PPT_RTG-FS_6593DCF4B5F84FF0846932462A10AC2D",
  "userId": "1",
  "casino": "PPT",
  "currency": "GBP",
  "transaction": {
    "id": "oyrf4-r01-y09",
    "payout": "4.00"
    },
  "round": {
    "id": 302,
    "starts": False,
    "ends": True
  },
  "game": {
    "type": "lines",
  },
  "retry": False
}

Refund_Request = {
  "token": "PPT_RTG-FS_6593DCF4B5F84FF0846932462A10AC2D",
  "userId": "201",
  "casino": "PPT",
  "currency": "GBP",
  "transaction": {
    "id": "orff4-r01-y09",
    "stake": "6.00"
  },
  "round": {
    "id": 304,
    "starts": False,
    "ends": True
  },
  "game": {
    "type": "lines"
  }
}
