# BatteryNag Audit

BatteryNag Audit is a dependency-free, read-only CLI that samples the power source and battery state behind repeated low-battery warnings. It helps distinguish an expected warning at 10% or below from a charger, cable, dock, or port that appears to flap between power sources.

It does **not** dismiss notifications. That is intentional: hiding a battery warning can conceal a real charging failure.

## Run

Python 3.9+ is required. macOS uses the built-in `pmset`; Linux reads the standard `/sys/class/power_supply` interface.

```sh
curl -LO https://github.com/00xmorty/batterynag-audit/releases/latest/download/batterynag-audit
chmod +x batterynag-audit
./batterynag-audit
```

Watch for source changes over one minute:

```sh
./batterynag-audit --samples 7 --interval 10
```

Machine-readable output:

```sh
./batterynag-audit --json
```

## Example

Synthetic example:

```text
BatteryNag Audit — read-only power snapshot
Sample 1: source=AC Power battery=9% state=charging
Sample 2: source=Battery Power battery=9% state=discharging
Transitions: 1
Assessment: power source changed during sampling; inspect the cable, dock, charger, and port
Safety: no alerts, settings, files, or processes were changed.
Limit: a short sample cannot prove why a notification appeared.
```

## Safety

- Read-only: no notification dismissal, preference changes, file writes, process control, `sudo`, telemetry, or network calls.
- Output contains only power source, percentage, charge state, and aggregate assessment; it omits hostnames, usernames, serial numbers, and device identifiers.
- The tool recommends physical inspection rather than suppressing a potentially important warning.

## Limitations

- A short observation window cannot prove the root cause of a popup or intermittent charging fault.
- macOS output depends on the undocumented stability of `pmset -g batt` text formatting.
- Linux hardware and drivers vary; systems without a standard battery interface report `n/a`.
- The tool cannot measure charger wattage, cable capability, battery health, electrical safety, or whether a GUI warning actually appeared.
- It does not replace Apple/OEM diagnostics or professional inspection for heat, swelling, damaged cables, or unreliable power.

## Development

```sh
python3 -m py_compile batterynag-audit
python3 -m unittest discover -s tests -v
./batterynag-audit --version
./batterynag-audit --fixture tests/fixtures/flapping.txt
```

## License

MIT. See [LICENSE](LICENSE).
