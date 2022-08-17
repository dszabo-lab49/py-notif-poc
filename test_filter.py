from main import FilterEngine, Filter, Item, Notification, Severity


def test_add_filter():
    filter_eng = FilterEngine()
    rule = Filter()
    filter_eng.add_filter(rule)
    assert len(filter_eng.filter_rules) == 1


def test_filter_pass_through():
    filter_eng = FilterEngine()

    rule = Filter(source=Item(1))
    filter_eng.add_filter(rule)

    notification = Notification(source=Item(2))
    result = filter_eng.filter(notification)
    assert result is notification


def test_filter_by_source():
    filter_eng = FilterEngine()
    filter_eng.add_filter(Filter(source=Item(1)))

    result = filter_eng.filter(Notification(source=Item(1)))
    assert result is None


def test_filter_by_source_type():
    filter_eng = FilterEngine()
    filter_eng.add_filter(Filter(source_type="space"))

    result = filter_eng.filter(Notification(source=Item(1, source_type="space")))
    assert result is None


def test_filter_by_severity():
    filter_eng = FilterEngine()
    filter_eng.add_filter(Filter(severity=Severity.WARNING))

    result = filter_eng.filter(Notification(source=Item(1), severity=Severity.WARNING))
    assert result is None
