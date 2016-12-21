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
  email = args['name']
  password = args['password']
  if not email:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  for u in users:
    if email == u['email'] and password == u['password']:
      # format result 
      s = { 'email'        : u['email'], 
            'display_name' : u['display_name'] } #, 
            #'roles'       : u['roles'] }
      # create array for single result
      r  =  { 'count': 1,
              'pager': '',
              'state': '',
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
  r  =  { 'count': 1,
          'pager': '',
          'state': '',
          'data' : l }
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
      s = { 'id'              : t['id'], 
            'this_account'    : { 
		'id'   : t['this_account']['id'], 
		'bank' : t['this_account']['bank']
            },
            'counterparty'    : {
                'name' : 'counterparty_name',
                'account_number' : '2330135d-fca8-4268-838d-833074985209'
	    },
            'details'	      : {
         	'type'        : t['details']['type'], 
            	'description' : t['details']['description'], 
            	'posted'      : t['details']['posted'], 
            	'completed'   : t['details']['completed'], 
            	'value'       : t['details']['value'], 
            	'new_balance' : t['details']['new_balance'], 
	    } 
	}
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
  l  =  []
  for t in transactions:
    if bankId == t['this_account']['bank'] and accountId == t['this_account']['id']:
      # assemble the return string
      s = { 'id'              : t['id'], 
            'this_account'    : { 
		'id'   : t['this_account']['id'], 
		'bank' : t['this_account']['bank']
            },
            'counterparty'    : {
                'name' : 'counterparty_name',
                'account_number' : '2330135d-fca8-4268-838d-833074985209'
	    },
            'details'	      : {
         	'type'        : t['details']['type'], 
            	'description' : t['details']['description'], 
            	'posted'      : t['details']['posted'], 
            	'completed'   : t['details']['completed'], 
            	'value'       : t['details']['value'], 
            	'new_balance' : t['details']['new_balance'], 
	    } 
	  }
      l.append(s)
  r  =  { 'count': 1,
          'pager': '',
          'state': '',
          'data' : l }
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
      s = { 'id'     			: a['id'], 
            'bank'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balance'    		: { 
		'amount'   : a['balance']['amount'],
                'currency' : a['balance']['currency'] 
	    },
            'IBAN'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
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

# getBankAccountis returns bank accounts 
# accepts arguments: list of bankIds and list of accountIds
# returns string
#
def getBankAccounts(args):
  global accounts 
  # get arguments
  bankIds = []
  if 'bankIds' in args: 
    bankIds = args['bankIds'].split(',')
  accountIds = [] 
  if 'accountIds' in args: 
    accountIds = args['accountIds'].split(',')
  if not bankIds and not accountIds:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  l = []
  for a in accounts:
    if ( a['id'] in accountIds and a['bank'] in bankIds ): 
      # assemble the return string
      s = { 'id'     			: a['id'], 
            'bank'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balance'    		: { 
		'amount'   : a['balance']['amount'],
                'currency' : a['balance']['currency'] 
	    },
            'IBAN'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
      # add to result
      l.append(s)
  r  =  { 'count': 1,
          'pager': '',
          'state': '',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j 
  # return empty if not found 
  return json.dumps({'':''})


# getUserAccounts returns all accounts owned by user 
# accepts arguments: name 
# returns string
#
def getUserAccounts(args):
  global accounts 
  # get arguments
  if 'name' in args: 
    name = args['name']
  if not name:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  l = []
  for a in accounts:
    if (name in a['owners']):
      # assemble the return string
      s = { 'id'     			: a['id'], 
            'bank'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balance'    		: { 
		'amount'   : a['balance']['amount'],
                'currency' : a['balance']['currency'] 
	    },
            'IBAN'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
      l.append(s)
  r  =  { 'count': 1,
          'pager': '',
          'state': '',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j 

# getAllAccounts returns all accounts user can view
# accepts arguments: name 
# returns string
#
def getPublicAccounts(args):
  global accounts 
  # get arguments
  if 'name' in args: 
    name = args['name']
  if not name:
    # return error if empty
    return json.dumps( {'error' : 'no argument given'} )
  l = []
  for a in accounts:
    print ( a['generate_public_view'])
    if ( a['generate_public_view'] == True and name not in a['owners'] ):
      # assemble the return string
      s = { 'id'     			: a['id'], 
            'bank'       		: a['bank'],
            'label'      		: a['label'],
            'number'     		: a['number'],
            'type'       		: a['type'],
            'balance'    		: { 
		'amount'   : a['balance']['amount'],
                'currency' : a['balance']['currency'] 
	    },
            'IBAN'       		: a['IBAN'],
            'owners'     		: a['owners'],
            'generate_public_view'      : a['generate_public_view'],
	    'generate_accountants_view' : a['generate_accountants_view'],
            'generate_auditors_view'    : a['generate_auditors_view']
      }
      l.append(s)
  r  =  { 'count': 1,
          'pager': '',
          'state': '',
          'data' : l }
  # create json
  j = json.dumps(r)
  # return result
  return j
