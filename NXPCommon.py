#!/usr/bin/env python3
#   Copyright 2018 ckb-next Development Team <ckb-next@googlegroups.com>
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#   
#   1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#   3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission. 
#   
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.

import re

BLD_LEN = 0x6000
APP_LEN = 0xC000
ISP_LEN = 0x20000
FWINFO_OFFSET = 0x102

def printFWInfo(ids, data_str, prefix):
    print(prefix + " Vendor ID: 0x" + format(ids[1], "02x") + format(ids[0], "02x"))
    print(prefix + " Product ID: 0x" + format(ids[3], "02x") + format(ids[2], "02x"))
    print(prefix + " Version: 0x" + format(ids[5], "02x") + format(ids[4], "02x"))

    # Try to find the protocol version
    r = re.compile(b"P\x00[0x]\x00[0-9x]\x00")
    res = r.findall(data_str)
    
    if len(res) > 0:
        if len(res) > 1:
            print("Possible " + prefix + " Protocol Versions:")
            for i in res:
                print(i.decode("utf-16"))
        else:
            print(prefix + " Protocol Version: " + res[0].decode("utf-16"))
    else:
        print("Could not detect " + prefix + " Protocol Version")
