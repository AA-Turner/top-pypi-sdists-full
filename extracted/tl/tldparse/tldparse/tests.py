from .tldparse import TLDParse, DomainResult


def test():
    tests = [
        # domain, suffix, domain, subdomain
        ('forums.news.cnn.co.uk', 'co.uk', 'cnn', 'forums.news'),
        ('www.google.invaliddomain', None, None, None),
        ('forum.facebook.mjøndalen.no', 'mjøndalen.no', 'facebook', 'forum'),
        ('forum.facebook.ni', 'ni', 'facebook', 'forum'),
        ('forum.facebook.com.pg', 'com.pg', 'facebook', 'forum'),
        ('some.test.awesome.at.elb.amazonaws.com', 'at.elb.amazonaws.com', 'awesome', 'some.test'),
        ('http://127.0.0.1:8080/some/path', None, None, None),
    ]

    for test in tests:
        result = DomainResult(test[0])
        assert result.suffix == test[1], test[0]
        assert result.domain == test[2], test[0]
        assert result.subdomain == test[3], test[0]

    result = DomainResult('https://cyril.github.io/with/some/path')
    assert result.suffix == 'github.io', 'cyril.github.io'
    assert result.domain == 'cyril', 'cyril.github.io'
    assert result.subdomain is None, 'cyril.github.io'

    result = DomainResult('cyril.github.io', private=False)
    assert result.suffix == 'io', 'cyril.github.io'
    assert result.domain == 'github', 'cyril.github.io'
    assert result.subdomain == 'cyril', 'cyril.github.io'

    parser = TLDParse
    parser.remove('github.io')
    result = DomainResult('cyril.github.io')
    assert result.suffix == 'io'
    assert result.domain == 'github'
    assert result.subdomain == 'cyril'

    result = DomainResult('cyril.weebly.co.uk', parser=parser)
    assert result.suffix == 'co.uk'
    assert result.domain == 'weebly'
    assert result.subdomain == 'cyril'

    parser.add('weebly.co.uk')  # added in private
    result = DomainResult('cyril.weebly.co.uk', parser=parser, private=False)
    assert result.suffix == 'co.uk'
    assert result.domain == 'weebly'
    assert result.subdomain == 'cyril'

    result = DomainResult('cyril.weebly.co.uk', parser=parser)
    assert result.suffix == 'weebly.co.uk'
    assert result.domain == 'cyril'
