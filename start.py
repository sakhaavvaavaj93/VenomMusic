"""Render Web Service entrypoint for VenomMusic.

Render Free supports Web Services, not Background Workers. This entrypoint
runs a tiny HTTP server in a daemon thread while the original VenomMusic
Telegram/PyTgCalls event loop remains the main process.
"""

import threading

from render_web import run_web_server


def main():
    web_thread = threading.Thread(
        target=run_web_server,
        name="render-http",
        daemon=True,
    )
    web_thread.start()

    # Keep the original VenomMusic startup path unchanged. This is important
    # because Pyrogram/PyTgCalls need to own the main asyncio event loop.
    from VenomX.__main__ import init
    from VenomX import LOGGER, app

    try:
        app.run(init())
    except KeyboardInterrupt:
        LOGGER("Render").info("Shutdown requested")
    except Exception:
        LOGGER("Render").exception("VenomMusic crashed")
        raise


if __name__ == "__main__":
    main()
