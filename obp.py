import json
import uuid
# load mockup data from json file
with open('example_import.json') as data_file:
  data = json.load(data_file)
banks        = data['banks']
users        = data['users']
accounts     = data['accounts']
transactions = data['transactions']
fxRates      = data['fx_rates']
counterparties = data['counterparties']
transactionRequestTypes = data['transaction_request_types']

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
  email = args['user']
  password = args['password']
  if not email:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for u in users:
    if email == u['email'] and password == u['password']:
      # format result 
      s = { 'email'        : u['email'], 
            'displayName'  : u['display_name']}
      # create array for single result
      r  =  { 'count': '',
              'pager': '',
              'state': '',
              'target': 'user',
              'data' : [s] }
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
      s = { 'bankId'     : b['id'],
            'name'       : b['full_name'],
            'logo'       : b['logo'], 
            'url'        : b['website'] }
      # create array for single result
      r  =  { 'count': '',
              'pager': '',
              'state': '',
              'target': 'bank',
              'data' : [s] }
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
  l  = []
  for b in banks:
    # assemble the return string
    s = {   'bankId'       : b['id'],
            'name'         : b['full_name'],
            'logo'         : b['logo'],
            'url'          : b['website'] }

    l.append(s)
  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'banks',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j 

# getChallengeThreshold returns maximal amount of money 
# that can be transfered without the challenge
# accepts arguments:  transactionRequestType, accountId, currency, userId 
# returns string
#
def getChallengeThreshold(args):
  transactionRequestType  = args['transactionRequestType'] 
  accountId = args['accountId']
  currency = args['currency']
  userId = args['userId']

  s = { 'limit'    : '1000',
        'currency' : 'EUR' }

  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'challengeThreshold',
          'data' : [s] }

  # create json
  j = json.dumps(r)
  # return result
  return j


# createChallenge returns id of challenge
# accepts arguments:  transactionRequestType, userId, transactionRequestId, bankId, accountId
# returns string
#
def createChallenge(args):
  transactionRequestType  = args['transactionRequestType']
  userId = args['userId']
  transactionRequestId = args['transactionRequestId']
  bankId = args['bankId']
  accountId = args['accountId']

  s = { 'challengeId' : str(uuid.uuid4()) }

  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'challengeThreshold',
          'data' : [s] }

  # create json
  j = json.dumps(r)
  # return result
  return j

# validateChallengeAnswer returns is it challenge satisfied
# accepts arguments:  challengeId, hashOfSuppliedAnswer
# returns string
#
def validateChallengeAnswer(args):
  challengeId  = args['challengeId']
  hashOfSuppliedAnswer = args['hashOfSuppliedAnswer']

  s = { 'answer' : 'true' }

  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'challengeThreshold',
          'data' : [s] }

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
      s = {'transactionId'	: t['id'], 
	   'accountId'		: t['this_account']['id'], 
           'amount'		: t['details']['value'], 
	   'bankId'		: t['this_account']['bank'],
           'completedDate'	: t['details']['completed'], 
           'counterpartyId' 	: '2330135d-fca8-4268-838d-833074985209',
           'counterpartyName'	: 'counterparty_name',
           'currency'		: 'EUR', 
           'description'	: t['details']['description'], 
           'newBalanceAmount'	: t['details']['new_balance'], 
           'newBalanceCurrency': 'EUR', 
           'postedDate'	: t['details']['posted'], 
           'type'		: t['details']['type'], 
           'userId'		: '' 
	  }
      # create array for single result
      r  =  { 'count': '',
              'pager': '',
              'state': '',
              'target': 'transaction',
              'data' : [s] }
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
  #queryParams = args['queryParams']
  l  =  []
  for t in transactions:
    if bankId == t['this_account']['bank'] and accountId == t['this_account']['id']:
      # assemble the return string
      s = {'transactionId'	: t['id'], 
	   'accountId'		: t['this_account']['id'], 
           'amount'		: t['details']['value'], 
	   'bankId'		: t['this_account']['bank'],
           'completedDate'	: t['details']['completed'], 
           'counterpartyId' 	: '2330135d-fca8-4268-838d-833074985209',
           'counterpartyName'	: 'counterparty_name',
           'currency'		: 'EUR', 
           'description'	: t['details']['description'], 
           'newBalanceAmount'	: t['details']['new_balance'], 
           'newBalanceCurrency': 'EUR', 
           'postedDate'	: t['details']['posted'], 
           'type'		: t['details']['type'], 
           'userId'		: '' 
	  }
      l.append(s)
  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'transactions',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j 

# Saves a transaction with amount @amt and counterparty @counterparty for account @account. 
# Returns the id of the saved transaction.
def putTransaction(args):
  global transactions
  
  # assemble the persistent data
  transactionIdNew = str(uuid.uuid4())
  # 
  tranactionNew = {
      "id": transactionIdNew,
      "this_account": {
          "id": args['accountId'],
          "bank": "obp-bank-x-gh",
          "currency": args['currency']
      },
      "counterparty": {
          "name": "TESOBE",
          "other_account_id": args['otherAccountId'],
          "other_account_currency": args['otherAccountCurrency']
      },
      "details": {
          "type": args['transactionType'],
          "description": args['description'],
          "posted": "",
          "completed": "",
          "new_balance": "",
          "value": args['amount']
      }
  }
  
  # append new element to the transactions attribute
  transactions.append(tranactionNew)
  # write the Json to lcal JSON file "example_import.json"
  with open('example_import.json', 'w') as f:
      json.dump(data, f)
  
  # assemble the return string
  s = {'transactionId': transactionIdNew}
  # create array for single result
  r = {'count': '',
       'pager': '',
       'state': '',
       'target': 'transaction',
       'data': [s]}
  # create json
  j = json.dumps(r)
  # return result
  return j 

# getBankAccount returns bank account data 
# accepts arguments: bankId and accountId
# returns string
#
def getAccount(args):
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
      s = { 'accountId'			: a['id'], 
            'bankId'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balanceAmount'    		: a['balance']['amount'],
            'balanceCurrency'           : a['balance']['currency'],
            'iban'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
      # create array for single result 
      r  =  { 'count': '',
              'pager': '',
              'state': '',
              'target': 'account',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''})

# getAccounts returns all accounts owned by user 
# accepts arguments: userId 
# returns string
#
def getAccounts(args):
  global accounts 
  # get arguments
  if 'bankId' in args: 
    bankId = args['bankId']
  if 'userId' in args: 
    userId = args['userId']
  if not userId or not bankId:
    return json.dumps( {'error' : 'no argument given'} )
  l = []
  for a in accounts:
    if (userId in a['owners'] and bankId == a['bank']):
      # assemble the return string
      s = { 'accountId'     			: a['id'], 
            'bankId'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balanceAmount'             : a['balance']['amount'],
            'balanceCurrency'           : a['balance']['currency'],
            'iban'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
      l.append(s)
  r  =  { 'count': '',
          'pager': '',
          'state': '',
          'target': 'accounts',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j 

# return the latest single FXRate data specified by the fields: fromCurrencyCode and toCurrencyCode.
# If it is not found by (fromCurrencyCode, toCurrencyCode) order, it will try (toCurrencyCode, fromCurrencyCode) order.
# accepts string fromCurrencyCode and toCurrencyCode as arguments
# returns string
#

def getCurrentFxRate(args):
  global fxRates 
  # get argument
  fromCurrencyCode = args['fromCurrencyCode']
  toCurrencyCode = args['toCurrencyCode']
  if not fromCurrencyCode:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  if not toCurrencyCode:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for f in fxRates:
    # find FXRate by (fromCurrencyCode, toCurrencyCode), the normal order  
    if fromCurrencyCode == f['from_currency_code'] and toCurrencyCode == f['to_currency_code']:
      # assemble the return string
      s = { 'from_currency_code'        : f['from_currency_code'],
            'to_currency_code'          : f['to_currency_code'],
            'conversion_value'          : f['conversion_value'], 
            'inverse_conversion_value'  : f['inverse_conversion_value'],
            'effective_date'            : f['effective_date']}
      # create array for single result
      r  =  { 'count': '',
              'pager': '',
              'state': '',
              'target': 'fx',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j 
    # find FXRate by (toCurrencyCode, fromCurrencyCode), the reverse order
    elif toCurrencyCode  == f['from_currency_code'] and  fromCurrencyCode== f['to_currency_code']:
      # assemble the return string
      s = { 'from_currency_code'        : f['to_currency_code'],
            'to_currency_code'          : f['from_currency_code'],
            'conversion_value'          : f['conversion_value'], 
            'inverse_conversion_value'  : f['inverse_conversion_value'],
            'effective_date'            : f['effective_date']}
      # create array for single result
      r  =  { 'count': 1,
              'pager': '',
              'state': '',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j
  # return empty if not found 
  return json.dumps({'':''})

# getCounterpartyByCounterpartyId returns single Counterparty data
# accepts string counterpartyId as argument
# returns string
#
def getCounterpartyByCounterpartyId(args):
  global counterparties 
  # get argument
  counterpartyId = args['counterpartyId']
  if not counterpartyId:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for c in counterparties:
    if counterpartyId == c['counterparty_id']:
      # assemble the return string
      s = { 'name'                          : c['name'],
            'created_by_user_id'            : c['created_by_user_id'],
            'this_bank_id'                   : c['this_bank_id'], 
            'this_account_id'               : c['this_account_id'],
            'this_view_id'                   : c['this_view_id'],
            'other_bank_id'                  : c['other_bank_id'],
            'other_account_id'              : c['other_account_id'],
            'other_account_provider'        : c['other_account_provider'],
            'counterparty_id'               : c['counterparty_id'],
            'other_bank_routing_scheme'     : c['other_bank_routing_scheme'],
            'other_account_routing_scheme'  : c['other_account_routing_scheme'],
            'other_bank_routing_address'    : c['other_bank_routing_address'],
            'other_account_routing_address' : c['other_account_routing_address'],
            'is_beneficiary'                : c['is_beneficiary']}
      # create array for single result
      r  =  { 'count': 1,
              'pager': '',
              'state': '',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''}) 
    
# getCounterpartyByIban returns single Counterparty data
# accepts string Iban(otherAccountRoutingAddress) as argument
# (This is a helper method that assumes OtherAccountRoutingScheme=IBAN)
# returns string
#
def getCounterpartyByIban(args):
  global counterparties 
  # get argument
  otherAccountRoutingAddress = args['otherAccountRoutingAddress']
  otherAccountRoutingScheme  = args['otherAccountRoutingScheme']
  if not otherAccountRoutingAddress or not otherAccountRoutingScheme:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for c in counterparties:
    if otherAccountRoutingAddress == c['other_account_routing_address'] and otherAccountRoutingScheme == c['other_account_routing_scheme']:
      # assemble the return string
      s = { 'name'                          : c['name'],
            'created_by_user_id'            : c['created_by_user_id'],
            'this_bank_id'                  : c['this_bank_id'], 
            'this_account_id'               : c['this_account_id'],
            'this_view_id'                  : c['this_view_id'],
            'other_bank_id'                 : c['other_bank_id'],
            'other_account_id'              : c['other_account_id'],
            'other_account_provider'        : c['other_account_provider'],
            'counterparty_id'               : c['counterparty_id'],
            'other_bank_routing_scheme'     : c['other_bank_routing_scheme'],
            'other_account_routing_scheme'  : c['other_account_routing_scheme'],
            'other_bank_routing_address'    : c['other_bank_routing_address'],
            'other_account_routing_address' : c['other_account_routing_address'],
            'is_beneficiary'                : c['is_beneficiary']}
      # create array for single result
      r  =  { 'count': 1,
              'pager': '',
              'state': '',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''}) 
    
# getTransactionRequestTypeCharge returns single Charge data
# accepts arguments: bankId, accountId, viewId and transactionRequestType
# returns string
#
def getTransactionRequestTypeCharge(args):
  global transactionRequestTypes 
  # get argument
  # It just for test reponse, no authenticate or exsiting check here
  bankId = args['bankId']
  accountId  = args['accountId']
  viewId  = args['viewId']
  transactionRequestType  = args['transactionRequestType']
  
  if not transactionRequestType:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for t in transactionRequestTypes:
    if transactionRequestType == t['transaction_request_type_id']:
      # assemble the return string
      s = { 
            'transaction_request_type_id'    : t['transaction_request_type_id'],
            'bank_id'    : t['bank_id'],
            'charge_amount'    : t['charge_amount'],
            'charge_summary'   : t['charge_summary'], 
            'charge_currency'  : t['charge_currency']}
      # create array for single result
      r  =  { 'count': 1,
              'pager': '',
              'state': '',
              'data' : [s] }
      # create json
      j = json.dumps(r)
      # return result
      return j 
  # return empty if not found 
  return json.dumps({'':''})     
