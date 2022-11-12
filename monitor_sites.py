MONITOR_SITES = [
    {
        "url": "https://example.com",
        "expect_body_includes": "Example Domain",
        "expect_status_code": 200
    },
    {
        "url": "https://www.google.com/blah",
        "expect_body_includes": "That’s an error.",
        "expect_status_code": 404
    }
]