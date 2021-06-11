# 用来模拟deposit接收端

import json
import requests
import time


url = "http://18.139.178.210:5005/"


# 利用Current_ledger index 减去 transaction ledger index 可以计算出 confirms.
def get_current_ledger_index():
    global url
    request_data = {"method": "ledger_current"}
    res = requests.post(url=url, data=json.dumps(request_data))
    print(res.json())
    return res.json()["result"]["ledger_current_index"]


# 筛选出上次记录的 ledger_index 以后的transactions, 利用其中的数据update data
def update_data(account_address, last_ledger_index):
    global url
    current_index = get_current_ledger_index()
    request_data = {"method": "account_tx",
                    "params": [{"account": account_address, "binary": False, "forward": False, "ledger_index_max": current_index,"ledger_index_min": last_ledger_index}]}
    res = requests.post(url=url, data=json.dumps(request_data))
    print(res.json())
    print(json.dumps(res.json()["result"]))

    # 此时更新数据库

    return current_index


# test account for server
# Address
# rs9yKEd62AS5JPzGyHY8Chn1nZ1RJzUDFy
# Secret
# sn1K8hdi888HVZnAaPyRd42VekvMX
if __name__ == '__main__':
    last_index = get_current_ledger_index()
    print("last_index : ", last_index)
    while True:
        # 每隔一定时间更新一次
        # 等待1秒
        time.sleep(1)
        last_index = update_data("rs9yKEd62AS5JPzGyHY8Chn1nZ1RJzUDFy", last_index)
