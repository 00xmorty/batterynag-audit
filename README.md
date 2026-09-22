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

### What can this snapshot tell you?

BatteryNag Audit observes power source, battery percentage and charging state. It does not dismiss low-battery notifications or change your settings.

To watch for power-source changes, run the already-downloaded tool:

    ./batterynag-audit --samples 7 --interval 10

A reported transition means the observed power source changed during sampling. It does not identify a faulty component or prove why a notification appeared. No transitions means only that none were observed in this short window; it does not rule out an intermittent issue.

The tool cannot measure charger wattage, cable capability, battery health or whether a GUI warning appeared. If your goal is to silence notifications, this tool does not do that.

If you choose to give feedback, describe whether the output was understandable and useful for your next troubleshooting step. Share only what you are comfortable making public; no full system logs or identifiers are needed.

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
