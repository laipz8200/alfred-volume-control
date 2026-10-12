# Volume Control

<img src="workflow/icon.png" width="128" alt="Volume Control icon">

Set your Mac's output volume from Alfred. Type `vol 50` and press Return for 50% volume.

## Install

Requires **macOS and Alfred 5 with Powerpack**.

1. [Download Volume Control](https://github.com/laipz8200/alfred-volume-control/releases/latest/download/Volume-Control.alfredworkflow).
2. Open the downloaded `.alfredworkflow` file and install it in Alfred.
3. Keep the default keyword `vol`, or choose your own during setup.

## Use

| Command | Result |
| --- | --- |
| `vol 25` | Set output volume to 25% and unmute |
| `vol 50` | Set output volume to 50% and unmute |
| `vol 0` | Set volume to zero and mute |

Accepts whole numbers from **0 to 100**. Invalid input produces an error notification without changing volume. Successful changes are silent.

To change the prefix later, open **Alfred Preferences → Workflows → Volume Control → Configure Workflow → Keyword**. For example, choose `sound` to use `sound 50`.

## Performance and compatibility

The workflow uses Alfred's cached NSAppleScript action, avoiding a new shell or interpreter process for each invocation. A local check measured about 45 ms for the action in Alfred; first use and other audio devices may take longer. This is action execution time, not keyboard-to-speaker latency.

It controls the currently selected macOS audio output. Devices with fixed hardware volume, such as some HDMI and USB outputs, cannot be adjusted through macOS system volume. No additional runtime dependencies, background service, or network access are required.

## Build and test

The complete workflow, including the AppleScript, is in [`workflow/info.plist`](workflow/info.plist).

```sh
python3 tests/test_workflow.py
python3 build.py
```

Tests require macOS and exercise validation and error handling with the volume command replaced, so they do not change your volume. The build creates `build/Volume-Control.alfredworkflow` using Python's standard library. Building from source requires Python 3; installing the release does not.

The workflow icon was generated with OpenAI image generation.

## Author and license

Created by **[-LAN-](https://github.com/laipz8200)**. Released under the [MIT License](LICENSE).
