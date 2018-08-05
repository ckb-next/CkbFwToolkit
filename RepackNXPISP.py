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
import os

OUTFILE = "PackedISP.bin"

def printHelp():
    print("Usage: " + sys.argv[0] + " BLD.bin APP.bin")
    sys.exit(1)

# FIXME: Add the ability to pack an optional second app
if len(sys.argv) - 1 != 2 or "--help" in sys.argv or "-h" in sys.argv:
    printHelp()

if os.path.isfile(OUTFILE):
    print(OUTFILE + " already exists.")
    sys.exit(2)

with open(sys.argv[1], "rb") as bld_f, open(sys.argv[2], "rb") as app_f:
    app = app_f.read()
    new_app_len = len(app)

    bld = bld_f.read()
    new_bld_len = len(bld)

    # Sanity check
    if new_bld_len > NXPCommon.BLD_LEN:
        print("Bld binary is too long. Perhaps you specified the files in the wrong order.")
        sys.exit(3)

    if new_app_len > NXPCommon.APP_LEN:
        print("App binary is too long. Perhaps you specified the files in the wrong order.")
        sys.exit(3)

    print("Repacking ISP image with the following contents:")
    NXPCommon.printFWInfo(bld[NXPCommon.FWINFO_OFFSET:NXPCommon.FWINFO_OFFSET + 0x6], bld, "BLD")
    print()
    NXPCommon.printFWInfo(app[NXPCommon.FWINFO_OFFSET:NXPCommon.FWINFO_OFFSET + 0x6], app, "APP")
    print()

    with open(OUTFILE, "ab") as isp:
        isp.write(bld)
        # Pad the rest with 0xFF
        if new_bld_len < NXPCommon.BLD_LEN:
            isp.write(bytes([0xFF] * (NXPCommon.BLD_LEN - new_bld_len))) # Thank you Lofty <3

        # Write app binary
        isp.write(app)
        if new_app_len < NXPCommon.APP_LEN:
            isp.write(bytes([0xFF] * (NXPCommon.APP_LEN - new_app_len)))

        # Duplicate app binary
        isp.write(app)
        if new_app_len < NXPCommon.APP_LEN:
            isp.write(bytes([0xFF] * (NXPCommon.APP_LEN - new_app_len)))

        # File is padded with 0xFF all the way up to ISP_LEN
        isp.write(bytes([0xFF] * (NXPCommon.ISP_LEN - (NXPCommon.BLD_LEN + 2 * NXPCommon.APP_LEN))))

print("Done!")
