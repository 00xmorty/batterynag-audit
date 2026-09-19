# Security Policy

## Supported version

Security fixes are provided for the latest release.

## Reporting

Open a GitHub issue for non-sensitive reports. For a vulnerability that should not be public, use GitHub's private vulnerability reporting for this repository.

## Safety boundary

BatteryNag Audit only reads local battery/power status. It does not dismiss alerts, change settings, write files, control processes, invoke `sudo`, send telemetry, or make network requests. Reports should never include device serial numbers or private system logs.
