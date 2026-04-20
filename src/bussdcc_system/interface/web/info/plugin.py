from typing import Any, Iterable
from datetime import timedelta

from flask import Blueprint, render_template, redirect, url_for, request
from flask_socketio import SocketIO

import humanize

from bussdcc import Message, Event, ContextProtocol
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin
from bussdcc_system import message


class SystemInfoPlugin(BaseWebPlugin):
    name = "system-info"

    def _format_uptime(self, ctx: ContextProtocol) -> str:
        uptime_seconds = ctx.state.get("system.uptime")
        uptime = humanize.precisedelta(timedelta(seconds=int(uptime_seconds)))
        return uptime

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_info",
            __name__,
            url_prefix="/system/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            return render_template(
                "bussdcc_system/info/index.html", uptime=self._format_uptime(ctx)
            )

        app.register_blueprint(bp)

    def event_types(self) -> Iterable[type[Message]]:
        return (message.UptimeUpdate,)

    def handle_event(
        self,
        app: FlaskApp,
        socketio: SocketIO,
        ctx: ContextProtocol,
        evt: Event[Message],
    ) -> None:
        socketio.emit(
            "ui.system.uptime.updated",
            self._format_uptime(ctx),
        )


plugin: WebPlugin = SystemInfoPlugin()
