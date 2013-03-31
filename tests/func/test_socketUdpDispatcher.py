import logging
import testUtils as utils

import time
import threading

from coap import coap, \
                 coapDefines

#============================ logging ===============================

log = logging.getLogger(utils.getMyLoggerName())
log.addHandler(utils.NullHandler())

#============================ defines ===============================

IPADDRESS1 = 'aaaa::1'
IPADDRESS2 = 'aaaa::2'

NUMPACKETS = 5

#============================ fixtures ==============================

#============================ helpers ===============================

#============================ tests =================================

def test_startStop(logFixture,snoopyDispatcher):
    
    for _ in range(5):
        
        assert len(threading.enumerate())==1
        
        # start two coap endpoints
        coap1 = coap.coap(ipAddress=IPADDRESS1,testing=True)
        coap2 = coap.coap(ipAddress=IPADDRESS2,testing=True)
        
        # let them live a bit
        time.sleep(0.500)
        
        assert len(threading.enumerate())==3
        
        # close them
        coap1.close()
        coap2.close()
        
        time.sleep(0.500)
        assert len(threading.enumerate())==1
    
def test_socketUdpComunication(logFixture,snoopyDispatcher):
    
    # start two coap endpoints
    coap1 = coap.coap(ipAddress=IPADDRESS1,testing=True)
    coap2 = coap.coap(ipAddress=IPADDRESS2,testing=True)
    
    # send coap1->coap2
    for _ in range(NUMPACKETS):
        coap1.socketUdp.sendUdp(
            destIp   = 'aaaa::3',
            destPort = coapDefines.DEFAULT_UDP_PORT,
            msg      = [0x51,0x01,0x7d,0x35,0x20,0xbb]+[ord(c) for c in 'temperature']
        )
        time.sleep(0.500)
        coap2.socketUdp.sendUdp(
            destIp   = IPADDRESS1,
            destPort = coapDefines.DEFAULT_UDP_PORT,
            msg      = [0x41,0x01,0x7d,0x35,0x20,0xbb]+[ord(c) for c in 'temperature']
        )
        time.sleep(0.500)
    
    # verify stats
    assert coap1.socketUdp.getStats()=={
        'numTx': NUMPACKETS,
        'numRx': NUMPACKETS,
    }
    assert coap2.socketUdp.getStats()=={
        'numTx': NUMPACKETS,
        'numRx': NUMPACKETS,
    }
    
    # close them
    coap1.close()
    coap2.close()
    
    time.sleep(0.500)
    assert len(threading.enumerate())==1