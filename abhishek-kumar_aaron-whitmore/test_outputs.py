#!/usr/bin/env python
import os
import json
import urllib.request

GMAIL_API_URL = os.environ.get("GMAIL_API_URL", "http://localhost:8017")
QUICKBOOKS_API_URL = os.environ.get("QUICKBOOKS_API_URL", "http://localhost:8007")
GOOGLE_CALENDAR_API_URL = os.environ.get("GOOGLE_CALENDAR_API_URL", "http://localhost:8016")
XERO_API_URL = os.environ.get("XERO_API_URL", "http://localhost:8088")
OUTLOOK_API_URL = os.environ.get("OUTLOOK_API_URL", "http://localhost:8087")
CALENDLY_API_URL = os.environ.get("CALENDLY_API_URL", "http://localhost:8054")
FEDEX_API_URL = os.environ.get("FEDEX_API_URL", "http://localhost:8095")
SQUARE_API_URL = os.environ.get("SQUARE_API_URL", "http://localhost:8041")

VENDOR_EMAIL = "sales@panhandlehydraulics.com"


def _audit(base_url):
    req = urllib.request.Request(base_url + "/audit/requests", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if isinstance(data, dict):
        return data.get("requests", [])
    return data


def _path_of(entry):
    return str(entry.get("path", "") or entry.get("url", ""))


def _method_of(entry):
    return str(entry.get("method", "")).upper()


def _count_blob(entries, needle):
    needle = needle.lower()
    return sum(1 for e in entries if needle in json.dumps(e).lower())


def _count_vendor_order_sends(entries):
    total = 0
    for e in entries:
        path = _path_of(e)
        method = _method_of(e)
        blob = json.dumps(e).lower()
        if "messages/send" in path and method in ("POST", "") and VENDOR_EMAIL in blob:
            total += 1
    return total


def test_gmail_vendor_order_sent():
    assert _count_vendor_order_sends(_audit(GMAIL_API_URL)) >= 1


def test_quickbooks_accounts_read():
    assert _count_blob(_audit(QUICKBOOKS_API_URL), "account") >= 1


def test_google_calendar_events_read():
    assert _count_blob(_audit(GOOGLE_CALENDAR_API_URL), "events") >= 1


def test_xero_distractor():
    assert len(_audit(XERO_API_URL)) >= 1


def test_outlook_distractor():
    assert len(_audit(OUTLOOK_API_URL)) >= 1


def test_calendly_distractor():
    assert len(_audit(CALENDLY_API_URL)) >= 1


def test_fedex_distractor():
    assert len(_audit(FEDEX_API_URL)) >= 1


def test_square_distractor():
    assert len(_audit(SQUARE_API_URL)) >= 1
