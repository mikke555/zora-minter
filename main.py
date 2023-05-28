from web3 import Web3
from loguru import logger
from time import sleep
from random import randint, shuffle

MINT_ADDRESS = Web3.to_checksum_address('0xa5358A17F943f9fB20d1f8dCF5ED9A9770bB0698')
ZORA_MINT_FEE = '0.000777'
DATA = '0xefef39a10000000000000000000000000000000000000000000000000000000000000001'

logger.add(
    "debug.log",
    format="{time} | {message}",
    level="DEBUG",
)

def mint(key):
    RPC = 'https://rpc.ankr.com/eth'
    web3 = Web3(Web3.HTTPProvider(RPC))
    wallet = web3.eth.account.from_key(key)

    tx = {
       "chainId": web3.eth.chain_id,
       "from": wallet.address,
       "to": web3.to_checksum_address(MINT_ADDRESS),
       "value": web3.to_wei(ZORA_MINT_FEE, 'ether'),
       "gas": 200_000,
       "gasPrice": web3.eth.gas_price,
       # "gasPrice": web3.to_wei(randint(25, 35), "gwei"), 
       "nonce": web3.eth.get_transaction_count(wallet.address),
       "data": DATA,
    }

    signed_txn = wallet.sign_transaction(tx)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.info(f'Mint from {wallet.address} txn: {web3.to_hex(txn_hash)}')
   

def load_keys():
    with open("keys.txt", "r") as f:
        keys = [row.strip() for row in f]
        return keys
       

if __name__ == "__main__":
    keys = load_keys()
    logger.info(f"Loaded {len(keys)} keys")
    shuffle(keys)

    for i, key in enumerate(keys):
        try:
            mint(key)

            if i != len(keys) - 1:  # Check if not last iteration
                siesta_length = randint(20, 60) # time to sleep between wallets
                print(f"Sleeping for {siesta_length} sec")
                sleep(siesta_length)

        except Exception as e:
            logger.error(f"An error occurred while minting with key {key}: {str(e)}")

    logger.info("Finish")
