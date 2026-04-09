# Security Analysis — Tasmota IRHVAC

**Date:** 2026-04-09  
**Scope:** Custom Home Assistant integration (`custom_components/tasmota_irhvac/`)  
**Branch:** `claude/security-analysis-rAf9M`

---

## Summary

This document records the security findings identified during an audit of the Tasmota IRHVAC integration and the fixes applied in this branch. The integration is a Python-based Home Assistant component that controls IR air conditioners via Tasmota devices over MQTT.

---

## Threat Model

| Trust Boundary | Notes |
|----------------|-------|
| Home Assistant instance | Trusted. Authentication delegated to HA. |
| MQTT broker | Semi-trusted. Assumed to be on a local network. A compromised broker is the primary external threat. |
| MQTT message payload | **Untrusted.** Core attack surface — all findings below relate to this boundary. |
| HA state store (`.storage/`) | Semi-trusted. Could be tampered with if filesystem access is gained. |

---

## Findings & Fixes Applied

### HIGH — Missing type validation on MQTT payload fields

**File:** `climate.py` (function `state_message_received`)  
**Risk:** A malformed or malicious MQTT message could send non-string values for fields such as `Power`, `Mode`, `Celsius`, `Quiet`, `Turbo`, `Econo`, `Light`, `Filter`, `Clean`, `Beep`, `SwingV`, `SwingH`, and `FanSpeed`. Calling `.lower()` on a non-string (e.g. an integer or dict) raises `AttributeError`, crashing the message handler and leaving the entity in an inconsistent state.

**Fix:** Added `isinstance(val, str)` guard before every `.lower()` call. Non-string values are silently ignored, preserving the previous state.

---

### HIGH — Temperature value accepted without bounds check

**File:** `climate.py` (function `state_message_received`)  
**Risk:** The incoming `Temp` field was checked only for `> 0`, allowing any numeric value (e.g. `9999`) to be stored as the target temperature without validation against the configured `min_temp`/`max_temp` range. No type check was performed either.

**Fix:** Temperature is now parsed with `float()` inside a `try/except`, and the value is only accepted if it falls within `[self._min_temp, self._max_temp]`.

---

### HIGH — MQTT topic validation absent in config flow UI

**File:** `config_flow.py`  
**Risk:** The `CONF_COMMAND_TOPIC` and `CONF_STATE_TOPIC` fields in the UI config flow used a bare `TextSelector()` with no validation. This allowed topics containing wildcards (`#`, `+`) or null bytes to be saved, which are invalid for MQTT publish topics and could cause unexpected broker behaviour. By contrast, the YAML-based `platform_schema` correctly used `mqtt.valid_publish_topic`.

**Fix:** Added `_is_valid_mqtt_topic()` helper that rejects empty strings, null bytes, and wildcard characters. This validator is called in both `async_step_user` (initial setup) and `TasmotaIrhvacOptionsFlow.async_step_init` (edit flow), returning the error key `invalid_mqtt_topic` on failure.

---

### MEDIUM — Payload size not limited before JSON parsing

**File:** `climate.py` (function `state_message_received`)  
**Risk:** `json.loads()` was called on the raw MQTT payload with no prior size check. A malicious or malfunctioning broker could send a very large message, consuming significant memory and CPU during parsing (denial of service).

**Fix:** Added a 10 240-byte (10 KB) size check before `json.loads()`. Messages exceeding this limit are rejected with an error log entry. This limit is well above the maximum realistic IRHVAC payload size (~500 bytes).

**Note:** Raw payload content is no longer logged at `DEBUG` level to avoid leaking AC state information in log files.

---

### MEDIUM — Division by zero in temperature rounding

**File:** `climate.py` (function `send_ir`)  
**Risk:** The expression `round(target / self._temp_precision) * self._temp_precision` raises `ZeroDivisionError` if `_temp_precision` is `0`. Although the configuration selects from a fixed set of values (`0.1`, `0.5`, `1.0`), a corrupted config entry or future code change could introduce a zero value.

**Fix:** Added a conditional guard: if `_temp_precision` is falsy (zero), the raw target temperature is used directly, preventing a crash.

---

### MEDIUM — Availability topic derived without segment validation

**File:** `climate.py` (`__init__`)  
**Risk:** When no explicit `availability_topic` is configured, the code splits `self.topic` on `/` and accesses `path[1]`. If the topic has fewer than two segments (e.g. a single word with no `/`), this raises `IndexError` at startup, preventing the entity from loading.

**Fix:** Added `len(path) >= 2` check before accessing `path[1]`. If the topic has too few segments, a warning is logged and the availability topic is left as `None` (no availability tracking).

---

### MEDIUM — State restore applies values without type validation

**File:** `climate.py` (`async_added_to_hass`)  
**Risk:** When the integration restores its state from the HA state store on startup, attributes are applied via `setattr(self, "_" + prop, val)` without checking the type of `val`. If the state file is corrupted or tampered with, a non-string attribute (e.g. a dict or list) could be set, causing crashes or incorrect behaviour in later string operations.

**Fix:** Added `isinstance(val, str)` guard before `setattr`, so only string values are restored. This matches the expected type for all entries in `ATTRIBUTES_IRHVAC`.

---

## Out of Scope / Accepted Risks

| Issue | Rationale |
|-------|-----------|
| No MQTT message signing/replay protection | Architectural limitation; would require changes to the Tasmota firmware protocol. Mitigated by keeping the MQTT broker on a trusted LAN. |
| Custom vendor strings not regex-validated | Low impact; vendor is only used for payload matching and MQTT publish, not executed. |
| `asyncio.sleep(3)` in async handler (`state_message_received`) | Functional choice to debounce the power sensor check; not a security issue. |
| No per-device rate limiting on service calls | Home Assistant's own rate limiting applies. Acceptable for home-automation context. |

---

## Recommendations (Not Yet Implemented)

1. **MQTT TLS:** Ensure the Home Assistant MQTT integration is configured with TLS to encrypt traffic between HA and the broker.
2. **Broker ACLs:** Restrict MQTT topic ACLs so only the Tasmota device and HA can publish/subscribe to device topics.
3. **`invalid_mqtt_topic` translation key:** Add the error string to `strings.json` / `translations/en.json` so the UI shows a human-readable message when an invalid topic is entered.
