# Define signer address
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


def singn_(seed, amount, destination, tag, client):
    my_secret = os.getenv(seed)
    wallet = Wallet(seed=seed, sequence=17)
    print(wallet)

    test_xaddress = addresscodec.classic_address_to_xaddress(destination, tag=tag, is_test_network=True)
    print("\nClassic address:\n\n", wallet.classic_address)
    print("X-address:\n\n", test_xaddress)

    result = xrpl.account.get_account_info(wallet.classic_address, client).result
    print(json.dumps(result, indent=4, sort_keys=True))
    sequence = result["account_data"]["Sequence"]
    my_payment = Payment(
        account=wallet.classic_address,
        amount=xrp_to_drops(amount),
        fee="10",
        destination=test_xaddress,
        # destination_tag=tag,
        sequence=sequence
    )
    print("Payment object:", my_payment)
    # signed = xrpl.transaction.safe_sign_transaction(my_payment, wallet)

    my_tx_payment_signed = safe_sign_and_autofill_transaction(my_payment, wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)

    print(json.dumps(tx_response.result, indent=4, sort_keys=True))


def account_tx(account_address, client):
    acct_info = AccountInfo(
        account=account_address,
        ledger_index="validated",
        strict=True,
    )
    response = client.request(acct_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(result, indent=4, sort_keys=True))

# Address:rExVyCkpHjabeMHSVmahgfPLsCbX7KrJ5F,Secret:shD1S7vKy1ifwoR17dHMYi8AL4ZHJ
# Address:rDswhJe76buxKLZAxnNWPLnBi947TYmWzQ,Secret:sn4EPFHCN23BWf3GUbth4kKMpcFro


if __name__ == '__main__':
    JSON_RPC_URL = "https://s.devnet.rippletest.net:51234"
    client = JsonRpcClient(JSON_RPC_URL)
    singn_("shD1S7vKy1ifwoR17dHMYi8AL4ZHJ", 10, "rDswhJe76buxKLZAxnNWPLnBi947TYmWzQ", 1999, client)
    account_tx("rDswhJe76buxKLZAxnNWPLnBi947TYmWzQ", client)
