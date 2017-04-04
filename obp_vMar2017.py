import json
import uuid

data = dict()


#
# use functions provided below as model for connecting to real data sources 
#

def getFuncName(data):
    jdata = json.loads(data)
    if 'action' in jdata:
        return json.loads(data)['action'].split('.')[1].replace('.', '') + json.loads(data)['action'].split('.')[2]


def getArguments(data):
    r = dict()
    args = json.loads(data)
    for item in args.items():
        k = item[0]
        v = item[1]
        if (k != "action"):
            r.update({k: v})
    return r


# getUser returns single user data 
# accepts strings email and password as arguments 
# returns string
#
# eg: http://127.0.0.1:8080/my/logins/direct
# getUserId -->  AuthUser.getResourceUserId -->kafkaUser <- getUserFromConnector -->getUser
# this one is special, it is used for external user. if it is not exsting in OBP locally, this method will call.
def getUser(args):
    global data
    users = data['users']
    # get arguments
    username = args['username']
    password = args['password']
    if not username:
        # return error if empty
        return json.dumps({'error': 'no argument given'})
    for u in users:
        if username == u['email'] and password == u['password']:
            # format result 
            s = {'errorCode': 'OBPS-001: ....',
                 'email': u['email'],
                 'displayName': u['displayName']}
            # create array for single result
            r = {'count': '',
                 'pager': '',
                 'state': '',
                 'target': 'user',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return json result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


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
        return json.dumps({'error': 'no argument given'})
    for b in banks:
        if bankId == b['id']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                'bankId': b['id'],
                 'name': b['fullName'],
                 'logo': b['logo'],
                 'url': b['website']}
            # create array for single result
            r = {'count': '',
                 'pager': '',
                 'state': '',
                 'target': 'bank',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


# getBanks returns list of all banks
# accepts no arguments
# returns string
#
def getBanks(args):
    global data
    banks = data['banks']
    l = []
    for b in banks:
        # assemble the return string
        s = {'errorCode': 'OBPS-001: ....',
             'bankId': b['id'],
             'name': b['fullName'],
             'logo': b['logo'],
             'url': b['website']}

        l.append(s)
    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'banks',
         'data': l}
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
    transactionRequestType = args['transactionRequestType']
    accountId = args['accountId']
    currency = args['currency']
    userId = args['userId']
    username = args['username']

    s = {'errorCode': 'OBPS-001: ....',
         'limit': '1000',
         'currency': 'EUR'}

    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'challengeThreshold',
         'data': [s]}

    # create json
    j = json.dumps(r)
    # return result
    return j


# getChargeLevel returns charge level 
# accepts arguments:  bankId, accountId, viewId, transactionRequestType, currency, userId, userName
# returns string
#
def getChargeLevel(args):
    transactionRequestType = args['transactionRequestType']
    accountId = args['accountId']
    currency = args['currency']
    userId = args['userId']
    username = args['username']

    s = {'errorCode': 'OBPS-001: ....',
         'amount': '0.001',
         'currency': 'EUR'}

    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'chargeLevel',
         'data': [s]}

    # create json
    j = json.dumps(r)
    # return result
    return j


# createChallenge returns id of challenge
# accepts arguments:  transactionRequestType, userId, transactionRequestId, bankId, accountId
# returns string
#
def createChallenge(args):
    transactionRequestType = args['transactionRequestType']
    userId = args['userId']
    username = args['username']
    transactionRequestId = args['transactionRequestId']
    bankId = args['bankId']
    accountId = args['accountId']

    s = {'errorCode': 'OBPS-001: ....',
         'challengeId': str(uuid.uuid4())}

    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'challengeThreshold',
         'data': [s]}

    # create json
    j = json.dumps(r)
    # return result
    return j


# validateChallengeAnswer returns is it challenge satisfied
# accepts arguments:  challengeId, hashOfSuppliedAnswer
# returns string
#
def validateChallengeAnswer(args):
    challengeId = args['challengeId']
    hashOfSuppliedAnswer = args['hashOfSuppliedAnswer']

    try:
        changToInt = int(hashOfSuppliedAnswer)
    except:
        return json.dumps({'error': 'Need a numeric TAN'})
    if changToInt <= 0:
        return json.dumps({'error': 'Need a positive TAN'})
    else:
        answer = "true"

    s = {'errorCode': 'OBPS-001: ....',
         'answer': answer}

    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'challengeThreshold',
         'data': [s]}

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
    bankId = args['bankId']
    accountId = args['accountId']
    transactionId = args['transactionId']
    for t in transactions:
        # these transactions are imported when create sandbox, the older ones.
        if 'thisAccount' in t:
            if bankId == t['thisAccount']['bank'] and accountId == t['thisAccount']['id'] and transactionId == t['id']:
                # assemble the return string
                s = {'errorCode': 'OBPS-001: ....',
                     'transactionId': t['id'],
                     'accountId': t['thisAccount']['id'],
                     'amount': t['details']['value'],
                     'bankId': t['thisAccount']['bank'],
                     'completedDate': t['details']['completed'],
                     'counterpartyId': '2330135d-fca8-4268-838d-833074985209',
                     'counterpartyName': 'counterpartyName',
                     'currency': 'EUR',
                     'description': t['details']['description'],
                     'newBalanceAmount': t['details']['newBalance'],
                     'newBalanceCurrency': 'EUR',
                     'postedDate': t['details']['posted'],
                     'type': t['details']['type'],
                     'userId': ''
                     }
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
        # this is for new transactions, when create transaction, there will be create new records.         
        elif 'fromAccountBankId' in t:
            if bankId == t['fromAccountBankId']and accountId == t['fromAccountId'] and transactionId == t['transactionId']:
                s = {'errorCode': 'OBPS-001: ....',
                     'transactionId': t['transactionId'],
                     'accountId': t['fromAccountId'],
                     'amount': t['transactionAmount'],
                     'bankId': t['fromAccountBankId'],
                     'completedDate': t['transactionPostedDate'],
                     'counterpartyId': t['toCounterpartyId'],
                     'counterpartyName':t['toCounterpartyName'],
                     'currency': t['transactionCurrency'],
                     'description': t['transactionDescription'],
                     'newBalanceAmount': '0.0',
                     'newBalanceCurrency': 'EUR',
                     'postedDate': t['transactionPostedDate'],
                     'type': t['type'],
                     'userId': t['userId']
                     }
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
    # return empty if not found 
    return json.dumps({'': ''})


# getTransactions returns list of transactions depending on queryParams
# accepts arguments: bankId, accountId, and queryParams
# returns string
#
def getTransactions(args):
    global data
    transactions = data['transactions']
    # get arguments
    bankId = args['bankId']
    accountId = args['accountId']
    # queryParams = args['queryParams']
    l = []
    for t in transactions:
        # these transactions are imported when create sandbox, the older ones.
        if 'thisAccount' in t:
            if bankId == t['thisAccount']['bank'] and accountId == t['thisAccount']['id']:
                # assemble the return string
                s = {'errorCode': 'OBPS-001: ....',
                     'transactionId': t['id'],
                     'accountId': t['thisAccount']['id'],
                     'amount': t['details']['value'],
                     'bankId': t['thisAccount']['bank'],
                     'completedDate': t['details']['completed'],
                     'counterpartyId': '2330135d-fca8-4268-838d-833074985209',
                     'counterpartyName': 'counterpartyName',
                     'currency': 'EUR',
                     'description': t['details']['description'],
                     'newBalanceAmount': t['details']['newBalance'],
                     'newBalanceCurrency': 'EUR',
                     'postedDate': t['details']['posted'],
                     'type': t['details']['type'],
                     'userId': ''
                     }
                l.append(s)
        # this is for new transactions, when create transaction, there will be create new records.       
        elif 'fromAccountBankId' in t:
             if bankId == t['fromAccountBankId']and accountId == t['fromAccountId']:
                # assemble the return string
                s = {'errorCode': 'OBPS-001: ....',
                     'transactionId': t['transactionId'],
                     'accountId': t['fromAccountId'],
                     'amount': t['transactionAmount'],
                     'bankId': t['fromAccountBankId'],
                     'completedDate': t['transactionPostedDate'],
                     'counterpartyId': t['toCounterpartyId'],
                     'counterpartyName':t['toCounterpartyName'],
                     'currency': t['transactionCurrency'],
                     'description': t['transactionDescription'],
                     'newBalanceAmount': '0.0',
                     'newBalanceCurrency': 'EUR',
                     'postedDate': t['transactionPostedDate'],
                     'type': t['type'],
                     'userId': t['userId']
                     }
                l.append(s)
    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'transactions',
         'data': l}
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
        "userId": args['userId'],
        "username": args['username'],
         #fromAccount
        "fromAccountName": args['fromAccountName'],
        "fromAccountId": args['fromAccountId'],
        "fromAccountBankId": args['fromAccountBankId'],
        
         #transaction details
        "transactionId": args['transactionId'],
        "transactionRequestType": args['transactionRequestType'],
        "transactionAmount": args['transactionAmount'],
        "transactionCurrency": args['transactionCurrency'],
        "transactionChargePolicy": args['transactionChargePolicy'],
        "transactionChargeAmount": args['transactionChargeAmount'],
        "transactionChargeCurrency": args['transactionChargeCurrency'],
        "transactionDescription": args['transactionDescription'],
        "transactionPostedDate": args['transactionPostedDate'],

        #toAccount or toCounterparty
        "toCounterpartyId": args['toCounterpartyId'],
        "toCounterpartyName": args['toCounterpartyName'],
        "toCounterpartyCurrency": args['toCounterpartyCurrency'],
        "toCounterpartyRoutingAddress": args['toCounterpartyRoutingAddress'],
        "toCounterpartyRoutingScheme": args['toCounterpartyRoutingScheme'],
        "toCounterpartyBankRoutingAddress": args['toCounterpartyBankRoutingAddress'],
        "toCounterpartyBankRoutingScheme": args['toCounterpartyBankRoutingScheme'],
        'type': 'AC'
    }

    # append new element to the transactions attribute
    transactions.append(tranactionNew)
    # write the Json to lcal JSON file "example_import_mar2017.json"
    with open('example_import_mar2017.json', 'w') as f:
        json.dump(data, f)

    # assemble the return string
    s = {'errorCode': 'OBPS-001: ....',
         'transactionId': args['transactionId']}
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
        return json.dumps({'error': 'no argument given'})
    for a in accounts:
        if (bankId == a['bank'] and accountId == a['id']) or \
                (bankId == a['bank'] and number == a['number']) or \
                (not bankId and accountId == a['id']) or \
                (not bankId and number == a['number']):
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'accountId': a['id'],
                 'bankId': a['bank'],
                 'label': a['label'],
                 'number': a['number'],
                 'type': a['type'],
                 'balanceAmount': a['balance']['amount'],
                 'balanceCurrency': a['balance']['currency'],
                 'iban': a['IBAN'],
                 'owners': a['owners'],
                 'generatePublicView': a['generatePublicView'],
                 'generateAccountantsView': a['generateAccountantsView'],
                 'generateAuditorsView': a['generateAuditorsView'],
                 'accountRoutingScheme': a['accountRoutingScheme'],
                 'accountRoutingAddress': a['accountRoutingAddress'],
                 'branchId': a['branchId']
                 }
            # create array for single result 
            r = {'count': '',
                 'pager': '',
                 'state': '',
                 'target': 'account',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


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
        return json.dumps({'error': 'no argument given'})
    l = []
    for a in accounts:
        if ((userId in a['owners'] or username in a['owners']) and bankId == a['bank']):
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'accountId': a['id'],
                 'bankId': a['bank'],
                 'label': a['label'],
                 'number': a['number'],
                 'type': a['type'],
                 'balanceAmount': a['balance']['amount'],
                 'balanceCurrency': a['balance']['currency'],
                 'iban': a['IBAN'],
                 'owners': a['owners'],
                 'generatePublicView': a['generatePublicView'],
                 'generateAccountantsView': a['generateAccountantsView'],
                 'generateAuditorsView': a['generateAuditorsView'],
                 'accountRoutingScheme': a['accountRoutingScheme'],
                 'accountRoutingAddress': a['accountRoutingAddress'],
                 'branchId': a['branchId']
                 }
            l.append(s)
    r = {'count': '',
         'pager': '',
         'state': '',
         'target': 'accounts',
         'data': l}
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
    fxRates = data['fxRates']
    # get argument
    fromCurrencyCode = args['fromCurrencyCode']
    toCurrencyCode = args['toCurrencyCode']
    if not fromCurrencyCode:
        # return error if empty
        return json.dumps({'error': 'no argument given'})
    if not toCurrencyCode:
        # return error if empty
        return json.dumps({'error': 'no argument given'})
    for f in fxRates:
        # find FXRate by (fromCurrencyCode, toCurrencyCode), the normal order  
        if fromCurrencyCode == f['fromCurrencyCode'] and toCurrencyCode == f['toCurrencyCode']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'fromCurrencyCode': f['fromCurrencyCode'],
                 'toCurrencyCode': f['toCurrencyCode'],
                 'conversionValue': f['conversionValue'],
                 'inverseConversionValue': f['inverseConversionValue'],
                 'effectiveDate': f['effectiveDate']}
            # create array for single result
            r = {'count': '',
                 'pager': '',
                 'state': '',
                 'target': 'fx',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # find FXRate by (toCurrencyCode, fromCurrencyCode), the reverse order
        elif toCurrencyCode == f['fromCurrencyCode'] and fromCurrencyCode == f['toCurrencyCode']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'fromCurrencyCode': f['toCurrencyCode'],
                 'toCurrencyCode': f['fromCurrencyCode'],
                 'conversionValue': f['conversionValue'],
                 'inverseConversionValue': f['inverseConversionValue'],
                 'effectiveDate': f['effectiveDate']}
            # create array for single result
            r = {'count': 1,
                 'pager': '',
                 'state': '',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
    # return empty if not found 
    return json.dumps({'': ''})


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
        return json.dumps({'error': 'no argument given'})
    for c in counterparties:
        if counterpartyId == c['counterpartyId']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'name': c['name'],
                 'createdByUserId': c['createdByUserId'],
                 'thisBankId': c['thisBankId'],
                 'thisAccountId': c['thisAccountId'],
                 'thisViewId': c['thisViewId'],
                 'counterpartyId': c['counterpartyId'],
                 'otherBankRoutingScheme': c['otherBankRoutingScheme'],
                 'otherBankRoutingAddress': c['otherBankRoutingAddress'],
                 'otherAccountRoutingScheme': c['otherAccountRoutingScheme'],
                 'otherAccountRoutingAddress': c['otherAccountRoutingAddress'],
                 'otherBranchRoutingScheme': c['otherBranchRoutingScheme'],
                 'otherBranchRoutingAddress': c['otherBranchRoutingAddress'],
                 'isBeneficiary': c['isBeneficiary']}
            # create array for single result
            r = {'count': 1,
                 'pager': '',
                 'state': '',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


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
    otherAccountRoutingScheme = args['otherAccountRoutingScheme']
    if not otherAccountRoutingAddress or not otherAccountRoutingScheme:
        # return error if empty
        return json.dumps({'error': 'no argument given'})
    for c in counterparties:
        if otherAccountRoutingAddress == c['otherAccountRoutingAddress'] and \
                        otherAccountRoutingScheme == c['otherAccountRoutingScheme']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                 'name': c['name'],
                 'createdByUserId': c['createdByUserId'],
                 'thisBankId': c['thisBankId'],
                 'thisAccountId': c['thisAccountId'],
                 'thisViewId': c['thisViewId'],
                 'counterpartyId': c['counterpartyId'],
                 'otherBankRoutingScheme': c['otherBankRoutingScheme'],
                 'otherBankRoutingAddress': c['otherBankRoutingAddress'],
                 'otherAccountRoutingScheme': c['otherAccountRoutingScheme'],
                 'otherAccountRoutingAddress': c['otherAccountRoutingAddress'],
                 'otherBranchRoutingScheme': c['otherBranchRoutingScheme'],
                 'otherBranchRoutingAddress': c['otherBranchRoutingAddress'],
                 'isBeneficiary': c['isBeneficiary']}
            # create array for single result
            r = {'count': 1,
                 'pager': '',
                 'state': '',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


# getTransactionRequestTypeCharge returns single Charge data
# accepts arguments: bankId, accountId, viewId and transactionRequestType
# returns string
#
def getTransactionRequestTypeCharge(args):
    global data
    transactionRequestTypes = data['transactionRequestTypes']
    # get argument
    # It just for test reponse, no authenticate or exsiting check here
    bankId = args['bankId']
    accountId = args['accountId']
    viewId = args['viewId']
    transactionRequestType = args['transactionRequestType']

    if not transactionRequestType:
        # return error if empty
        return json.dumps({'error': 'no argument given'})
    for t in transactionRequestTypes:
        if transactionRequestType == t['transactionRequestType']:
            # assemble the return string
            s = {'errorCode': 'OBPS-001: ....',
                'transactionRequestType': t['transactionRequestType'],
                'bankId': t['bankId'],
                'chargeCurrency': t['chargeCurrency'],
                'chargeAmount': t['chargeAmount'],
                'chargeSummary': t['chargeSummary']}
            # create array for single result
            r = {'count': 1,
                 'pager': '',
                 'state': '',
                 'data': [s]}
            # create json
            j = json.dumps(r)
            # return result
            return j
            # return empty if not found 
    return json.dumps({'': ''})


# getTransactionRequestStatusesImpl 
# accepts arguments: None
# returns string: 
def getTransactionRequestStatusesImpl(args):
    transactionRequestId = "1234567"

    s = {'errorCode': 'OBPS-001: ....',
        "transactionRequestId": transactionRequestId,
        "bulkTransactionsStatus": [
            {
                "transactionId": "1",
                "transactionStatus": "2",
                "transactionTimestamp": "3"
            },
            {
                "transactionId": "1",
                "transactionStatus": "2",
                "transactionTimestamp": "3"
            }
        ]
    }

    r = {'count': 1,
         'pager': '',
         'state': '',
         'data': [s]}

    # create json
    j = json.dumps(r)
    # return result
    return j
