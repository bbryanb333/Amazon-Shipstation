SELLER_ID	= 'A895K0WHLWP9V'
ACCESS_KEY	= 'AKIAI35HQTUTVNDKK3EA'
SECRET_KEY	= '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'
api_key = 'edbb945e7b004d1f801a92a707d656ca'
api_secret = '4bd53686988446f1a6a594feae72d0e3'
MWS_AUTH_TOKEN = 'amzn.mws.f8ba0128-5b02-0ac1-c637-19fac9a77fec'

import requests, zipfile, io, json
import mws, os
from pyshipstation.shipstation.api import *
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler



def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [indict]




def Send_Request():
    
    created_after = datetime.datetime.utcnow() - datetime.timedelta(hours=48)
    created_before= datetime.datetime.utcnow() - datetime.timedelta(hours=.05)
    print(created_after)
    print(created_before)
    orders_api = mws.Orders(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        account_id=SELLER_ID,
        auth_token=MWS_AUTH_TOKEN

    )

    order_statuses = [
            "PendingAvailability",
            "Unshipped",
        ]

    orders = orders_api.list_orders(marketplaceids=['ATVPDKIKX0DER'], orderstatus= None, created_after = created_after, created_before = created_before)



    request = ""
    sku = ""
    title = ""
    quantity = ""
    unit_price = Decimal("0")
    shipping = Decimal("0")
    tax = Decimal("0")
    order_id = ""
    date = ""
    shipping_service = ""
    city = ""
    postal_code = ""
    state = ""
    country = ""
    buyer_name = ""
    A1 = ""
    A2 = ""
    A3 = ""

    ss = ShipStation(key=api_key, secret=api_secret)
    

    if orders.parsed.Orders != {}:
        to_parse =  False
        loops = 0
        if(isinstance(orders.parsed.Orders.Order, list)):
            to_parse = True
            loops = len(orders.parsed.Orders.Order)
            #print("parsing")



        for i in range(loops):

            if(to_parse):
                for _ in dict_generator(orders.parsed.Orders.Order[i]):
                    if "PurchaseDate" in _:
                        date = _[-1]
                    if ("ShippingAddress" in _ and "City" in _):
                        city = _[-1]
                    if ("ShippingAddress" in _ and "StateOrRegion" in _):
                        state = _[-1]
                    if ("ShippingAddress" in _ and "CountryCode" in _):
                        country = _[-1]
                    if ("ShippingAddress" in _ and "PostalCode" in _):
                        postal_code = _[-1]
                    if ("ShippingAddress" in _ and "Name" in _):
                        buyer_name = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine1" in _):
                        A1 = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine2" in _):
                        A2 = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine3" in _):
                        A3 = _[-1]
                    if ("ShipmentServiceLevelCategory" in _ ):
                        shipping_service = _[-1]
                    #print(_)
                response = orders_api.list_order_items(orders.parsed.Orders.Order[i].AmazonOrderId)
            else:
                for _ in dict_generator(orders.parsed.Orders.Order):
                    if "PurchaseDate" in _ :
                        date = _[-1]
                    if ("ShippingAddress" in _ and "City" in _):
                        city = _[-1]
                    if ("ShippingAddress" in _ and "StateOrRegion" in _):
                        state = _[-1]
                    if ("ShippingAddress" in _ and "CountryCode" in _):
                        country = _[-1]
                    if ("ShippingAddress" in _ and "PostalCode" in _):
                        postal_code = _[-1]
                    if ("ShippingAddress" in _ and "Name" in _):
                        buyer_name = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine1" in _):
                        A1 = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine2" in _):
                        A2 = _[-1]
                    if ("ShippingAddress" in _ and "AddressLine3" in _):
                        A3 = _[-1]
                    if ("ShipmentServiceLevelCategory" in _ ):
                        shipping_service = _[-1]
                    #print(_)
                response = orders_api.list_order_items(orders.parsed.Orders.Order.AmazonOrderId)

            #print(date)
    
            for _ in dict_generator(response.parsed):
                if "CustomizedURL" in _:
                    request = _[-1]
                if "Title" in _:
                    title = _[-1]
                if "SellerSKU" in _:
                    sku = _[-1]
                if ("ItemPrice" in _ and "Amount" in _):
                     unit_price = _[-1]
                if ("ItemTax" in _ and "Amount" in _):
                    tax = _[-1]
                if "AmazonOrderId" in _:
                    order_id = _[-1]
                if ("ShippingPrice" in _ and "Amount" in _):
                    shipping = _[-1]
                if ("QuantityOrdered" in _):
                    quantity = _[-1]
                #print(_)

            initials = None
            name = None
            extra = None
            #order_id = order_id + 'test1'
            if(request != ""):
                r = requests.get(request)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                jsonpath = ""
                for i in z.namelist():
                    if i.endswith(".json"):
                        jsonpath = i
                z.extractall("C:/Amazon Request/zips")
                f = open("C:/Amazon Request/zips/" + jsonpath)
                #print(jsonpath)
                data = json.load(f)
                f.close()
                textfound = False
                fieldfound = False
                nextfield = ""
                custom = {}
                for _ in dict_generator(data):
                    print(_)
                    if fieldfound:
                        custom[nextfield] = _[-1]
                        fieldfound = False
                    if textfound:
                        nextfield = _[-1]
                        fieldfound = True 
        
                    if _[-1] == "TextCustomization":
                        textfound = True
                    else:
                        textfound = False

                if 'Initial' in custom:
                    initials = custom["Initial"]

                if 'Name' in custom:
                    name = custom["Name"]

                #extra= custom["extra"]
            
            

                order_check = ss.fetch_orders(parameters ={'order_number': order_id})
                #print(order_check.json())
                if (order_check.json()['total'] == 0):
                    ss_order = ShipStationOrder(order_number= order_id, amount_paid=unit_price, tax = tax, shipping = shipping, customer_notes=initials, internal_notes=name )
                    ss_order.set_status('awaiting_shipment')
    

                    shipping_address = ShipStationAddress(name=buyer_name, street1 = A1, street2 = A2, street3 = A3, city = city, state = state, postal_code = postal_code, country = country )
                    ss_order.set_shipping_address(shipping_address)


                    billing_address = ShipStationAddress(name=buyer_name, street1 = A1, street2 = A2, street3 = A3, city = city, state = state, postal_code = postal_code, country = country )
                    ss_order.set_billing_address(billing_address)


                    ss_item = ShipStationItem(
                    sku=sku,
                    name=title,
                    quantity=quantity,
                    unit_price=unit_price
                    )


                    ss_order.add_item(ss_item)
                    ss_order.set_order_date(date=date)

                    ss.add_order(ss_order)
                    print("added order")
                


            
            textfound = False
            fieldfound = False
            nextfield = ""
            custom = {}
            request = ""
            sku = ""
            title = ""
            quantity = ""
            unit_price = Decimal("0")
            shipping = Decimal("0")
            tax = Decimal("0")
            order_id = ""
            date = ""
            shipping_service = ""
            city = ""
            postal_code = ""
            state = ""
            country = ""
            buyer_name = ""
            A1 = ""
            A2 = ""
            A3 = ""
            initials = None
            name = None
            extra = None
            #time.sleep(1)

            
    ss.submit_orders();
    print("Done")
#scheduler = BlockingScheduler()
#scheduler.add_job(Send_Request, 'interval', minutes = 15)
#scheduler.start()

Send_Request()