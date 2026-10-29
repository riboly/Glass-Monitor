# GlassMonitor — Windows Floating System Monitor

A lightweight, always-on-top floating widget for Windows that shows live
hardware stats and network speed in a frosted-glass panel, styled after iOS
glassmorphism. It docks to the right side of the screen by default, stays out
of your way, and uses almost no resources itself.

No Electron, no PyQt — just Python's standard `tkinter` plus `psutil` and
NVML. Idle CPU usage is typically under 1%, memory around 30–50 MB.

## Who Is This For

- **Everyday Windows users** who want CPU, memory, GPU, and network stats at
  a glance, without opening Task Manager or running a heavy overlay.
- **Gamers and video watchers**: the widget automatically hides itself when
  a fullscreen app is in the foreground, and comes back when you leave it.
- **VPS users**: an optional traffic card tracks your server's bandwidth
  quota against a traffic API, with green / yellow / red progress coloring.
- **Minimal-desktop fans**: a small glass panel with themes, rounded corners,
  adjustable opacity, and per-card double-click shortcuts.

## Features

### Cards — all toggleable and reorderable

The window height adjusts automatically to the cards you enable. Each card
can be shown or hidden, and you can drag cards (or use the up/down buttons
in Settings) to change their order.

| Card | What it shows |
|------|---------------|
| **Clock & Date** | Large time, plus date, weekday, and week number (weekends highlighted) |
| **Hardware** | CPU / memory / GPU usage as true-alpha anti-aliased rings (6x supersampled masks), plus temperatures |
| **Net Speed** | Live upload / download speed in two capsules |
| **Speed Chart** | Dual-color area chart of network throughput, with peak values |
| **Disk** | Read / write rates for all disks, plus per-partition usage bars that change color at thresholds |
| **Top Processes** | Top 3 processes by CPU usage (name, memory, CPU%) |
| **System Info** | Uptime, VRAM usage, battery status (battery row is omitted automatically on desktops without a battery) |
| **VPS Traffic** | Bandwidth quota progress bar: green under 50%, yellow at 50–70%, red above 70% |

### Temperatures

- **GPU temperature** is read through NVML (`nvidia-ml-py`). Validated on
  an RTX 4060. Without an NVIDIA GPU, GPU readings show as N/A.
- **CPU temperature** is read through the bundled helper
  `bin/cpu_temp_helper.exe`, built on OpenHardwareMonitorLib
  (source in `vendor/cpu_temp_helper.cs`). The helper only starts when a
  temperature card or a CPU temperature alert actually needs it, and exits
  automatically when no longer needed. If a temperature shows as `—`, check
  that the helper exists; some machines need administrator rights to read
  MSR sensors.

### Interaction

| Action | Behavior |
|--------|----------|
| Left-drag | Move the window (position is saved to `window_pos.json` on release) |
| Double-click a card | Runs that card's assigned action (customizable, see below) |
| Right-click | Menu: Settings, Show/Hide, Always on top, Collapse, Exit |
| Tray icon right-click | Menu: Settings, Show/Hide, Always on top, Exit |
| Fullscreen app in foreground | Widget hides automatically, returns when you leave fullscreen |

There is deliberately **no close button on the window** — quit from the tray
menu or the right-click menu.

### Double-click actions — 40 to choose from

Every card can be bound to its own double-click action, configured in
Settings. The built-in actions cover system tools (Task Manager, Resource
Monitor, Disk Management, Services, Event Viewer, …), terminals
(PowerShell, Command Prompt), folders (This PC, Downloads, Recycle Bin),
system settings pages, desktop utilities (show/hide desktop icons, mute,
lock screen, screenshot), and widget controls (open settings, toggle
always-on-top, collapse, hide, refresh traffic now).

Only non-destructive actions are included — nothing that shuts down,
sleeps, or empties the Recycle Bin, because a double-click is easy to hit
by accident. Adding a new action is a one-line change in `actions.py`'s
`ACTIONS` registry; it then appears in the Settings dropdown automatically.

### Settings

Everything is configured from the tray / right-click **Settings** window and
written to `config.json` in the program directory, so your layout, theme,
and card order travel with the folder if you move it.

| Setting | Notes |
|---------|-------|
| Card visibility & order | 8 cards, each toggleable, reorderable |
| Lock position | Prevents accidental dragging |
| Auto-hide on fullscreen | Hides over fullscreen apps |
| Edge snap distance | 0–64 px, 0 disables snapping |
| Themes | 15 built-in schemes (Midnight Glass, Deep Sea, Aurora Mint, Cobalt Dusk, …) |
| Corner radius | 8–36 px, default 22 |
| Window / card opacity | Sliders, applied live as you drag |
| Text halo strength | 0–100%, keeps text readable on light wallpapers, 0 disables it |
| Autostart | Writes a `GlassMonitor.bat` to the user's Startup folder |
| Start pinned / visible | Linked to the tray menu checkmarks |
| Layout preset / width | Compact, Standard, Relaxed presets, or a custom width of 260–420 px |
| Click-through | The whole window ignores mouse input; restore it from the tray menu |
| Resource alerts | Threshold notifications for CPU/GPU temperature, memory, disk, and VPS traffic, with duration, cooldown, and hysteresis |
| Diagnostics | Collection latency, sensor availability, traffic status, and config paths |
| Global hotkey | Configurable show/hide hotkey; showing the widget via hotkey forces it always-on-top |
| VPS traffic display | Toggle for the bottom traffic bar, plus update interval (1–120 minutes) |

### VPS traffic API (optional)

Configure it under the `traffic` section of `config.json`:

```json
"traffic": {
  "enabled": true,
  "url": "https://your-traffic-api.example.com/?key=YOUR_KEY",
  "proxy": "http://127.0.0.1:7890",
  "interval_min": 5
}
```

- Traffic is fetched preferentially through the configured proxy (e.g. a
  local mihomo instance), falling back to a direct connection.
- On failure, the last successful data is kept and marked as cached.
- After 10 consecutive failures, the card reports a fetch failure.
- Usage = upload + download; percentage = used / total.

Sharing safety: your traffic API URL and proxy live only in your own
`config.json` — never in the source code. Before sharing your config,
clear `traffic.url` and `traffic.proxy`, and do not include old
`config.json.bak` files. `config.example.json` ships without any personal
addresses and is safe to share as a reference.

### Low-resource design

1. **No Electron / no PyQt**: standard `tkinter` + `psutil` + NVML only.
2. **1-second refresh**, with non-blocking `cpu_percent(interval=None)`.
3. **No subprocesses on the hot path** — no per-second `nvidia-smi` or
   slow WMI calls.
4. Network history keeps only `history_points` samples; system metrics are
   collected on a background thread.
5. GPU / CPU temperature sensors and other collectors start lazily, only
   when an enabled card or alert needs them.

## Requirements

- Windows 10 / 11
- Python 3.10+ (developed on Python 3.14)
- NVIDIA graphics driver for GPU usage / temperature (optional; without it
  GPU readings show as N/A)

## Quick Start

```bat
pip install -r requirements.txt
py monitor.py
```

Or simply double-click `run.bat`.

## Configuration

All user settings live in `config.json` in the program directory (see
`config.example.json` for the full default set with documentation).
Manually editing the file requires a restart to take effect. Window
position is stored separately in `window_pos.json`; deleting it restores
the default right-side layout.

If an older version stored data under `%LOCALAPPDATA%\GlassMonitor`, the
program migrates those files back into the program directory automatically
on first launch when they are missing there.

## Project Structure

```
monitor.py          # Entry point
glass_ui.py         # Floating window: layout, interaction, per-frame compositing
aa_draw.py          # True-alpha anti-aliased drawing (rings, curves, text, bars)
layered.py          # Layered-window wrapper (UpdateLayeredWindow)
metrics.py          # Metric collection (psutil / NVML / optional WMI temperatures)
metrics_worker.py   # Background collection with thread-safe snapshots
alerting.py         # Threshold duration / cooldown / hysteresis state machine
cards_meta.py       # Card registry (order, display names, default switches)
actions.py          # Double-click action registry (add an action here only)
themes.py           # Color schemes
settings_ui.py      # Settings window
win_display.py      # Multi-monitor work-area and position constraints
app_storage.py      # User data migration, atomic writes, local backups
autostart.py        # Startup registration
hotkey_mgr.py       # Global hotkey handling
instance_guard.py   # Single-instance guard
traffic.py          # VPS traffic API client
gpu_wddm.py         # GPU helpers (WDDM)
config.example.json # Shareable default configuration, no personal addresses
requirements.txt    # Dependencies
run.bat             # One-click launch
tests/              # Core tests
```

## Contributing

Issues and pull requests are welcome. If you add a feature, please keep
the low-resource discipline above: no heavy frameworks, no subprocesses on
the hot path, and new double-click actions must stay non-destructive.

## License

MIT — see [LICENSE](LICENSE).
