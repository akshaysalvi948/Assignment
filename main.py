import flask
from flask import request, jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required
from flask_bcrypt import Bcrypt 
from flask_cors import CORS

import datetime
from datetime import timedelta
import dateutil
from dateutil.relativedelta import relativedelta, FR

import logger

# from urllib.request import HTTPError
from urllib.error import HTTPError
# from urllib3.request import HTTPError

import python_http_client

import pandas as pd

app = flask.Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

import flask_login

@app.route('/ProcessPayment_api', methods=['GET']) 
# @jwt_required
def ProcessPayment():

    try:

        if 'cardNumber' in request.args and 'cardHolder' in request.args and 'expireDate' in request.args and 'amount' in request.args:

            cardNumber = request.args['cardNumber']
            cardHolder = request.args['cardHolder']
            expireDate = request.args['expireDate']
            securityCode = request.args['securityCode']
            amount = int(request.args['amount'])

            expireDate = pd.to_datetime(expireDate)

            # print(" Length "+len(securityCode))
            print(len(securityCode))
            print(type(expireDate))

            expensivePay = True
            premiumPay = True

            assert int(len(securityCode)) == 3,"SecurityCode Should be 3 digit."
            assert amount > 0,"Amount Should be positive number."
            assert expireDate > datetime.date.today(),"ExpiryDate Should be more than Today."

            if amount > 0 and len(securityCode) == 3 and expireDate > datetime.date.today() :

                print( " cardNumber "+str(cardNumber) + 
                "\n cardHolder "+str(cardHolder) + 
                "\n expireDate "+str(expireDate) + 
                "\n amount "+str(amount))

                if amount < 20:
                    CheapPaymentGateway()

                elif amount > 21 and amount < 500:
                    if expensivePay == True:
                        ExpensivePaymentGateway()
                    else:
                        CheapPaymentGateway()

                elif amount > 500:
                    PremiumPaymentGateway()
                    count = 3
                    print(count)
                    for i in range(count):

                        if premiumPay == True:
                            premium = PremiumPaymentGateway()
                            if premium == None:
                                count-=1
                    

        return "Payment is processed"

    except Exception as e:
        print("Error : " + str(e))
        return "Error: " + str(e)
    
    # except urllib.error.HTTPError as he:
    #     print("Error : " + str(he))
    #     return "Error: " + str(he)

    # except (HTTPError, python_http_client.exception.BadRequestsError) as error:
    #     print(error)
              

@app.errorhandler(400)
def bad_request(error):
    return "400 error",400

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

def CheapPaymentGateway():
    return "Using CheapPaymentGateway"

def ExpensivePaymentGateway():
    return "Using ExpensivePaymentGateway"

def PremiumPaymentGateway():
    return "Using PremiumPaymentGateway"

if __name__=="__main__":
	app.debug = True
	app.run(host='127.0.0.1', port=8081)