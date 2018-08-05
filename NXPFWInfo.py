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
    sys.exit(1)

if len(sys.argv) - 1 != 1 or "--help" in sys.argv or "-h" in sys.argv:
    printHelp()

with open(sys.argv[1], "rb") as file:
    # FIXME: Read the file only once
    file_len = len(file.read())

    # Check if APP/BLD or ISP
    if file_len <= NXPCommon.APP_LEN:
        # Both APP and BLD have the ids at the same address
        file.seek(NXPCommon.FWINFO_OFFSET)
        ids = file.read(0x6)

        # FIXME: Try to narrow it down further
        data_str = file.read()

        if file_len <= NXPCommon.BLD_LEN:
            prefix = "BLD"
        else:
            prefix = "APP"

        print(prefix + " image detected\n")

        NXPCommon.printFWInfo(ids, data_str, prefix)

    elif file_len <= NXPCommon.ISP_LEN:
        print("ISP image detected\n")

        # First is BLD
        file.seek(0x00)
        data_str = file.read(NXPCommon.BLD_LEN)
        file.seek(NXPCommon.FWINFO_OFFSET)

        ids = file.read(0x6)
        NXPCommon.printFWInfo(ids, data_str, "BLD")
        print()

        # Followed by APP1
        file.seek(NXPCommon.BLD_LEN)
        data_str = file.read(NXPCommon.APP_LEN)
        file.seek(NXPCommon.BLD_LEN + NXPCommon.FWINFO_OFFSET)

        ids = file.read(0x6)
        NXPCommon.printFWInfo(ids, data_str, "APP1")
        print()

        # Followed by APP2
        file.seek(NXPCommon.BLD_LEN + NXPCommon.APP_LEN)
        data_str = file.read(NXPCommon.APP_LEN)
        file.seek(NXPCommon.BLD_LEN + NXPCommon.APP_LEN + NXPCommon.FWINFO_OFFSET)

        ids = file.read(0x6)
        NXPCommon.printFWInfo(ids, data_str, "APP2")

    else:
        print("Invalid image specified")
        sys.exit(3)

