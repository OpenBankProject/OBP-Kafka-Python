import json
import uuid
import obp_vMar2017

data = dict()

#
# use functions provided below as model for connecting to real data sources 
#

def getFuncName(data):
  jdata = json.loads(data)
  if 'target' in jdata:
    return json.loads(data)["name"]+(json.loads(data)["target"].title())
  else:
    return json.loads(data)["north"]

def getArguments(data):
  r = dict()
  args = json.loads(data)
  for item in args.items():
    k = item[0]
    v = item[1]
    if (k != "name" and k != "target"):
      r.update({k:v})
  return r


# getUser returns single user data 
# accepts strings email and password as arguments 
# returns string
#
def getUser(args):
  global data
  users = data['users']
  # get arguments
  username = args['username']
  password = args['password']
  if not username:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for u in users:
    if username == u['email'] and password == u['password']:
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
  global data
  banks = data['banks']
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
  global data
  banks = data['banks']
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
# accepts arguments:  bankId, accountId, viewId, transactionRequestType, currency, userId, userName
# returns string
#
def getChallengeThreshold(args):
  transactionRequestType  = args['transactionRequestType'] 
  accountId = args['accountId']
  currency = args['currency']
  userId = args['userId']
  username = args['username']

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

# getChargeLevel returns charge level 
# accepts arguments:  bankId, accountId, viewId, transactionRequestType, currency, userId, userName
# returns string
#
def getChargeLevel(args):
    transactionRequestType  = args['transactionRequestType']
    accountId = args['accountId']
    currency = args['currency']
    userId = args['userId']
    username = args['username']

    s = { 'amount'    : '0.001',
          'currency' : 'EUR' }

    r  =  { 'count': '',
            'pager': '',
            'state': '',
            'target': 'chargeLevel',
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
  username = args['username']
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
  global data
  transactions = data['transactions']
  # get arguments
  bankId  = args['bankId'] 
  accountId = args['accountId']
  transactionId = args['transactionId']
  for t in transactions:
    if 'this_account' in t:
      if bankId == t['this_account']['bank'] and accountId == t['this_account']['id'] and transactionId == t['id']:
        # assemble the return string
        s = {'transactionId'	    : t['id'],
	         'accountId'		    : t['this_account']['id'],
             'amount'		        : t['details']['value'],
	         'bankId'		        : t['this_account']['bank'],
             'completedDate'	    : t['details']['completed'],
             'counterpartyId' 	: '2330135d-fca8-4268-838d-833074985209',
             'counterpartyName'	: 'counterparty_name',
             'currency'		    : 'EUR',
             'description'	    : t['details']['description'],
             'newBalanceAmount'	: t['details']['new_balance'],
             'newBalanceCurrency' : 'EUR',
             'postedDate'	        : t['details']['posted'],
             'type'		        : t['details']['type'],
             'userId'		        : ''
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
  global data
  transactions = data['transactions']
  # get arguments
  bankId  = args['bankId'] 
  accountId = args['accountId']
  #queryParams = args['queryParams']
  l  =  []
  for t in transactions:
    if 'this_account' in t:
      if bankId == t['this_account']['bank'] and accountId == t['this_account']['id']:
        # assemble the return string
        s = {'transactionId'	: t['id'],
           'accountId'		    : t['this_account']['id'],
           'amount'		        : t['details']['value'],
           'bankId'		        : t['this_account']['bank'],
           'completedDate'	    : t['details']['completed'],
           'counterpartyId'     : '2330135d-fca8-4268-838d-833074985209',
           'counterpartyName'	: 'counterparty_name',
           'currency'		    : 'EUR',
           'description'	    : t['details']['description'],
           'newBalanceAmount'   : t['details']['new_balance'],
           'newBalanceCurrency' : 'EUR',
           'postedDate'	        : t['details']['posted'],
           'type'		        : t['details']['type'],
           'userId'		        : ''
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
  global data
  transactions = data['transactions']
  
  # assemble the persistent data
  transactionIdNew = str(uuid.uuid4())

  tranactionNew = {
      "id": transactionIdNew,
      "description": args['description'],
      "transaction_request_type": args['transactionRequestType'],
      "to_currency": args['toCurrency'],
      "to_amount": args['toAmount'],
      "charge_policy": args['chargePolicy'],
      "from_bank_id": args['fromBankId'],
      "from_account_id": args['fromAccountId'],
      "to_bank_id": args['toBankId'],
      "to_account_id": args['toAccountId'],
      "to_counterparty_id": args['toCounterpartyId'],
      "to_counterparty_other_bank_routing_address": args['toCounterpartyOtherBankRoutingAddress'],
      "to_counterparty_other_account_routing_address": args['toCounterpartyOtherAccountRoutingAddress'],
      "to_counterparty_other_account_routing_scheme": args['toCounterpartyOtherAccountRoutingScheme'],
      "to_counterparty_other_bank_routing_scheme": args['toCounterpartyOtherBankRoutingScheme'],
      "type": args['type']
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
  global data
  accounts = data['accounts']
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
      s = {'accountId': a['id'],
           'bankId': a['bank'],
           'label': a['label'],
           'number': a['number'],
           'type': a['type'],
           'balanceAmount': a['balance']['amount'],
           'balanceCurrency': a['balance']['currency'],
           'iban': a['IBAN'],
           'owners': a['owners'],
           'generate_public_view': a['generate_public_view'],
           'generate_accountants_view': a['generate_accountants_view'],
           'generate_auditors_view': a['generate_auditors_view'],
           'accountRoutingScheme': a['accountRoutingScheme'],
           'accountRoutingAddress': a['accountRoutingAddress'],
           'branchId': a['branchId']
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
  global data
  accounts = data['accounts']
  # get arguments
  if 'bankId' in args:
    bankId = args['bankId']
  if 'userId' in args:
    userId = args['userId']
  if 'username' in args:
    username = args['username']
  else:
    username = ""
  if not userId or not username or not bankId:
    return json.dumps( {'error' : 'no argument given'} )
  l = []
  for a in accounts:
    if ( (userId in a['owners'] or username in a['owners'] ) and bankId == a['bank']):
      # assemble the return string
      s = {'accountId': a['id'],
           'bankId': a['bank'],
           'label': a['label'],
           'number': a['number'],
           'type': a['type'],
           'balanceAmount': a['balance']['amount'],
           'balanceCurrency': a['balance']['currency'],
           'iban': a['IBAN'],
           'owners': a['owners'],
           'generate_public_view': a['generate_public_view'],
           'generate_accountants_view': a['generate_accountants_view'],
           'generate_auditors_view': a['generate_auditors_view'],
           'accountRoutingScheme': a['accountRoutingScheme'],
           'accountRoutingAddress': a['accountRoutingAddress'],
           'branchId': a['branchId']
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
  global data
  fxRates = data['fx_rates']
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
  global data
  counterparties = data['counterparties']
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
            'this_bank_id'                  : c['this_bank_id'],
            'this_account_id'               : c['this_account_id'],
            'this_view_id'                  : c['this_view_id'],
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
  global data
  counterparties = data['counterparties']
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
  global data
  transactionRequestTypes = data['transaction_request_types']
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

# see details in bp_vMar2017.getTransactionRequestStatusesImpl
def getTransactionRequestStatusesImpl(args):
    obp_vMar2017.getTransactionRequestStatusesImpl
