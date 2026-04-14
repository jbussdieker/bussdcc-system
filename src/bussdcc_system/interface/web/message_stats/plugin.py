from typing import Any, Iterable

from flask import Blueprint, render_template
from flask_socketio import SocketIO

from bussdcc import ContextProtocol, Event, Message
from bussdcc_framework.web import BaseWebPlugin, FlaskApp, WebPlugin
from bussdcc import message as bussdcc_message
from bussdcc_framework import message as framework_message


class SystemMessageStatsPlugin(BaseWebPlugin):
    name = "system-message-stats"

    def init_app(self, app: FlaskApp, ctx: ContextProtocol) -> None:
        bp = Blueprint(
            "bussdcc_system_message_stats",
            __name__,
            url_prefix="/system/runtime/info",
            template_folder="templates",
        )

        @bp.route("/")
        def index() -> Any:
            message_stats = ctx.state.get("runtime_info", {})

            return render_template(
                "bussdcc_system/message_stats/index.html",
                message_stats=message_stats,
            )

        app.register_blueprint(bp)

    def event_types(self) -> Iterable[type[Message]]:
        return (
            bussdcc_message.RuntimeBooted,
            framework_message.FrameworkBooted,
            Message,
        )

    def handle_event(
        self,
        app: FlaskApp,
        socketio: SocketIO,
        ctx: ContextProtocol,
        evt: Event[Message],
    ) -> None:
        socketio.emit(
            "ui.system.message_stats.updated",
            ctx.state.get("runtime_info", {}),
        )


plugin: WebPlugin = SystemMessageStatsPlugin()
