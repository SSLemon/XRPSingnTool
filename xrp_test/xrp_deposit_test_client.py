# 用来模拟deposit发送端

import os
from xrpl.models.transactions import Payment
from xrpl.wallet import Wallet
# from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
import xrpl.transaction
from xrpl.models.requests.account_info import AccountInfo
import json
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.transaction import send_reliable_submission
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
import xrpl.account

url = "http://18.139.178.210:5005/"


def singn_(seed, amount, destination, tag):
    global url
    client = JsonRpcClient(url)
    wallet = Wallet(seed=seed, sequence=17)
    result = xrpl.account.get_account_info(wallet.classic_address, client).result
    # print(json.dumps(result, indent=4, sort_keys=True))
    sequence = result["account_data"]["Sequence"]
    my_payment = Payment(
        account=wallet.classic_address,
        amount=xrp_to_drops(amount),
        fee="10",
        destination=destination,
        destination_tag=tag,
        sequence=sequence
    )
    my_tx_payment_signed = safe_sign_and_autofill_transaction(my_payment, wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))


# test account for client
# Address
# rEqpEaL2rpdea2ziNy2E7a6Nyn63SXuwUj
# Secret
# spxGcHvdQvnuUpRS7Wb4pXb7rJta4

# dev account for server
# Address
# rDswhJe76buxKLZAxnNWPLnBi947TYmWzQ
if __name__ == '__main__':
    secret = "spxGcHvdQvnuUpRS7Wb4pXb7rJta4"
    destination = "rs9yKEd62AS5JPzGyHY8Chn1nZ1RJzUDFy"
    singn_(secret, 32, destination, 2)
