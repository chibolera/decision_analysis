import threading
import time
from buyer_agent import BuyerAgent
import sys

def run_agent(name, test_case, max_size):
    agent = BuyerAgent(name, test=test_case, max_size=max_size)
    agent.run()

if __name__== "__main__":
    run_agent(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))