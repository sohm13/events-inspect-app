from events_inpsect.blockchain_scan import Pair, BlockChainScan
from events_inpsect.web3_provider import MyWeb3
import time



if __name__ == "__main__":

    web3 = MyWeb3('aurora').get_http_provider()


    PAIRS = (
        ('0x20F8AeFB5697B77E0BB835A8518BE70775cdA1b0', 'NEAR_USDC'),
        ('0x63da4DB6Ef4e7C62168aB03982399F9588fCd198', 'WETH_NEAR'),

    )

    pairs = [Pair(address=p[0], symbol=p[1]) for p in PAIRS] 

    bsc_scan = BlockChainScan(web3)
    #
    tik = time.time()
    blocks_range = [ [70581516, 70581516+10] for _ in range(len(PAIRS))]
    # # pairs_data = bsc_scan.get_scan_event_from_blocks(blocks_range, pairs)
    pairs_data = bsc_scan.get_scan_event_from_blocks_async(blocks_range, pairs)
    print('time', time.time() - tik)
    print('pairs:', len(pairs_data))
    print('events:', sum([len(pair) for pair in pairs_data]))

    # # can make dict with key and data
    pairs_dict = { PAIRS[i][1]:pairs_data[i] for i in range(len(pairs_data)) }
    print(pairs_dict)

    # # blocks data
    # tik = time.time()
    blocks = bsc_scan.get_blocks(*blocks_range[0])
    for b in blocks:
        print(b.number, b.timestamp, b.size, )
    print(f'time for get blocks {len(blocks)}', time.time() - tik)
    print(blocks[0])


