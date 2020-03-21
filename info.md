# nexxtsolution_router

The nexxtsolution_router platform allows for presence detection by listing devices connected to your Nexxt Solution router.

It was tested with a Nexxt Solution Nebula 1200 Firmware version V15.03.4.14_EN

The component is a modified version of https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/huawei_router

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
| `username` | `string` | `False`  | Defaults to `admin`. You should not have to customize it as Nexxt Solution defaults to `admin` on login and only allow you to specify password. |
| `password` | `string` | `True`   | The password for your given local admin account.                                                                                                |

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
