#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from saib.skeleton import parse_update, parse_update_entry

__author__ = "Ryan Long"
__copyright__ = "Ryan Long"
__license__ = "mit"


@pytest.fixture
def data():
    return [
        'Ryans-iPad.echoes.net (192.168.0.117) at 02:0f:b5:69:90:a8 [ether]  on br0\n',
        '? (192.168.0.101) at 02:0f:b5:6b:09:3d [ether]  on br0\n',
        'Blitzcrank.echoes.net (192.168.0.118) at b8:d7:af:8e:93:78 [ether]  on br0\n',
        '? (192.168.0.103) at 0c:62:a6:df:4e:3a [ether]  on br0\n',
        'SAMSUNG-SM-T377V.echoes.net (192.168.0.104) at 02:0f:b5:5f:f3:6b [ether]  on br0\n',
        '? (192.168.0.2) at 4e:24:24:d6:bd:10 [ether]  on br0\n',
        '? (192.168.0.123) at ac:3a:7a:7c:f2:a5 [ether]  on br0\n',
        'SAMSUNG-SM-G930A.echoes.net (192.168.0.107) at 02:0f:b5:5f:d3:18 [ether]  on br0\n',
        'raspberrypi.echoes.net (192.168.0.108) at 00:13:ef:40:3c:2e [ether]  on br0\n',
        'SAMSUNG-SM-G955U.echoes.net (192.168.0.109) at dc:ef:ca:cd:eb:31 [ether]  on br0\n',
        'amazon-337c9f22b.echoes.net (192.168.0.126) at 02:0f:b5:65:a5:7a [ether]  on br0\n',
        'Viktor.echoes.net (192.168.0.127) at f4:b7:e2:01:2c:64 [ether]  on br0\n',
        'amazon-0738eece4.echoes.net (192.168.0.148) at cc:f7:35:e7:e4:8f [ether]  on br0\n',
        'Galaxy-Tab-A.echoes.net (192.168.0.114) at 44:78:3e:2a:95:50 [ether]  on br0\n',
        'Ekko.echoes.net (192.168.0.115) at d4:25:8b:fa:02:80 [ether]  on br0\n',
        '? (72.28.56.1) at 00:cc:fc:61:e0:19 [ether]  on eth0\n',
        '? (192.168.0.150) at da:d3:a3:8a:ab:74 [ether]  on br0\n',
        'JHIN.echoes.net (192.168.0.133) at 30:9c:23:81:d1:ca [ether]  on br0\n']


def test_parse_update_WhenCalled_ReturnsListOfDictsUpdatedDevice(data):
    result = parse_update(data)
    assert result == [{'name': 'Ryans-iPad.echoes.net', 'ip': '192.168.0.117',
                       'mac_address': '02:0f:b5:69:90:a8'},
                      {'name': '?', 'ip': '192.168.0.101',
                       'mac_address': '02:0f:b5:6b:09:3d'},
                      {'name': 'Blitzcrank.echoes.net', 'ip': '192.168.0.118',
                       'mac_address': 'b8:d7:af:8e:93:78'},
                      {'name': '?', 'ip': '192.168.0.103',
                       'mac_address': '0c:62:a6:df:4e:3a'},
                      {'name': 'SAMSUNG-SM-T377V.echoes.net',
                       'ip': '192.168.0.104',
                       'mac_address': '02:0f:b5:5f:f3:6b'},
                      {'name': '?', 'ip': '192.168.0.2',
                       'mac_address': '4e:24:24:d6:bd:10'},
                      {'name': '?', 'ip': '192.168.0.123',
                       'mac_address': 'ac:3a:7a:7c:f2:a5'},
                      {'name': 'SAMSUNG-SM-G930A.echoes.net',
                       'ip': '192.168.0.107',
                       'mac_address': '02:0f:b5:5f:d3:18'},
                      {'name': 'raspberrypi.echoes.net', 'ip': '192.168.0.108',
                       'mac_address': '00:13:ef:40:3c:2e'},
                      {'name': 'SAMSUNG-SM-G955U.echoes.net',
                       'ip': '192.168.0.109',
                       'mac_address': 'dc:ef:ca:cd:eb:31'},
                      {'name': 'amazon-337c9f22b.echoes.net',
                       'ip': '192.168.0.126',
                       'mac_address': '02:0f:b5:65:a5:7a'},
                      {'name': 'Viktor.echoes.net', 'ip': '192.168.0.127',
                       'mac_address': 'f4:b7:e2:01:2c:64'},
                      {'name': 'amazon-0738eece4.echoes.net',
                       'ip': '192.168.0.148',
                       'mac_address': 'cc:f7:35:e7:e4:8f'},
                      {'name': 'Galaxy-Tab-A.echoes.net',
                       'ip': '192.168.0.114',
                       'mac_address': '44:78:3e:2a:95:50'},
                      {'name': 'Ekko.echoes.net', 'ip': '192.168.0.115',
                       'mac_address': 'd4:25:8b:fa:02:80'},
                      {'name': '?', 'ip': '72.28.56.1',
                       'mac_address': '00:cc:fc:61:e0:19'},
                      {'name': '?', 'ip': '192.168.0.150',
                       'mac_address': 'da:d3:a3:8a:ab:74'},
                      {'name': 'JHIN.echoes.net', 'ip': '192.168.0.133',
                       'mac_address': '30:9c:23:81:d1:ca'}]


def test_parse_update_entry_WhenCalledWithValidEntry_ReturnsValidTypeAndData():
    entry = "Ekko.echoes.net (192.168.0.115) at d4:25:8b:fa:02:80 [ether]  on br0"
    result = parse_update_entry(entry)
    assert result["name"] == "Ekko.echoes.net"
    assert result["ip"] == "192.168.0.115"
    assert result["mac_address"] == "d4:25:8b:fa:02:80"
