#
# Copyright 2012 Red Hat, Inc.
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

import re
from utils import CommandPath, execCmd

_qemuimg = CommandPath("qemu-img",
                       "/usr/bin/qemu-img",  # Fedora, RHEL
                       )


class FORMAT:
    QCOW2 = "qcow2"
    QCOW = "qcow"
    QED = "qed"
    RAW = "raw"
    VMDK = "vmdk"

__iregex = {
    'format': re.compile("^file format: (?P<value>\w+)$"),
    'virtualsize': re.compile("^virtual size: "
                              "[\d.]+[KMGT] \((?P<value>\d+) bytes\)$"),
    'clustersize': re.compile("^cluster_size: (?P<value>\d+)$"),
    'backingfile': re.compile("^backing file: (?P<value>.+) \(actual path"),
}


def __iregexSearch(pattern, text):
    return __iregex[pattern].search(text).group("value")


class QImgError(Exception):
    def __init__(self, ecode, stdout, stderr, message=None):
        self.ecode = ecode
        self.stdout = stdout
        self.stderr = stderr
        self.message = message

    def __str__(self):
        return "ecode=%s, stdout=%s, stderr=%s, message=%s" % (
            self.ecode, self.stdout, self.stderr, self.message)


def info(image, format=None):
    cmd = [_qemuimg.cmd, "info"]

    if format:
        cmd.extend(("-f", format))

    cmd.append(image)
    rc, out, err = execCmd(cmd)

    if rc != 0:
        raise QImgError(rc, out, err)

    try:
        info = {
            'format': __iregexSearch("format", out[1]),
            'virtualsize': int(__iregexSearch("virtualsize", out[2])),
        }

        if len(out) > 4:
            info['clustersize'] = int(__iregexSearch("clustersize", out[4]))

        if len(out) > 5:
            info['backingfile'] = __iregexSearch("backingfile", out[5])
    except:
        raise QImgError(rc, out, err, "unable to parse qemu-img output")

    return info


def check(image, format=None):
    cmd = [_qemuimg.cmd, "check"]

    if format:
        cmd.extend(("-f", format))

    cmd.append(image)
    rc, out, err = execCmd(cmd)

    if rc != 0:
        raise QImgError(rc, out, err)
