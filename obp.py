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
  bank                      = "123"
  account                   = "12345"
  transactionId             = "1"
  transactionType           = "someType"
  amount                    = "10,000.00"
  newAccountBalance         = "10,000.00"
  currency                  = "Dollar"
  tStartDate                = "Fri Nov 13 17:57:02 CET 2015"
  tFinishDate               = "Fri Nov 13 17:57:04 CET 2015"
  description               = "Test transaction"
  counterpartyAccountHolder = "holder"
  counterpartyAccountNumber = "222"

  # assemble the return string
  r  = '{'
  r += 'bank:"'                      + bank                      + '",' 
  r += 'account:"'                   + account                   + '",' 
  r += 'transactionId:"'             + transactionId             + '",' 
  r += 'transactionType:"'           + transactionType           + '",' 
  r += 'amount:"'                    + amount                    + '",' 
  r += 'newAccountBalance:"'         + newAccountBalance         + '",' 
  r += 'currency:"'                  + currency                  + '",' 
  r += 'tFinishDate:"'               + tFinishDate               + '",' 
  r += 'tStartDate:"'                + tStartDate                + '",' 
  r += 'description:"'               + description               + '",' 
  r += 'counterpartyAccountHolder:"' + counterpartyAccountHolder + '",'
  r += 'counterpartyAccountNumber:"' + counterpartyAccountNumber + '"'
  r += '}' 
  # return result
  return r

