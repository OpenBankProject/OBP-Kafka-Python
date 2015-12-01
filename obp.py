import json
import uuid
import datetime
import random

import settings

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
    return '{"error":"no argument given"}'
  for b in banks:
    if bankId == b["id"]:
      # assemble the return string
      r  = '{'
      r += '"bankId":"'        + b["id"]         + '",' 
      r += '"shortBankName":"' + b["short_name"] + '",' 
      r += '"fullBankName":"'  + b["full_name"]  + '",' 
      r += '"logoURL":"'       + b["logo"]       + '",' 
      r += '"websiteURL":"'    + b["website"]    + '"'
      r += '}' 
      # return result
      return r
  # return empty if not found 
  return '{}'

# getBanks returns list of all banks
# accepts no arguments
# returns string
#
def getBanks(args):
  global banks 
  r  =  '{' 
  for b in banks:
    # assemble the return string
    r  = '{'
    r += '"bankId":"'        + b["id"]         + '",' 
    r += '"shortBankName":"' + b["short_name"] + '",' 
    r += '"fullBankName":"'  + b["full_name"]  + '",' 
    r += '"logoURL":"'       + b["logo"]       + '",' 
    r += '"websiteURL":"'    + b["website"]    + '"'
    r += '}' 
    r += ','
  # remove trailing comma from result string
  if r.endswith(","):
    r  = r[:-1]  
  # closing bracket
  r  +=  '}' 
  # return result
  return r


# getRandomTransaction returns a random transaction
# accepts arguments: accounts
# returns dict of strings representing the account data
def getRandomTransaction(accounts):
    account = accounts[random.randint(0, len(accounts) - 1)]
    transaction_id = str(uuid.uuid4())
    description = "Random transfer {}".format(transaction_id)
    nowish = datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S.000Z")
    new_balance = "{:.2f}".format(random.random() * 1000)
    value = "{:.2f}".format(random.random() * -10)

    transaction = {
      "id": transaction_id,
      "this_account":{
        "id": account['id'],
        "bank": account['bank'],
      },
      "counterparty":{
        "name":"NONE"
      },
      "details":{
        "type":"Transfer",
        "description": description,
        "posted": nowish,
        "completed": nowish,
        "new_balance": new_balance,
        "value": value,
      }
    }
    if settings.DEBUG:
        print("Transaction: {}".format(transaction))
    return transaction


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
  if settings.INJECT_RANDOM_TRANSACTIONS:
    global accounts
    transactions.append(getRandomTransaction(accounts))
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
  # return empty if not found 
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
  queryParams = args['queryParams']
  if settings.INJECT_RANDOM_TRANSACTIONS:
    global accounts
    transactions.append(getRandomTransaction(accounts))
  r  =  '{' 
  for t in transactions:
    if bankId == t["this_account"]["bank"] and accountId == t["this_account"]["id"]:
      # assemble the return string
      r += '{'
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
      r += ','
  # remove trailing comma from result string
  if r.endswith(","):
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
  global accounts 
  # get arguments
  bankId = args['bankId']
  accountId = args['accountId']
  if not bankId or not accountId:
    # return error if empty
    return '{"error":"no argument given"}'
  for a in accounts:
    if bankId == a["bank"] and accountId == a["id"]:
      # assemble the return string
      r  = '{'
      r += '"accountId":"'       + a["id"]                    + '",' 
      r += '"accountType":"'     + a["type"]                  + '",' 
      r += '"balance":"'         + a["balance"]["amount"]     + '",' 
      r += '"currency":"'        + a["balance"]["currency"]   + '",' 
      r += '"name":"'            + a["owners"]                + '",' 
      r += '"label":"'           + a["label"]                 + '",' 
      r += '"swift_bic":"'       + "SWIFT_BIC"                + '",' 
      r += '"iban":"'            + a["IBAN"]                  + '",' 
      r += '"number":"'          + a["number"]                + '",'
      r += '"bankId":"'          + a["bank"]                  + '",' 
      r += '"lastUpdate":"'      + "2015-07-01T00:00:00.000Z" + '",'
      r += '"accountHolder":"'   + a["owners"]                + '"' #deprecated?
      r += '}' 
      # return result
      return r
  # return empty if not found 
  return '{}'
