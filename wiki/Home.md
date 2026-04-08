# Tasmota IRHVAC — Documentation

## Table of Contents

- [How it works](#how-it-works)
- [Hardware](#hardware)
- [Tasmota configuration](#tasmota-configuration)
- [Installation](#installation)
- [Setup via UI (recommended)](#setup-via-ui-recommended)
- [Setup via YAML (legacy)](#setup-via-yaml-legacy)
- [Configuration reference](#configuration-reference)
- [Services](#services)
- [Template switches example](#template-switches-example)
- [Sending arbitrary IR codes](#sending-arbitrary-ir-codes)
- [Lovelace button card example](#lovelace-button-card-example)

---

## How it works

This integration exposes each IR Air Conditioner as a **climate entity** in Home Assistant. It communicates with a Tasmota IR transceiver over MQTT using the `IRhvac` command and JSON payload.

When you press a button on your real AC remote, the Tasmota device receives the IR signal and publishes the decoded state to MQTT — the entity in HA updates automatically. When you change settings from HA, the integration publishes an `IRhvac` MQTT command that the Tasmota device transmits as an IR signal.

---

## Hardware

Build a Tasmota IR transceiver using an ESP8266 or ESP32 board with an IR LED and an IR receiver. The schematic below shows a typical wiring.

![Schematics](/images/schematics.jpeg)

> **Note:** The 100 Ω resistor marked with a light blue X in the schematic can be omitted.  
> If powering via micro-USB and your board has a `VU` pin, connect the IR LED to `VU` instead of `VIN`.

A fully assembled unit mounted under an AC looks like this:

![Mounted transceivers](/images/multisensors.jpeg)

More info about parts and hardware discussion: [HA Community Thread](https://community.home-assistant.io/t/tasmota-mqtt-irhvac-controler/162915/31)

---

## Tasmota configuration

Flash your ESP device with **Tasmota-ir** (tasmota-ircustom.bin). After flashing, configure the device in the Tasmota web UI:

![Tasmota config](/images/tasmota_config.jpeg)

Open the **Tasmota console**, point your AC remote at the IR receiver and press the power button. You should see output like this (Fujitsu example):

```json
{
  "IrReceived": {
    "Protocol": "FUJITSU_AC",
    "Bits": 128,
    "Data": "0x1463001010FE09304013003008002025",
    "Repeat": 0,
    "IRHVAC": {
      "Vendor": "FUJITSU_AC",
      "Model": 1,
      "Power": "On",
      "Mode": "fan_only",
      "Celsius": "On",
      "Temp": 20,
      "FanSpeed": "Auto",
      "SwingV": "Off",
      "SwingH": "Off",
      "Quiet": "Off",
      "Turbo": "Off",
      "Econo": "Off",
      "Light": "Off",
      "Filter": "Off",
      "Clean": "Off",
      "Beep": "Off",
      "Sleep": -1
    }
  }
}
```

If `Vendor` is not `"Unknown"` and the `IRHVAC` key is present with valid data, the integration will work with your AC.

---

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Go to **Integrations** and click **+ Explore & Download Repositories**.
3. Search for **Tasmota IRHVAC** and install it.
4. Restart Home Assistant.

### Manual

1. Download or clone this repository.
2. Copy the `custom_components/tasmota_irhvac/` folder into your HA `config/custom_components/` directory.
3. Restart Home Assistant.

---

## Setup via UI (recommended)

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Tasmota IRHVAC** and select it.
3. **Step 1 — Required settings:**
   - **Name** — friendly name for the entity.
   - **Vendor / Protocol** — your AC brand (e.g. `SAMSUNG_AC`, `DAIKIN`, `MITSUBISHI_AC`). Start typing to search the built-in list, or enter a custom protocol name.
   - **MQTT Command Topic** — topic used to send IR commands (e.g. `cmnd/tasmota_ir/IRhvac`).
   - **MQTT State Topic** — topic used to receive state updates (e.g. `tele/tasmota_ir/RESULT`).
4. **Step 2 — Advanced settings** (all optional, defaults pre-filled):
   - Temperature range, precision, step.
   - Supported HVAC modes, fan speeds, swing modes.
   - Default states: quiet, turbo, econo, light, filter, clean, beep, sleep.
   - Away preset temperature, external sensors, secondary MQTT topic, and more.
5. Click **Submit**. The entity is created immediately — no restart needed.

To edit settings later, click **Configure** on the device card.

---

## Setup via YAML (legacy)

Add the following to your `configuration.yaml` and restart Home Assistant.

```yaml
climate:
  - platform: tasmota_irhvac
    name: "Kitchen AC"
    command_topic: "cmnd/your_tasmota_device/irhvac"
    # State updated on received IR (includes own TX and original remote)
    state_topic: "tele/your_tasmota_device/RESULT"
    # Optional second state topic (subscribe to both tele and stat)
    state_topic_2: "stat/your_tasmota_device/RESULT"
    # availability_topic: "tele/your_tasmota_device/LWT"  # optional
    temperature_sensor: sensor.kitchen_temperature
    humidity_sensor: sensor.kitchen_humidity     # optional
    power_sensor: binary_sensor.kitchen_ac_power # optional
    vendor: "ELECTRA_AC"
    mqtt_delay: 0.0       # optional - seconds between commands
    min_temp: 16          # optional - default 16
    max_temp: 32          # optional - default 32
    target_temp: 26       # optional - default 26
    initial_operation_mode: "off"  # optional - default "off"
    away_temp: 24         # optional - removes the away preset if omitted
    precision: 1          # optional - 1, 0.5 or 0.1
    supported_modes:
      - "heat"
      - "cool"
      - "dry"
      - "fan_only"
      - "auto"
      - "off"
      # - "auto_fan_only"  # if remote shows Fan but Tasmota says Auto
      # - "fan_only_auto"  # if remote shows Auto but Tasmota says Fan
    supported_fan_speeds:
      - "medium"
      - "high"
      - "min"
      - "max"
      # - "auto_max"   # would display as max
      # - "max_high"   # would display as high
    supported_swing_list:
      - "off"
      - "vertical"
      # - "horizontal"
      # - "both"
    default_quiet_mode: "Off"    # optional
    default_turbo_mode: "Off"    # optional
    default_econo_mode: "Off"    # optional
    hvac_model: "-1"             # optional
    celsius_mode: "On"           # optional
    default_light_mode: "Off"    # optional
    default_filter_mode: "Off"   # optional
    default_clean_mode: "Off"    # optional
    default_beep_mode: "Off"     # optional
    default_sleep_mode: "-1"     # optional
    default_swingv: "high"       # optional
    default_swingh: "left"       # optional
    keep_mode_when_off: True     # optional - required for MITSUBISHI_AC, ECOCLIM, etc.
    ignore_off_temp: False       # optional - keep last temperature displayed when AC is off
    special_mode: ""             # optional - vendor-specific special mode
    # toggle_list:               # optional - features that toggle instead of holding state
    #   - Beep
    #   - Clean
    #   - Econo
    #   - Filter
    #   - Light
    #   - Quiet
    #   - Sleep
    #   - SwingH
    #   - SwingV
    #   - Turbo
```

---

## Configuration reference

| Key | Required | Default | Description |
|---|---|---|---|
| `name` | Yes | — | Friendly name of the entity |
| `vendor` | Yes* | — | AC vendor/protocol (e.g. `SAMSUNG_AC`) |
| `protocol` | Yes* | — | Deprecated alias for `vendor` |
| `command_topic` | Yes | — | MQTT topic to publish IR commands |
| `state_topic` | Yes | — | MQTT topic to subscribe to for state |
| `state_topic_2` | No | — | Optional secondary state topic |
| `availability_topic` | No | Auto-derived | MQTT LWT topic |
| `temperature_sensor` | No | — | Entity ID of a temperature sensor |
| `humidity_sensor` | No | — | Entity ID of a humidity sensor |
| `power_sensor` | No | — | Entity ID of a binary power sensor |
| `min_temp` | No | `16` | Minimum temperature |
| `max_temp` | No | `32` | Maximum temperature |
| `target_temp` | No | `26` | Initial target temperature |
| `precision` | No | `1` | Temperature precision: `1`, `0.5` or `0.1` |
| `temp_step` | No | `1` | Temperature step: `1` or `0.5` |
| `celsius_mode` | No | `"On"` | `"On"` for °C, `"Off"` for °F |
| `initial_operation_mode` | No | `"off"` | HVAC mode at startup |
| `away_temp` | No | — | Temperature for away preset (omit to disable) |
| `supported_modes` | No | See below | List of supported HVAC modes |
| `supported_fan_speeds` | No | See below | List of supported fan speed values |
| `supported_swing_list` | No | `["off", "vertical"]` | List of supported swing modes |
| `keep_mode_when_off` | No | `False` | Keep HVAC mode when AC is turned off. Required for some vendors (MITSUBISHI_AC, ECOCLIM) |
| `ignore_off_temp` | No | `False` | Keep last target temperature displayed when AC is off |
| `mqtt_delay` | No | `0` | Delay in seconds between MQTT commands (useful for grouped devices) |
| `hvac_model` | No | `"-1"` | Vendor-specific model number |
| `special_mode` | No | `""` | Vendor-specific special mode string |
| `toggle_list` | No | `[]` | Features that toggle (do not retain On state) |
| `default_quiet_mode` | No | `"off"` | Default quiet state |
| `default_turbo_mode` | No | `"off"` | Default turbo state |
| `default_econo_mode` | No | `"off"` | Default economy state |
| `default_light_mode` | No | `"off"` | Default light state |
| `default_filter_mode` | No | `"off"` | Default filter state |
| `default_clean_mode` | No | `"off"` | Default clean state |
| `default_beep_mode` | No | `"off"` | Default beep state |
| `default_sleep_mode` | No | `"-1"` | Default sleep value |
| `default_swingv` | No | `""` | Default vertical swing position |
| `default_swingh` | No | `""` | Default horizontal swing position |

*`vendor` and `protocol` are mutually exclusive; one is required.

**Default `supported_modes`:** `cool`, `heat`, `dry`, `auto_fan_only`, `fan_only_auto`  
**Default `supported_fan_speeds`:** `auto_max`, `max_high`, `medium`, `min`

---

## Services

All services accept `entity_id` (required) and an optional `state_mode` (`"SendStore"` or `"StoreOnly"`).

| Service | Field | Values |
|---|---|---|
| `tasmota_irhvac.set_econo` | `econo` | `"on"` / `"off"` |
| `tasmota_irhvac.set_turbo` | `turbo` | `"on"` / `"off"` |
| `tasmota_irhvac.set_quiet` | `quiet` | `"on"` / `"off"` |
| `tasmota_irhvac.set_light` | `light` | `"on"` / `"off"` |
| `tasmota_irhvac.set_filters` | `filters` | `"on"` / `"off"` |
| `tasmota_irhvac.set_clean` | `clean` | `"on"` / `"off"` |
| `tasmota_irhvac.set_beep` | `beep` | `"on"` / `"off"` |
| `tasmota_irhvac.set_sleep` | `sleep` | Any string your AC supports |
| `tasmota_irhvac.set_swingv` | `swingv` | `off` / `auto` / `highest` / `high` / `middle` / `low` / `lowest` |
| `tasmota_irhvac.set_swingh` | `swingh` | `off` / `auto` / `left max` / `left` / `middle` / `right` / `right max` / `wide` |

> **Note:** Only call services for features your AC and Tasmota IRHVAC library actually support.

---

## Template switches example

Expose AC extra features as toggle switches in HA:

```yaml
switch:
  - platform: template
    switches:
      kitchen_climate_econo:
        friendly_name: "Econo"
        value_template: "{{ is_state_attr('climate.kitchen_ac', 'econo', 'on') }}"
        turn_on:
          service: tasmota_irhvac.set_econo
          data:
            entity_id: climate.kitchen_ac
            econo: 'on'
        turn_off:
          service: tasmota_irhvac.set_econo
          data:
            entity_id: climate.kitchen_ac
            econo: 'off'
      kitchen_climate_turbo:
        friendly_name: "Turbo"
        value_template: "{{ is_state_attr('climate.kitchen_ac', 'turbo', 'on') }}"
        turn_on:
          service: tasmota_irhvac.set_turbo
          data:
            entity_id: climate.kitchen_ac
            turbo: 'on'
        turn_off:
          service: tasmota_irhvac.set_turbo
          data:
            entity_id: climate.kitchen_ac
            turbo: 'off'
```

Repeat the same pattern for `quiet`, `light`, `filters`, `clean`, `beep`, and `sleep`.

---

## Sending arbitrary IR codes

Add these scripts to your `scripts.yaml` to send HEX or RAW IR codes to any Tasmota device. Name your devices using a room name (lowercase) followed by `Multisensor` (e.g. `kitchenMultisensor`).

```yaml
ir_code:
  sequence:
    - data_template:
        payload: '{"Protocol":"{{ protocol }}","Bits":{{ bits }},"Data":"0x{{ data }}"}'
        topic: 'cmnd/{{ room }}Multisensor/irsend'
      service: mqtt.publish

ir_raw:
  sequence:
    - data_template:
        payload: '0, {{ data }}'
        topic: 'cmnd/{{ room }}Multisensor/irsend'
      service: mqtt.publish
```

---

## Lovelace button card example

Use the `custom:button-card` plugin to trigger IR codes from your dashboard.

```yaml
type: vertical-stack
cards:
  - type: vertical-stack
    cards:
      - type: custom:button-card
        icon: mdi:power
        name: Turn On Audio
        color: white
        style:
          - background: green
        action: service
        service:
          domain: script
          action: ir_code
          data:
            protocol: SONY
            bits: 12
            data: A80
            room: kitchen

      - type: custom:button-card
        icon: mdi:power
        name: Turn Off Audio
        color: white
        style:
          - background: red
        action: service
        service:
          domain: script
          action: ir_code
          data:
            protocol: SONY
            bits: 12
            data: E85
            room: kitchen
```
