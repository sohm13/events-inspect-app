from events_inpsect.blockchain_scan import Pair, BlockChainScan
from events_inpsect.web3_provider import MyWeb3
from events_inpsect.helper import get_pairs_config, get_pairs_async
from events_inpsect.utils import get_block_by_timestamp, get_block_by_timestamp_async
from events_inpsect.contract_calls import get_erc20_contract
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

import time



async def run_tasks( tasks):
    response = await asyncio.gather(*tasks)
    return response

async def run(web3: MyWeb3):
    pair_params = get_pairs_config(network_name)

    tik = time.time()
    pairs_dex = await get_pairs_async(web3, pair_params.tokens_other, pair_params.tokens_mixin, pair_params.factories)
    pairs = [Pair(address=pd.address, symbol=pd.label) for pd in pairs_dex]
    print('pair time:', time.time() - tik, 'pairs len:', len(pairs))
    p_address = [[p.token0.address, p.token1.address] for p in pairs_dex]


    scan = BlockChainScan(web3)


    tik = time.time()
    timestamp_start = 1656000000
    step = 50

    [block_start, block_end] = await asyncio.gather(
        get_block_by_timestamp_async(web3, timestamp_start, 18943612-50),
        get_block_by_timestamp_async(web3, timestamp_start+step, 18943612-50)
    )

    print('blocks for scan', block_end-block_start)

    # blocks_range = [ [block_start, block_end] for _ in range(len(pairs))]
    pairs_data = scan.get_scan_event_from_blocks(blocks_range, pairs)
    # pairs_data = scan.get_scan_event_from_blocks2(blocks_range, pairs)

    # print('pairs_data len:', len(pairs_data), 'events:', sum([len(p) for p in pairs_data]))
    print('time:', time.time() - tik)



if __name__ == "__main__":
    import sys

    network_name = sys.argv[1] if len(sys.argv) > 1 else 'bsc'
    print('network_name', network_name)
    w3 = MyWeb3(network_name).get_http_provider_async() 
    asyncio.run(run(w3))


    


