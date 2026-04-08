[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/hacs_repository/?owner=nemiro-TECH&repository=Tasmota-IRHVAC&category=integration)
[![GitHub Release](https://img.shields.io/github/release/nemiro-TECH/Tasmota-IRHVAC.svg?style=for-the-badge&color=blue)](https://github.com/hristo-atanasov/Tasmota-IRHVAC/releases)
[![HA Minimum Version](https://img.shields.io/badge/Home%20Assistant-2024.11%2B-blue?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![License](https://img.shields.io/github/license/nemiro-TECH/Tasmota-IRHVAC.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/nemiro-TECH/Tasmota-IRHVAC?style=for-the-badge)](https://github.com/nemiro-TECH/Tasmota-IRHVAC/stargazers)

# Tasmota IRHVAC

**Home Assistant integration for controlling IR Air Conditioners via Tasmota IR transceivers over MQTT.**

Control hundreds of AC models out of the box. The integration exposes each air conditioner as a native **climate entity** — supporting modes, fan speeds, swing, presets, and vendor-specific features like turbo, econo, quiet, sleep, and more.

---

## Features

- Works with any AC supported by the Tasmota IRHVAC library (hundreds of models)
- Native climate entity with full HA thermostat card support
- Real-time state sync when the original remote is used alongside the transceiver
- Optional external sensors for temperature, humidity, and power state
- Extra services: turbo, econo, quiet, light, filter, clean, beep, sleep, swing
- **UI setup wizard** — add devices without editing any YAML

---

## Installation

### HACS (recommended)

This integration is not in the HACS default store yet — you need to add it as a **custom repository** first.

**Option A — one-click (recommended):**

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=hristo-atanasov&repository=Tasmota-IRHVAC&category=integration)

**Option B — manually:**

1. Open HACS in Home Assistant
2. Click the three-dot menu (⋮) in the top-right corner and select **Custom repositories**
3. Paste `https://github.com/hristo-atanasov/Tasmota-IRHVAC` in the URL field, set category to **Integration**, and click **Add**
4. Search for **Tasmota IRHVAC** and install it
5. Restart Home Assistant

### Manual

Copy `custom_components/tasmota_irhvac/` into your `config/custom_components/` directory and restart.

---

## Quick start

After installation, go to **Settings → Devices & Services → Add Integration** and search for **Tasmota IRHVAC**.

The setup wizard will guide you through two steps:

1. **Required** — device name, AC vendor, MQTT command topic, MQTT state topic
2. **Advanced** — temperature range, supported modes, fan speeds, swing, default states, external sensors, and more (all optional with sensible defaults)

> **YAML users:** The legacy `platform: tasmota_irhvac` configuration continues to work unchanged.

---

## Documentation

Full documentation is available on the [**Wiki**](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki):

- [How it works](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#how-it-works)
- [Hardware & wiring](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#hardware)
- [Tasmota configuration](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#tasmota-configuration)
- [UI setup](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#setup-via-ui-recommended)
- [YAML configuration reference](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#configuration-reference)
- [Services](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#services)
- [Template switches](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#template-switches-example)
- [Sending arbitrary IR codes](https://github.com/hristo-atanasov/Tasmota-IRHVAC/wiki/Home#sending-arbitrary-ir-codes)

---

## Community

- [HA Community Thread](https://community.home-assistant.io/t/tasmota-mqtt-irhvac-controler/162915/31)
- [Issue Tracker](https://github.com/hristo-atanasov/Tasmota-IRHVAC/issues)
