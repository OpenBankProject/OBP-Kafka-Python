import json
# load mockup data from json file
with open('example_import.json') as data_file:
  data = json.load(data_file)
banks        = data['banks']
users        = data['users']
accounts     = data['accounts']
transactions = data['transactions']

#
# use functions provided below as model for connecting to real data sources 
#

# getUser returns single user data 
# accepts strings email and password as arguments 
# returns string
#
def getUser(args):
  global users 
  # get arguments
  email = args['email']
  password = args['password']
  if not email:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for u in users:
    if email == u['email'] and password == u['password']:
      # format result 
      r = { 'email'        : u['email'], 
            'display_name' : u['display_name'], 
            'roles'        : u['roles'] }
      # create json
      j = json.dumps(r)
      # return json result
      return j 
  # return empty if not found 
  return json.dumps({'':''}) 

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
    return json.dumps( {'error' : 'no argument given'} )
  for b in banks:
    if bankId == b['id']:
      # assemble the return string
      s = { 'bankId'        : b['id'], 
            'shortBankName' : b['short_name'], 
            'fullBankName'  : b['full_name'], 
            'logoURL'       : b['logo'], 
            'websiteURL'    : b['website'] }
      # create array for single result 
      r = []
      r.append(s)
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''}) 

# getBanks returns list of all banks
# accepts no arguments
# returns string
#
def getBanks(args):
  global banks 
  r  =  [] 
  for b in banks:
    # assemble the return string
    s = { 'bankId'             : b['id'], 
          'shortBankName'      : b['short_name'], 
          'fullBankName'       : b['full_name'], 
          'logoURL'            : b['logo'], 
          'nationalIdentifier' : 'NATIONAL-IDENTIFIER',
          'swiftBic'           : 'SWIFT-BIC', 
          'websiteURL'         : b['website'] }
    r.append(s)
  # create json
  j = json.dumps(r)
  # return result
  return j 

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
    if bankId == t['this_account']['bank'] and accountId == t['this_account']['id'] and transactionId == t['id']:
      # assemble the return string
      s = { 'bankId'          : t['this_account']['bank'],
            'accountId'       : t['this_account']['id'],
            'transactionId'   : t['id'],
            'transactionType' : t['details']['type'],
            'amount'          : t['details']['value'],
            'currency'        : 'GBP',
            'description'     : t['details']['description'],
            'startDate'       : t['details']['posted'],
            'finishDate'      : t['details']['completed'],
            'balance'         : t['details']['new_balance'],
            'otherBankId'     : 'obp-bank-x-g',
            'otherAccountId'  : '2330135d-fca8-4268-838d-833074985209' }
      # create array for single result 
      r = []
      r.append(s)
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''}) 

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
  r  =  [] 
  for t in transactions:
    if bankId == t['this_account']['bank'] and accountId == t['this_account']['id']:
      # assemble the return string
      s = { 'bankId'          : t['this_account']['bank'], 
            'accountId'       : t['this_account']['id'], 
            'transactionId'   : t['id'], 
            'transactionType' : t['details']['type'], 
            'amount'          : t['details']['value'], 
            'currency'        : 'GBP', 
            'description'     : t['details']['description'], 
            'startDate'       : t['details']['posted'], 
            'finishDate'      : t['details']['completed'], 
            'balance'         : t['details']['new_balance'], 
            'otherBankId'     : 'obp-bank-x-g',
            'otherAccountId'  : '2330135d-fca8-4268-838d-833074985209' }
      r.append(s)
  # create json
  j = json.dumps(r)
  # return result
  return j 

# getBankAccount returns bank account data 
# accepts arguments: bankId and accountId
# returns string
#
def getBankAccount(args):
  global accounts 
  # get arguments
  bankId = ''
  if 'bankId' in args: 
    bankId = args['bankId']
  number = ''
  if 'number' in args: 
    number = args['number']
  accountId = ''
  if 'accountId' in args: 
    accountId = args['accountId']
  if not bankId and not accountId and not number:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for a in accounts:
    if (bankId == a['bank'] and accountId == a['id']) or \
       (bankId == a['bank'] and number == a['number']) or \
       (not bankId and accountId == a['id']) or \
       (not bankId and number    == a['number']): 
      # assemble the return string
      s = { 'accountId'     : a['id'], 
            'accountType'   : a['type'],
            'balance'       : a['balance']['amount'],
            'currency'      : a['balance']['currency'],
            'name'          : a['owners'][0],
            'label'         : a['label'],
            'swift_bic'     : 'SWIFT_BIC',
            'iban'          : a['IBAN'],
            'number'        : a['number'],
            'bankId'        : a['bank'],
            'lastUpdate'    : '2015-07-01T00:00:00.000Z',
            'accountHolder' : a['owners'][0] }
      # create array for single result 
      r = []
      r.append(s)
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''})
