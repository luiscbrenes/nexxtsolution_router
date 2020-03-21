![GitHub release (latest by date)](https://img.shields.io/github/v/release/luiscbrenes/nexxtsolution_router?style=for-the-badge) ![GitHub Release Date](https://img.shields.io/github/release-date/luiscbrenes/nexxtsolution_router?style=for-the-badge)

# Nexxt Solution integration for Home Assistant

The nexxtsolution_router platform allows for presence detection by listing devices connected to your Nexxt Solution router.

It was tested with a Nexxt Solution Nebula 1200 Firmware version V15.03.4.14_EN

The component is a modified version of https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/huawei_router.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `nexxtsolution_router`.
4. Download _all_ the files from the `custom_components/nexxtsolution_router/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant.
7. Move on to the configuration.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/nexxtsolution_router/__init__.py
custom_components/nexxtsolution_router/device_tracker.py
custom_components/nexxtsolution_router/manifest.json
```

## Example configuration.yaml

```yaml
device_tracker:
  - platform: nexxtsolution_router
    host: 192.168.1.1
    username: admin
    password: YOUR_PASSWORD
```

### Configuration options

| Key        | Type     | Required | Description                                                                                                                                     |
| ---------- | -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `host`     | `string` | `True`   | The hostname or IP address of your access point, e.g., 192.168.1.1.                                                                             |
| `username` | `string` | `True`   | Defaults to `admin`. You should not have to customize it as Nexxt Solution defaults to `admin` on login and only allow you to specify password. |
| `password` | `string` | `True`   | The password for your given local admin account.                                                                                                |

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
