from main import RoutingEngine, RoutingRule, Notification, Action, Item


def test_add_route():
    router = RoutingEngine()
    route = RoutingRule()
    router.add_rule(route)
    assert len(router.rules) == 1
    assert router.rules.pop() == route


def test_route_no_rule():
    router = RoutingEngine()
    notification = Notification()
    result = router.route(notification)
    assert result == notification


def test_route_drop_rule():
    router = RoutingEngine()
    router.add_rule(RoutingRule(source=Item(1), action=Action.DROP))

    notification = Notification(source=Item(1))
    result = router.route(notification)
    assert result is None


def test_route_allow_rule():
    router = RoutingEngine()

    source = Item(1)
    router.add_rule(RoutingRule(source=source, action=Action.ALLOW))

    notification = Notification(source=source)
    result = router.route(notification)
    assert result is notification


def test_route_priority():
    router = RoutingEngine()

    source = Item(1)
    target = Item(2)
    router.add_rule(RoutingRule(source=source, target=target, action=Action.ALLOW, priority=1))
    router.add_rule(RoutingRule(source=source, target=target, action=Action.DROP, priority=0))

    result = router.route(Notification(source=source, target=target))
    assert result is None


def test_route_enabled():
    router = RoutingEngine()

    source = Item(1)
    target = Item(2)
    router.add_rule(RoutingRule(source=source, target=target, action=Action.ALLOW, priority=1))
    router.add_rule(RoutingRule(source=source, target=target, action=Action.DROP, priority=0, enabled=False))

    notification = Notification(source=source, target=target)
    result = router.route(notification)
    assert result is notification
