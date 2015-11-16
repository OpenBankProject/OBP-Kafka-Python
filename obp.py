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

# getTransactions returns transactions
# accepts arguments
# returns string
#
def getTransactions(args):
  # hardcoded values for transaction1 
  bankId          = "123"
  accountId       = "12345"
  transactionId   = "1"
  transactionType = "current"
  amount          = "10,000.00"
  currency        = "EUR"
  description     = "Test transaction"
  startDate       = "Fri Nov 13 17:57:02 CET 2015"
  finishDate      = "Fri Nov 13 17:57:04 CET 2015"
  balance         = "10,000.00"
  otherBankId     = "321"
  otherAccountId  = "54321"
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


# getBankAccount returns bank account data 
# accepts arguments: bankId and accountId
# returns string
#
def getBankAccount(args):
  # get argument
  bankId = args['bankId']
  accountId = args['accountId']
  if not bankId or not accountId:
    # return error if empty
    return '{error:"no argument given"}'
  if bankId == "123" and accountId == "12345":
    # hardcoded values for bankAccount1 
    accountId       = "12345"
    accountType     = "savings"
    balance         = "20,000.00"
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
    balance         = "15,000.00"
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
