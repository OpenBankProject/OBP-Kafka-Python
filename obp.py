import json
# load mockup data from json file
with open('example_import.json') as data_file:
  data = json.load(data_file)
banks        = data["banks"]
users        = data["users"]
accounts     = data["accounts"]
transactions = data["transactions"]

#
# use functions provided below as model for connecting to real data sources 
#

# getBank returns single bank data
# accepts string bankId as argument 
# returns string
#
def getBank(args):
  global banks 
  # get argument
  bankId = args['bankId']
  if not bankId:
    # return error if empty
    return '{error:"no argument given"}'
  if bankId   == "123":
    # hardcoded values for bank1 
    permalink     = "123" 
    fullBankName  = "Test Bank"
    shortBankName = "tbank"
    logoURL       = "http://tbank.tb/images/logo.png"
    websiteURL    = "http://tbank.tb"
  elif bankId == "321":
    # hardcoded values for bank2
    permalink     = "321" 
    fullBankName  = "Another Bank"
    shortBankName = "abank"
    logoURL       = "http://abank.ab/images/logo.png"
    websiteURL    = "http://abank.ab"
  else:
    # just two banks in this demo
    return '{}'
  # assemble the return string
  r  = '{'
  r += '"permalink":"'     + permalink     + '",' 
  r += '"fullBankName":"'  + fullBankName  + '",' 
  r += '"shortBankName":"' + shortBankName + '",' 
  r += '"logoURL":"'       + logoURL       + '",' 
  r += '"websiteURL":"'    + websiteURL    + '"'
  r += '}' 
  # return result
  return r

# getBanks returns list of all banks
# accepts no arguments
# returns string
#
def getBanks(args):
  global banks 
  # list of bankIds to return
  bankList  = ["123", "321"] 
  # opening bracket
  r  =  '{' 
  # loop over all bankIds
  for bank in bankList:
    # get bank data calling getBank with bankId as argument
    r += getBank({"bankId":bank})
    # add comma after each entry
    r += '",'
  # remove trailing comma from result string
  r  = r[:-1]  
  # closing bracket
  r  +=  '}' 
  # return result
  return r

# getTransaction returns transaction data
# accepts arguments: bankId, accountId, and transactionId 
# returns string
#
def getTransaction(args):
  global transactions 
  # get arguments
  bankId  = args['bankId'] 
  accountId = args['accountId']
  transactionId = args['transactionId']
  for t in transactions:
    if bankId == t["this_account"]["bank"] and accountId == t["this_account"]["id"] and transactionId == t["id"]:
      # assemble the return string
      r  = '{'
      r += '"bankId":"'          + t["this_account"]["bank"]   + '",' 
      r += '"accountId":"'       + t["this_account"]["id"]     + '",' 
      r += '"transactionId":"'   + t["id"]                     + '",' 
      r += '"transactionType":"' + t["details"]["type"]        + '",' 
      r += '"amount":"'          + t["details"]["value"]       + '",' 
      r += '"currency":"'        + "GBP"                       + '",' 
      r += '"description":"'     + t["details"]["description"] + '",' 
      r += '"startDate":"'       + t["details"]["posted"]      + '",' 
      r += '"finishDate":"'      + t["details"]["completed"]   + '",' 
      r += '"balance":"'         + t["details"]["new_balance"] + '",' 
      r += '"otherBankId":"'     + "obp-bank-x-g"              + '",'
      r += '"otherAccountId":"'  + "2330135d-fca8-4268-838d-833074985209"  + '"'
      r += '}' 
      # return result
      return r
  return '{}'

# getTransactions returns list of transactions depending on queryParams
# accepts arguments: bankId, accountId, and queryParams
# returns string
#
def getTransactions(args):
  global transactions 
  # get arguments
  bankId  = args['bankId'] 
  accountId = args['accountId']
  # mock search results according to queryParams
  if (bankId == "obp-bank-x-gh" and accountID == "test-x"):
    transactionIds = ['1','2']
  elif (bankId == "obp-bank-y-gh" and accountID == "test-y"):
    transactionIds = ['3']
  else:
    return '{}'
  # opening bracket
  r  =  '{' 
  # loop over all bankIds
  for transactionId in transactionIds:
    # get bank data calling getBank with bankId as argument
    r += getTransaction({"bankId":bankId,"accountId":accountId,"transactionId":transactionId})
    # add comma after each entry
    r += '",'
  # remove trailing comma from result string
  r  = r[:-1]  
  # closing bracket
  r  +=  '}' 
  # return result
  return r

# getBankAccount returns bank account data 
# accepts arguments: bankId and accountId
# returns string
#
def getBankAccount(args):
  global data
  # get arguments
  bankId = args['bankId']
  accountId = args['accountId']
  if not bankId or not accountId:
    # return error if empty
    return '{error:"no argument given"}'
  if bankId == "123" and accountId == "12345":
    # hardcoded values for bankAccount1 
    accountId       = "12345"
    accountType     = "savings"
    balance         = "20000"
    currency        = "EUR"
    name            = "Test transaction"
    label           = "test_transaction"
    swift_bic       = "SWIFT_BIC"
    iban            = "IBAN12345"
    number          = "123451234512345"
    bankId          = "123"
    lastUpdate      = "Fri Nov 13 17:57:04 CET 2015"
    accountHolder   = "ACCOUNT_HOLDER"  #deprecated?
  elif bankId == "321" and accountId == "54321":
    # hardcoded values for bankAccount2
    accountId       = "54321"
    accountType     = "savings"
    balance         = "15000"
    currency        = "EUR"
    name            = "Transaction testing"
    label           = "transaction_testing"
    swift_bic       = "BIC_SWIFT"
    iban            = "IBAN54321"
    number          = "543215432154321"
    bankId          = "321"
    lastUpdate      = "Sat Nov 14 11:37:14 CET 2015"
    accountHolder   = "HOLDER_OF_THE_ACCOUNT"  #deprecated?
  else:
    # just two bank accounts in this demo
    return '{}'
  # assemble the return string
  r  = '{'
  r += '"accountId":"'       + accountId       + '",' 
  r += '"accountType":"'     + accountType     + '",' 
  r += '"balance":"'         + balance         + '",' 
  r += '"currency":"'        + currency        + '",' 
  r += '"name":"'            + name            + '",' 
  r += '"label":"'           + label           + '",' 
  r += '"swift_bic":"'       + swift_bic       + '",' 
  r += '"iban":"'            + iban            + '",' 
  r += '"number":"'          + number          + '",'
  r += '"bankId":"'          + bankId          + '",' 
  r += '"lastUpdate":"'      + lastUpdate      + '",'
  r += '"accountHolder":"'   + accountHolder   + '"' #deprecated?
  r += '}' 
  # return result
  return r
