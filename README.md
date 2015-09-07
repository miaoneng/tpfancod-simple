License BSD3 tpfancod-simple

This program is inspired by tpfancod. However, this tool uses a naive way to control fan speed rather than complex rule

Read temp from sensors -> Convert temp to preset level -> Write level to /proc/acpi/ibm/fan

* Enable fan from kmod: option thinkpad_acpi fan_control=1

* TODO: Add configuration file to control fan speed rather than hardcoded way.
