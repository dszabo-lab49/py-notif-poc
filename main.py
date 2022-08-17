from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum

from typing import List


@dataclass()
class Item:
    item_pk: int
    source_type: str = ""


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass()
class Notification:
    source: Item = None
    target: Item = None
    job: int = 0
    data: str = ""
    severity: Severity = Severity.INFO
    meta: str = ""


class NotificationService:
    def __init__(self):
        self.router = RoutingEngine()
        self.filter = FilterEngine()
        self.deliverables = []

    def post(self, notification: Notification):
        res = self.filter.filter(self.router.route(notification))
        if res is not None:
            self.deliverables.append(res)


class Action(Enum):
    DROP = "drop"
    ALLOW = "allow"


class DeliveryMode(Enum):
    NOTIFICATION = "notification"
    EMAIL = "email"


@dataclass()
class RoutingRule:
    name: str = ""
    action: Action = Action.DROP
    enabled: bool = True
    priority: int = 0
    source: Item = None
    source_type: str = ""
    target: Item = None
    notes: str = ""
    delivery_mode: DeliveryMode = DeliveryMode.NOTIFICATION
    persist: bool = False
    updated_at: date = datetime.today()
    updated_by: str = ""


class RoutingEngine:
    def __init__(self):
        self.rules: List[RoutingRule] = []

    def add_rule(self, rule: RoutingRule):
        self.rules.append(rule)

    def get_enabled_rules_by_source_or_target(self, source: Item, target: Item):
        self.rules.sort(key=lambda r: r.priority)
        for rule in self.rules:
            if rule.enabled:
                if rule.source is None and rule.target is None:
                    yield rule
                    continue

                source_match = rule.source is None or rule.source.item_pk == source.item_pk
                target_match = rule.target is None or rule.target.item_pk == target.item_pk
                if source_match and target_match:
                    yield rule
                    continue

    def route(self, notification: Notification):
        rules = self.get_enabled_rules_by_source_or_target(notification.source, notification.target)
        for rule in rules:
            if rule.action is Action.DROP:
                return None
        return notification


@dataclass()
class User:
    user_pk: int = 0


@dataclass()
class Filter:
    name: str = ""
    user: User = None
    source: Item = None
    source_type: str = ""
    enabled: bool = True
    severity: Severity = Severity.INFO
    tags: str = ""


def is_mismatch(rules: filter, notification: Notification):
    for rule in rules:
        source_mismatch = rule.source is not None and rule.source.item_pk != notification.source.item_pk
        source_type_mismatch = rule.source_type is not None and rule.source_type != notification.source.source_type
        severity_mismatch = rule.severity is not None and rule.severity != notification.severity
        if source_mismatch or source_type_mismatch or severity_mismatch:
            return True
    return False


class FilterEngine:
    def __init__(self):
        self.filter_rules: List[Filter] = []

    def add_filter(self, rule: Filter):
        self.filter_rules.append(rule)

    def filter(self, notification: Notification):
        enabled_rules = filter(lambda r: r.enabled, self.filter_rules)
        if is_mismatch(enabled_rules, notification):
            return notification
        return None
