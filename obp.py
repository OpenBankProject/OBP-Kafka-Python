# use the provided functions for connecting to your data sources 

# getBank returns single bank data
# accepts string bankId as argument 
# returns string
#
def getBank(args):
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
  r += 'permalink:"'     + permalink     + '",' 
  r += 'fullBankName:"'  + fullBankName  + '",' 
  r += 'shortBankName:"' + shortBankName + '",' 
  r += 'logoURL:"'       + logoURL       + '",' 
  r += 'websiteURL:"'    + websiteURL    + '"'
  r += '}' 
  # return result
  return r

# getBanks returns list of all banks
# accepts no arguments
# returns string
#
def getBanks(args):
  # list of bankIds to return
  bankList  = ["123", "321"] 
  # opening bracket
  r  =  '{' 
  # loop over all bankIds
  for bank in bankList:
    # get bank data calling getBank with bankId as argument
    r += getBank({"bankId":bank})
    # add comma after each entry
    r += ','
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
  # hardcoded values for transaction1 
  if bankId == "obp-bank-x-gh" and accountId == "test-x" and transactionId == "1":
    bankId          = "obp-bank-x-gh"
    accountId       = "test-x"
    transactionId   = "1"
    transactionType = "current"
    amount          = "10000"
    currency        = "EUR"
    description     = "Test transaction"
    startDate       = "Fri Nov 13 17:57:02 CET 2015"
    finishDate      = "Fri Nov 13 17:57:04 CET 2015"
    balance         = "10000"
    otherBankId     = "obp-bank-y-gh"
    otherAccountId  = "test-y"
  elif bankId == "obp-bank-x-gh" and accountId == "test-x" and transactionId == "2":
    bankId          = "obp-bank-x-gh"
    accountId       = "test-x"
    transactionId   = "2"
    transactionType = "current"
    amount          = "2000"
    currency        = "EUR"
    description     = "Test transaction"
    startDate       = "Fri Nov 13 17:57:02 CET 2015"
    finishDate      = "Fri Nov 13 17:57:04 CET 2015"
    balance         = "12000"
    otherBankId     = "obp-bank-y-gh"
    otherAccountId  = "test-y"
  elif bankId == "obp-bank-y-gh" and accountId == "test-y" and transactionId == "3":
    bankId          = "obp-bank-y-gh"
    accountId       = "test-y"
    transactionId   = "3"
    transactionType = "current"
    amount          = "8000"
    currency        = "EUR"
    description     = "Test 2nd transaction"
    startDate       = "Fri Nov 14 17:57:02 CET 2015"
    finishDate      = "Fri Nov 14 17:57:04 CET 2015"
    balance         = "13000"
    otherBankId     = "obp-bank-x-gh"
    otherAccountId  = "test-x"
  else:
    # just two transactions in this demo
    return '{}'
  # assemble the return string
  r  = '{'
  r += 'bankId:"'          + bankId          + '",' 
  r += 'accountId:"'       + accountId       + '",' 
  r += 'transactionId:"'   + transactionId   + '",' 
  r += 'transactionType:"' + transactionType + '",' 
  r += 'amount:"'          + amount          + '",' 
  r += 'currency:"'        + currency        + '",' 
  r += 'description:"'     + description     + '",' 
  r += 'startDate:"'       + startDate       + '",' 
  r += 'finishDate:"'      + finishDate      + '",' 
  r += 'balance:"'         + balance         + '",' 
  r += 'otherBankId:"'     + otherBankId     + '",'
  r += 'otherAccountId:"'  + otherAccountId  + '"'
  r += '}' 
  # return result
  return r

# getTransactions returns list of transactions depending on queryParams
# accepts arguments: bankId, accountId, and queryParams
# returns string
#
def getTransactions(args):
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
    r += ','
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
  r += 'accountId:"'       + accountId       + '",' 
  r += 'accountType:"'     + accountType     + '",' 
  r += 'balance:"'         + balance         + '",' 
  r += 'currency:"'        + currency        + '",' 
  r += 'name:"'            + name            + '",' 
  r += 'label:"'           + label           + '",' 
  r += 'swift_bic:"'       + swift_bic       + '",' 
  r += 'iban:"'            + iban            + '",' 
  r += 'number:"'          + number          + '",'
  r += 'bankId:"'          + bankId          + '",' 
  r += 'lastUpdate:"'      + lastUpdate      + '",'
  r += 'accountHolder:"'   + accountHolder   + '"' #deprecated?
  r += '}' 
  # return result
  return r
