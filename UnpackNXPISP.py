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

import NXPCommon
import sys

def printHelp():
    print("Usage: " + sys.argv[0] + " Image.bin")
    sys.exit(-1)

if len(sys.argv) - 1 != 1 or "--help" in sys.argv or "-h" in sys.argv:
    printHelp()

with open(sys.argv[1], "rb") as file:
    # First 0x6000 bytes are BLD
    bld = file.read(NXPCommon.BLD_LEN)
    with open("ExtractedBLD.bin", "wb") as out:
        out.write(bld)

    # Seek to 0x6000, first App binary starts from there
    #file.seek(NXPCommon.BLD_LEN)
    # Max app length appears to be 0xC000
    app1 = file.read(NXPCommon.APP_LEN)
    with open("ExtractedAPP1.bin", "wb") as out:
        out.write(app1)

    # Seek to the second App binary
    #file.seek(0x12000) # NXPCommon.BLD_LEN + NXPCommon.APP_LEN
    # Read the rest of the App2
    app2 = file.read(NXPCommon.APP_LEN)
    with open("ExtractedAPP2.bin", "wb") as out:
        out.write(app2)

    print("Done!")

    if app1 == app2:
        print("Extracted APP images are identical.")
    else:
        print("Extracted APP images differ.")

    # File is padded with 0xFF all the way up to 0x20000
