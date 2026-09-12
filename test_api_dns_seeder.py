from unittest.mock import patch

from api_dns_seeder import PeerResolver
from dnslib import DNSRecord


# Test to ensure the resolver keeps only unique, publicly routable peers
def test_update_peers():
    mock_response = {
        "result": [
            {"addr": "8.8.8.8"},
            {"addr": "8.8.8.8"},
            {"addr": "2001:4860:4860::8888"},
            {"addr": "192.168.1.1"},
            {"addr": "127.0.0.1"},
            {"addr": "2001:db8::1"},
            {"addr": "not-an-address"}
        ]
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        resolver = PeerResolver(
            "https://api.adventurecoin.quest/peers",
            start_thread=False
        )
        resolver.update_peers()

        assert mock_get.call_count == 2
        assert resolver.ipv4_peers == ["8.8.8.8"]
        assert resolver.ipv6_peers == ["2001:4860:4860::8888"]


# Test DNS resolution (A and AAAA queries)
def test_resolve():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 503
        resolver = PeerResolver(
            "https://api.adventurecoin.quest/peers",
            start_thread=False
        )

    resolver.ipv4_peers = ["8.8.8.8"]
    resolver.ipv6_peers = ["2001:4860:4860::8888"]

    request_ipv4 = DNSRecord.question("example.com", "A")
    request_ipv6 = DNSRecord.question("example.com", "AAAA")

    response_ipv4 = resolver.resolve(request_ipv4, None)
    response_ipv6 = resolver.resolve(request_ipv6, None)

    assert len(response_ipv4.rr) == 1
    assert str(response_ipv4.rr[0].rdata) == "8.8.8.8"

    assert len(response_ipv6.rr) == 1
    assert str(response_ipv6.rr[0].rdata) == "2001:4860:4860::8888"
