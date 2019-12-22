import threading
from train import predict_buyer
import numpy as np, random
import requests, websocket, json
import math
class BuyerAgent():
    def __init__(self, name, day=1, test=1, max_size=60):
        super().__init__()
        self._kill = threading.Event()
        self.rate_series = []
        self.name = name
        self.budget = 11000000
        self.dollar = 0
        self.status = 'not'
        self.results = [],
        self.day = day
        self.max_size = max_size
        self.test = test
        self.ws_uri = 'ws://127.0.0.1:8000/agent/ws/'+self.name+'/'
        self.seller = None
        self.buyer = None
        self.cost = 0.
        self.seller_quantity = 0
        self.pred = 0.
        self.dif = 0.
        
    
        self.quantity = 0.

    def on_open(self,ws):
        print("ONOPEN")
        r = requests.get("http://127.0.0.1:8000/main/rates/1/")
        results = r.json()
        self.results = list(self.results)
        self.results.extend(results)
        for result in results:
            self.rate_series.append([result['usd']])
        self.train()

    def run(self):
        def on_message(ws, message):
            self.on_message(ws, message)

        def on_open(ws):
            self.on_open(ws)
        ws = websocket.WebSocketApp(self.ws_uri,
                              on_message = on_message)
        ws.on_open = on_open
        ws.run_forever()

    def on_message(self,ws, message):
        print("WAITING NEXT MESSAGE")
        ws_message = json.loads(message)
        new_message = ws_message['message']
        if 'from_government' in new_message:
            self.seller = 'Government'
            self.cost = self.rate_series[-1][0]
            self.quantity = self.budget*self.dif/100/self.rate_series[-1][0]
            for other in new_message['others']:
                if other['cost'] < self.cost and other['is_seller'] and other['quantity'] >= self.quantity/2:
                    self.cost = other['cost']
                    self.seller = other['name']
                    self.seller_quantity = other['quantity']
            
            if self.pred > self.cost:
                self.buy()
            else:
                if 'quantity' not in new_message:
                    self.sell()
            self.cost = 0.
            self.seller_quantity = 0
                
        else:
            if new_message['buy']:
                self.budget += ((self.pred+self.rate_series)/2)* new_message['quantity']
                self.dollar -= new_message['quantity']
            else:   
                self.results.append(new_message)
                if len(self.rate_series) < self.max_size:
                    self.rate_series.append([new_message['usd']])
                else:
                    self.rate_series.pop(0)
                    self.rate_series.append([new_message['usd']])
                self.day += 1
                self.train()

    def train(self):
        self.pred = predict_buyer(np.array(self.rate_series), self.name)
        self.dif = abs(self.pred - self.rate_series[-1][0])
        
        if self.pred < self.rate_series[-1][0]:
            #send to agreement
            post_data = {
                'name': self.name,
                'day': self.day,
                'test_case': self.test,
                'is_seller': True,
                'cost': (self.pred + self.rate_series[-1][0]) / 2,
                'quantity': self.dollar / 2
            }
            pos_req = requests.post("http://127.0.0.1:8000/main/state/", data=post_data)
            print(pos_req.json())
        else:
            post_data = {
                'name': self.name,
                'day': self.day,
                'test_case': self.test,
                'is_seller': False,
                'cost': 0.,
                'quantity': 0.
            }
            pos_req = requests.post("http://127.0.0.1:8000/main/state/", data=post_data)
            print(pos_req.json())

    def sell(self):
        print("SELL")
        self.status = 'sell'
        self.quantity = self.dollar / 2
        post_data = {
            'name': self.name,
            'status': self.status,
            'prediction': self.pred,
            'current': self.rate_series[-1][0],
            'real_price': self.rate_series[-1][0],
            'from_government': False,
            'day': self.day,
            'test_case': self.test,
            'tenge': self.budget,
            'dollar': self.dollar,
            'quantity': self.quantity,
        }
        pos_req = requests.post("http://127.0.0.1:8000/main/", data=post_data)
        print(pos_req.json())

    def buy(self):
        print("BUY")
        self.status = 'buy'
        print("BUY1")
        self.quantity = self.budget*self.dif/100/self.rate_series[-1][0]
        
        if self.seller == 'Government':
            print("BUY2")
            self.budget -=  self.budget*self.dif/100
        else:
            if self.quantity > self.seller_quantity:
                print("BUY3")
                self.quantity = self.seller_quantity
            self.budget -=  self.quantity * self.cost
        print("BUY4")

        self.dollar += self.quantity

        post_data = {
            'name': self.name,
            'status': self.status,
            'prediction': self.pred,
            'current': self.rate_series[-1][0],
            'real_price': self.rate_series[-1][0],
            'day': self.day,
            'test_case': self.test,
            'tenge': self.budget,
            'dollar': self.dollar,
            'from_government': self.seller == 'Government',
            'seller': self.seller,
            'quantity': self.quantity,
        }

        pos_req = requests.post("http://127.0.0.1:8000/main/", data=post_data)
        print(pos_req.json())