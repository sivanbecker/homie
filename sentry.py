import logbook

import sentry_sdk

_logger = logbook.Logger(__name__)


def init_sentry():
    _logger.notice("Initializing Sentry")
    sentry_sdk.init(
        "https://b989688065ac4d99b5ea870555c36b2d@o923570.ingest.sentry.io/5890357",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )
