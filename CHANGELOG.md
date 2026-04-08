# Changelog

## [2026.4.5] - 2026-04-08

### Added

- **UI Config Flow** — AC devices can now be created directly from the Home Assistant interface, without editing `configuration.yaml`.
  - **Step 1 (Required):** Device name, AC vendor/protocol (searchable dropdown with 45+ known brands plus free-text input), MQTT command topic, MQTT state topic.
  - **Step 2 (Advanced):** All optional settings — temperature range, precision, supported HVAC/fan/swing modes, default states (quiet, turbo, econo, light, filter, clean, beep, sleep), away preset temperature, external sensors (temperature, humidity, power), secondary MQTT topic, availability topic, MQTT delay, model number, special mode, toggle list.
  - **Options flow:** After creation, all settings can be edited through a single-page form via *Settings → Devices & Services → Configure*.
- **Device registry integration** — each AC entity now appears as a proper HA device with the vendor set as the manufacturer.

### Changed

- `__init__.py` now handles config entry lifecycle (`async_setup_entry`, `async_unload_entry`). Reloads the entry automatically when options are saved.
- `climate.py` service registration is now idempotent — safe whether entities are created via YAML or config entry.

### Notes

- **Existing YAML configurations are fully preserved.** The `platform: tasmota_irhvac` setup still works as before — no migration required.
- New installations are encouraged to use the UI flow instead of manual YAML configuration.
