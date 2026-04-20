import socket
from pathlib import Path

from bussdcc import Service, ContextProtocol

from .. import message


class SystemIdentityService(Service):
    name = "system_identity"
    interval = 1.0

    def start(self, ctx: ContextProtocol) -> None:
        hostname = socket.gethostname()
        model = self._read("/proc/device-tree/model")
        serial = self._cpuinfo_field("Serial")

        ctx.emit(
            message.SystemIdentityEvent(hostname=hostname, model=model, serial=serial)
        )

    def _emit_uptime(self, ctx: ContextProtocol) -> None:
        ctx.emit(
            message.UptimeUpdate(
                uptime=ctx.clock.uptime(),
            )
        )

    def tick(self, ctx: ContextProtocol) -> None:
        self._emit_uptime(ctx)

    def _read(self, path: str) -> str | None:
        try:
            return Path(path).read_text().strip("\x00\n")
        except Exception:
            return None

    def _cpuinfo_field(self, key: str) -> str | None:
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith(key):
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return None
