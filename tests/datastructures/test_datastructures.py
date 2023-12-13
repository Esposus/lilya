from lilya.datastructures import URL, MultiDict, Secret


def test_url_structure():
    url = URL("https://example.org:123/path/to/somewhere?abc=123#anchor")
    assert url.scheme == "https"
    assert url.hostname == "example.org"
    assert url.port == 123
    assert url.netloc == "example.org:123"
    assert url.username is None
    assert url.password is None
    assert url.path == "/path/to/somewhere"
    assert url.query == "abc=123"
    assert url.fragment == "anchor"

    new = url.replace(scheme="http")
    assert new == "http://example.org:123/path/to/somewhere?abc=123#anchor"
    assert new.scheme == "http"

    new = url.replace(port=None)
    assert new == "https://example.org/path/to/somewhere?abc=123#anchor"
    assert new.port is None

    new = url.replace(hostname="example.com")
    assert new == "https://example.com:123/path/to/somewhere?abc=123#anchor"
    assert new.hostname == "example.com"

    ipv6_url = URL("https://[fe::2]:12345")
    new = ipv6_url.replace(port=8080)
    assert new == "https://[fe::2]:8080"

    new = ipv6_url.replace(username="username", password="password")
    assert new == "https://username:password@[fe::2]:12345"
    assert new.netloc == "username:password@[fe::2]:12345"

    ipv6_url = URL("https://[fe::2]")
    new = ipv6_url.replace(port=123)
    assert new == "https://[fe::2]:123"

    url = URL("http://u:p@host/")
    assert url.replace(hostname="bar") == URL("http://u:p@bar/")

    url = URL("http://u:p@host:80")
    assert url.replace(port=88) == URL("http://u:p@host:88")


def test_url_query_params():
    url = URL("https://example.org/path/?page=3")
    assert url.query == "page=3"

    url = url.include_query_params(page=4)
    assert str(url) == "https://example.org/path/?page=4"

    url = url.include_query_params(search="testing")
    assert str(url) == "https://example.org/path/?page=4&search=testing"

    url = url.replace_query_params(order="name")
    assert str(url) == "https://example.org/path/?order=name"

    url = url.remove_query_params("order")
    assert str(url) == "https://example.org/path/"


def test_hidden_password():
    url = URL("https://example.org/path/to/somewhere")
    assert repr(url) == "URL('https://example.org/path/to/somewhere')"

    url = URL("https://username@example.org/path/to/somewhere")
    assert repr(url) == "URL('https://username@example.org/path/to/somewhere')"

    url = URL("https://username:password@example.org/path/to/somewhere")
    assert repr(url) == "URL('https://username:***********@example.org/path/to/somewhere')"


def test_secret():
    value = Secret("a-value-being-passed")

    assert repr(value) == "Secret('***********')"
    assert str(value) == "a-value-being-passed"


def test_multidict():
    query = MultiDict([("a", "123"), ("a", "456"), ("b", "789")])
    assert "a" in query
    assert "A" not in query
    assert "c" not in query
    assert query["a"] == "456"
    assert query.get("a") == "456"
    assert query.get("nope", default=None) is None
    assert query.getlist("a") == ["123", "456"]
    assert list(query.keys()) == ["a", "b"]
    assert list(query.values()) == ["456", "789"]
    assert list(query.items()) == [("a", "456"), ("b", "789")]
    assert len(query) == 2
    assert list(query) == ["a", "b"]
    assert dict(query) == {"a": "456", "b": "789"}
    assert str(query) == "MultiDict([('a', '123'), ('a', '456'), ('b', '789')])"
    assert repr(query) == "MultiDict([('a', '123'), ('a', '456'), ('b', '789')])"
    assert MultiDict({"a": "123", "b": "456"}) == MultiDict([("a", "123"), ("b", "456")])
    assert MultiDict({"a": "123", "b": "456"}) == MultiDict({"b": "456", "a": "123"})
    assert MultiDict() == MultiDict({})
    assert MultiDict({"a": "123", "b": "456"}) != "invalid"

    query = MultiDict([("a", "123"), ("a", "456")])
    assert MultiDict(query) == query

    query = MultiDict([("a", "123"), ("a", "456")])
    query["a"] = "789"
    assert query["a"] == "789"
    assert query.get("a") == "789"
    assert query.getlist("a") == ["789"]

    query = MultiDict([("a", "123"), ("a", "456")])
    del query["a"]
    assert query.get("a") is None
    assert repr(query) == "MultiDict([])"

    query = MultiDict([("a", "123"), ("a", "456"), ("b", "789")])
    assert query.pop("a") == "456"
    assert query.get("a", None) is None
    assert repr(query) == "MultiDict([('b', '789')])"

    query = MultiDict([("a", "123"), ("a", "456"), ("b", "789")])
    item = query.popitem()
    assert query.get(item[0]) is None

    query = MultiDict([("a", "123"), ("a", "456"), ("b", "789")])
    assert query.poplist("a") == ["123", "456"]
    assert query.get("a") is None
    assert repr(query) == "MultiDict([('b', '789')])"

    query = MultiDict([("a", "123"), ("a", "456"), ("b", "789")])
    query.clear()
    assert query.get("a") is None
    assert repr(query) == "MultiDict([])"

    query = MultiDict([("a", "123")])
    query.setlist("a", ["456", "789"])
    assert query.getlist("a") == ["456", "789"]
    query.setlist("b", [])
    assert "b" not in query

    query = MultiDict([("a", "123")])
    assert query.setdefault("a", "456") == "123"
    assert query.getlist("a") == ["123"]
    assert query.setdefault("b", "456") == "456"
    assert query.getlist("b") == ["456"]
    assert repr(query) == "MultiDict([('a', '123'), ('b', '456')])"

    query = MultiDict([("a", "123")])
    query.append("a", "456")
    assert query.getlist("a") == ["123", "456"]
    assert repr(query) == "MultiDict([('a', '123'), ('a', '456')])"

    query = MultiDict([("a", "123"), ("b", "456")])
    query.update({"a": "789"})
    assert query.getlist("a") == ["789"]
    assert query == MultiDict([("a", "789"), ("b", "456")])

    query = MultiDict([("a", "123"), ("b", "456")])
    query.update(query)
    assert repr(query) == "MultiDict([('a', '123'), ('b', '456')])"

    query = MultiDict([("a", "123"), ("a", "456")])
    query.update([("a", "123")])
    assert query.getlist("a") == ["123"]
    query.update([("a", "456")], a="789", b="123")
    assert query == MultiDict([("a", "456"), ("a", "789"), ("b", "123")])
