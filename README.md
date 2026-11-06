# AQUA WORLD Facebook Reposter

Deploy as a separate Railway service connected to a GitHub repository.

Required Railway variables:
- `TELEGRAM_BOT_TOKEN` — token from BotFather (keep private)
- `FACEBOOK_PAGE_ID` — numeric ID of AQUA WORLD Facebook Page
- `FACEBOOK_PAGE_TOKEN` — Page access token with publishing permissions

Optional:
- `TELEGRAM_CHANNEL_USERNAME` — default `@AquaWorld_Official`
- `FACEBOOK_GRAPH_VERSION` — default `v24.0`; adjust to supported API version if needed

Bot must be an admin in Telegram channel. Publish a new text or single-photo post to test. Only new posts are processed. Photo albums, videos and edits are not yet supported. No durable deduplication: Telegram retries or a service crash may produce duplicates. Avoid running multiple copies with the same bot token.
