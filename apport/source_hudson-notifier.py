# Apport integration for Hudson notifier
#
# Copyright 2009 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Stub for Apport"""
# pylint: disable-msg=F0401,C0103
# shut up about apport. We know. We aren't going to backport it for pqm
import apport

def add_info(report):
    """add report info"""

    if not apport.packaging.is_distro_package(report['Package'].split()[0]):
        report['ThirdParty'] = 'True'
        report['CrashDB'] = 'hudsonnotifier'
