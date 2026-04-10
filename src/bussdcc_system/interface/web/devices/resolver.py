from bussdcc import ContextProtocol
from bussdcc_framework.interface.web.formtree.types import FieldOption
from bussdcc_framework.metadata import FieldRef


class RuntimeRefResolver:
    def __init__(self, ctx: ContextProtocol) -> None:
        self.ctx = ctx

    def resolve(
        self,
        ref: FieldRef,
        field_type: object,
    ) -> list[FieldOption] | None:
        if ref.kind == "bus":
            return [
                FieldOption(value=device.id, label=device.id)
                for device in self.ctx.runtime.devices.list()
                if getattr(device, "kind", None) == "bus"
            ]

        return None
