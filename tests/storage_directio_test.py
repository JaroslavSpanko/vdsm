#
# Copyright 2012-2016 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

from testlib import VdsmTestCase as TestCaseBase
from testlib import permutations, expandPermutations
from testlib import temporaryPath

from vdsm.storage import directio


@expandPermutations
class DirectFileTests(TestCaseBase):

    DATA = "a" * 512 + "b" * 512

    @permutations([[0], [512], [1024], [1024 + 512]])
    def testRead(self, size):
        with temporaryPath(data=self.DATA) as srcPath, \
                directio.DirectFile(srcPath, "r") as f:
            self.assertEquals(f.read(size), self.DATA[:size])

    @permutations([[512], [1024]])
    def testSeekRead(self, offset):
        with temporaryPath(data=self.DATA) as srcPath, \
                directio.DirectFile(srcPath, "r") as f:
            f.seek(offset)
            self.assertEquals(f.read(), self.DATA[offset:])

    def testWrite(self):
        with temporaryPath() as srcPath, \
                directio.DirectFile(srcPath, "w") as f:
            f.write(self.DATA)
            with open(srcPath) as f:
                self.assertEquals(f.read(), self.DATA)

    def testSmallWrites(self):
        with temporaryPath() as srcPath, \
                directio.DirectFile(srcPath, "w") as f:
            f.write(self.DATA[:512])
            f.write(self.DATA[512:])

            with open(srcPath) as f:
                self.assertEquals(f.read(), self.DATA)

    def testUpdateRead(self):
        with temporaryPath() as srcPath, \
                directio.DirectFile(srcPath, "w") as f:
            f.write(self.DATA[:512])

            with directio.DirectFile(srcPath, "r+") as f:
                f.seek(512)
                f.write(self.DATA[512:])

            with open(srcPath) as f:
                self.assertEquals(f.read(), self.DATA)