import esphome.codegen as cg
from esphome.components import mcp23x17_base, mcp23xxx_base, spi
import esphome.config_validation as cv
from esphome.const import CONF_ID

AUTO_LOAD = ["mcp23x17_base"]
CODEOWNERS = ["@SenexCrenshaw", "@jesserockz"]
DEPENDENCIES = ["spi"]
MULTI_CONF = True

CONF_DEVICEADDRESS = "deviceaddress"

mcp23S17_ns = cg.esphome_ns.namespace("mcp23s17")

mcp23S17 = mcp23S17_ns.class_("MCP23S17", mcp23x17_base.MCP23X17Base, spi.SPIDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.Required(CONF_ID): cv.declare_id(mcp23S17),
            cv.Optional(CONF_DEVICEADDRESS, default=0): cv.uint8_t,
        }
    )
    .extend(mcp23xxx_base.MCP23XXX_CONFIG_SCHEMA)
    .extend(spi.spi_device_schema())
)


async def to_code(config):
    var = await mcp23xxx_base.register_mcp23xxx(config)
    cg.add(var.set_device_address(config[CONF_DEVICEADDRESS]))
    await spi.register_spi_device(var, config)
