"""Config flow for Tasmota IRHVAC integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_DIFFUSE,
    FAN_FOCUS,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_MIDDLE,
    FAN_OFF,
    FAN_ON,
    FAN_TOP,
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_OFF,
    SWING_VERTICAL,
    HVACMode,
)
from homeassistant.const import CONF_NAME, PRECISION_HALVES, PRECISION_TENTHS, PRECISION_WHOLE
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from .const import (
    CONF_AVAILABILITY_TOPIC,
    CONF_AWAY_TEMP,
    CONF_BEEP,
    CONF_CELSIUS,
    CONF_CLEAN,
    CONF_COMMAND_TOPIC,
    CONF_ECONO,
    CONF_FAN_LIST,
    CONF_FILTER,
    CONF_HUMIDITY_SENSOR,
    CONF_IGNORE_OFF_TEMP,
    CONF_INITIAL_OPERATION_MODE,
    CONF_KEEP_MODE,
    CONF_LIGHT,
    CONF_MAX_TEMP,
    CONF_MIN_TEMP,
    CONF_MODEL,
    CONF_MODES_LIST,
    CONF_MQTT_DELAY,
    CONF_POWER_SENSOR,
    CONF_PRECISION,
    CONF_QUIET,
    CONF_SLEEP,
    CONF_SPECIAL_MODE,
    CONF_STATE_TOPIC,
    CONF_SWING_LIST,
    CONF_SWINGH,
    CONF_SWINGV,
    CONF_TARGET_TEMP,
    CONF_TEMP_SENSOR,
    CONF_TEMP_STEP,
    CONF_TOGGLE_LIST,
    CONF_TURBO,
    CONF_VENDOR,
    DEFAULT_CONF_BEEP,
    DEFAULT_CONF_CELSIUS,
    DEFAULT_CONF_CLEAN,
    DEFAULT_CONF_ECONO,
    DEFAULT_CONF_FILTER,
    DEFAULT_CONF_KEEP_MODE,
    DEFAULT_CONF_LIGHT,
    DEFAULT_CONF_MODEL,
    DEFAULT_CONF_QUIET,
    DEFAULT_CONF_SLEEP,
    DEFAULT_CONF_TURBO,
    DEFAULT_FAN_LIST,
    DEFAULT_IGNORE_OFF_TEMP,
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_TEMP,
    DEFAULT_MQTT_DELAY,
    DEFAULT_NAME,
    DEFAULT_PRECISION,
    DEFAULT_TARGET_TEMP,
    DOMAIN,
    HVAC_FAN_AUTO,
    HVAC_FAN_AUTO_MAX,
    HVAC_FAN_MAX,
    HVAC_FAN_MAX_HIGH,
    HVAC_FAN_MEDIUM,
    HVAC_FAN_MIN,
    HVAC_MODES,
    TOGGLE_ALL_LIST,
)

CONF_STATE_TOPIC_2 = CONF_STATE_TOPIC + "_2"

KNOWN_VENDORS = [
    "AIRTON", "AIRWELL", "AMCOR", "ARGO", "AUX", "BOSCH",
    "CARRIER_AC", "COOLIX", "CORONA_AC", "DAIKIN", "DAIKIN128",
    "DAIKIN2", "DAIKIN64", "DELONGHI_AC", "ECOCLIM", "ELECTRA_AC",
    "FUJITSU_AC", "GOODWEATHER", "GORENJE", "GREE", "HAIER_AC",
    "HISENSE_AC", "HITACHI_AC", "KELVINATOR", "LG", "LG2", "MIDEA",
    "MITSUBISHI_AC", "MITSUBISHI136", "MITSUBISHI112",
    "MITSUBISHI_HEAVY_152", "MITSUBISHI_HEAVY_88", "NEOCLIMA",
    "PANASONIC_AC", "PIONEER", "SAMSUNG_AC", "SANYO_AC",
    "SHARP_AC", "TCL112AC", "TECO", "TOSHIBA_AC", "VESTEL_AC",
    "VOLTAS", "WHIRLPOOL_AC", "YORK",
]

# Deduplicated fan mode list (HVAC_FAN_AUTO="auto" = FAN_AUTO, HVAC_FAN_MEDIUM="medium" = FAN_MEDIUM)
ALL_FAN_MODES = list(dict.fromkeys([
    FAN_ON, FAN_OFF, FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH,
    FAN_MIDDLE, FAN_FOCUS, FAN_DIFFUSE, FAN_TOP,
    HVAC_FAN_MIN, HVAC_FAN_MEDIUM, HVAC_FAN_MAX, HVAC_FAN_AUTO,
    HVAC_FAN_MAX_HIGH, HVAC_FAN_AUTO_MAX,
]))

DEFAULT_MODES_LIST = [
    HVACMode.OFF,  # Required by HA 2024.1+ when ClimateEntityFeature.TURN_OFF is declared
    HVACMode.COOL, HVACMode.HEAT, HVACMode.DRY,
    # HVAC_MODE_AUTO_FAN, HVAC_MODE_FAN_AUTO,
    HVACMode.AUTO, HVACMode.FAN_ONLY,
]
DEFAULT_SWING_LIST = [SWING_OFF, SWING_VERTICAL]

STEP1_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): TextSelector(),
    vol.Required(CONF_VENDOR): SelectSelector(
        SelectSelectorConfig(
            options=KNOWN_VENDORS,
            custom_value=True,
            mode=SelectSelectorMode.DROPDOWN,
        )
    ),
    vol.Required(CONF_COMMAND_TOPIC): TextSelector(),
    vol.Required(CONF_STATE_TOPIC): TextSelector(),
})


def _step2_fields(defaults: dict) -> dict:
    """Return the voluptuous field dict for the advanced/options step."""
    return {
        # Temperature
        vol.Optional(CONF_MIN_TEMP, default=defaults.get(CONF_MIN_TEMP, DEFAULT_MIN_TEMP)): NumberSelector(
            NumberSelectorConfig(min=0, max=100, step=0.5, mode=NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_MAX_TEMP, default=defaults.get(CONF_MAX_TEMP, DEFAULT_MAX_TEMP)): NumberSelector(
            NumberSelectorConfig(min=0, max=100, step=0.5, mode=NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_TARGET_TEMP, default=defaults.get(CONF_TARGET_TEMP, DEFAULT_TARGET_TEMP)): NumberSelector(
            NumberSelectorConfig(min=0, max=100, step=0.5, mode=NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_PRECISION, default=str(defaults.get(CONF_PRECISION, DEFAULT_PRECISION))): SelectSelector(
            SelectSelectorConfig(options=[str(PRECISION_TENTHS), str(PRECISION_HALVES), str(PRECISION_WHOLE)])
        ),
        vol.Optional(CONF_TEMP_STEP, default=str(defaults.get(CONF_TEMP_STEP, PRECISION_WHOLE))): SelectSelector(
            SelectSelectorConfig(options=[str(PRECISION_HALVES), str(PRECISION_WHOLE)])
        ),
        vol.Optional(CONF_CELSIUS, default=defaults.get(CONF_CELSIUS, DEFAULT_CONF_CELSIUS)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        # Modes
        vol.Optional(CONF_MODES_LIST, default=defaults.get(CONF_MODES_LIST, DEFAULT_MODES_LIST)): SelectSelector(
            SelectSelectorConfig(options=HVAC_MODES, multiple=True)
        ),
        vol.Optional(CONF_FAN_LIST, default=defaults.get(CONF_FAN_LIST, DEFAULT_FAN_LIST)): SelectSelector(
            SelectSelectorConfig(options=ALL_FAN_MODES, multiple=True)
        ),
        vol.Optional(CONF_SWING_LIST, default=defaults.get(CONF_SWING_LIST, DEFAULT_SWING_LIST)): SelectSelector(
            SelectSelectorConfig(
                options=[SWING_OFF, SWING_BOTH, SWING_VERTICAL, SWING_HORIZONTAL],
                multiple=True,
            )
        ),
        # Initial / default states
        vol.Optional(
            CONF_INITIAL_OPERATION_MODE,
            default=defaults.get(CONF_INITIAL_OPERATION_MODE, HVACMode.OFF),
        ): SelectSelector(SelectSelectorConfig(options=HVAC_MODES)),
        vol.Optional(CONF_QUIET, default=defaults.get(CONF_QUIET, DEFAULT_CONF_QUIET)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_TURBO, default=defaults.get(CONF_TURBO, DEFAULT_CONF_TURBO)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_ECONO, default=defaults.get(CONF_ECONO, DEFAULT_CONF_ECONO)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_LIGHT, default=defaults.get(CONF_LIGHT, DEFAULT_CONF_LIGHT)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_FILTER, default=defaults.get(CONF_FILTER, DEFAULT_CONF_FILTER)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_CLEAN, default=defaults.get(CONF_CLEAN, DEFAULT_CONF_CLEAN)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_BEEP, default=defaults.get(CONF_BEEP, DEFAULT_CONF_BEEP)): SelectSelector(
            SelectSelectorConfig(options=["on", "off"])
        ),
        vol.Optional(CONF_SLEEP, default=defaults.get(CONF_SLEEP, DEFAULT_CONF_SLEEP)): TextSelector(),
        vol.Optional(CONF_SWINGV, default=defaults.get(CONF_SWINGV, "")): TextSelector(),
        vol.Optional(CONF_SWINGH, default=defaults.get(CONF_SWINGH, "")): TextSelector(),
        # Toggle list
        vol.Optional(CONF_TOGGLE_LIST, default=defaults.get(CONF_TOGGLE_LIST, [])): SelectSelector(
            SelectSelectorConfig(options=TOGGLE_ALL_LIST, multiple=True)
        ),
        # Feature flags
        vol.Optional(CONF_KEEP_MODE, default=defaults.get(CONF_KEEP_MODE, DEFAULT_CONF_KEEP_MODE)): BooleanSelector(),
        vol.Optional(CONF_IGNORE_OFF_TEMP, default=defaults.get(CONF_IGNORE_OFF_TEMP, DEFAULT_IGNORE_OFF_TEMP)): BooleanSelector(),
        # Away preset (0 = disabled)
        vol.Optional(CONF_AWAY_TEMP, default=defaults.get(CONF_AWAY_TEMP, 0)): NumberSelector(
            NumberSelectorConfig(min=0, max=100, step=0.5, mode=NumberSelectorMode.BOX)
        ),
        # Sensors
        vol.Optional(CONF_TEMP_SENSOR, default=defaults.get(CONF_TEMP_SENSOR, "")): TextSelector(),
        vol.Optional(CONF_HUMIDITY_SENSOR, default=defaults.get(CONF_HUMIDITY_SENSOR, "")): TextSelector(),
        vol.Optional(CONF_POWER_SENSOR, default=defaults.get(CONF_POWER_SENSOR, "")): TextSelector(),
        # MQTT extras
        vol.Optional(CONF_AVAILABILITY_TOPIC, default=defaults.get(CONF_AVAILABILITY_TOPIC, "")): TextSelector(),
        vol.Optional(CONF_STATE_TOPIC_2, default=defaults.get(CONF_STATE_TOPIC_2, "")): TextSelector(),
        vol.Optional(CONF_MQTT_DELAY, default=defaults.get(CONF_MQTT_DELAY, DEFAULT_MQTT_DELAY)): NumberSelector(
            NumberSelectorConfig(min=0, max=60, step=0.1, mode=NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_MODEL, default=defaults.get(CONF_MODEL, DEFAULT_CONF_MODEL)): TextSelector(),
        vol.Optional(CONF_SPECIAL_MODE, default=defaults.get(CONF_SPECIAL_MODE, "")): TextSelector(),
    }


def _step2_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(_step2_fields(defaults))


def _options_schema(current: dict) -> vol.Schema:
    """Single-page schema for the options flow (all fields)."""
    return vol.Schema({
        vol.Required(CONF_NAME, default=current.get(CONF_NAME, DEFAULT_NAME)): TextSelector(),
        vol.Required(CONF_VENDOR, default=current.get(CONF_VENDOR, "")): SelectSelector(
            SelectSelectorConfig(
                options=KNOWN_VENDORS,
                custom_value=True,
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(CONF_COMMAND_TOPIC, default=current.get(CONF_COMMAND_TOPIC, "")): TextSelector(),
        vol.Required(CONF_STATE_TOPIC, default=current.get(CONF_STATE_TOPIC, "")): TextSelector(),
        **_step2_fields(current),
    })


class TasmotaIrhvacConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tasmota IRHVAC."""

    VERSION = 1

    def __init__(self) -> None:
        self._step1_data: dict = {}

    async def async_step_user(self, user_input=None):
        """Step 1: required fields (name, vendor, MQTT topics)."""
        errors: dict = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_COMMAND_TOPIC])
            self._abort_if_unique_id_configured()
            self._step1_data = user_input
            return await self.async_step_advanced()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP1_SCHEMA,
            errors=errors,
        )

    async def async_step_advanced(self, user_input=None):
        """Step 2: optional/advanced fields."""
        if user_input is not None:
            return self.async_create_entry(
                title=self._step1_data[CONF_NAME],
                data={**self._step1_data, **user_input},
            )

        return self.async_show_form(
            step_id="advanced",
            data_schema=_step2_schema({}),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return TasmotaIrhvacOptionsFlow(config_entry)


class TasmotaIrhvacOptionsFlow(config_entries.OptionsFlow):
    """Handle Tasmota IRHVAC options (edit after creation)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Single-page form with all device settings."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(current),
        )
