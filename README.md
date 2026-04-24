# pi

Infrastructure and services running on my Raspberry Pi 4 (8GB).

## Hardware

- Raspberry Pi 4 Model B — 8GB RAM
- OS: Raspberry Pi OS Trixie (64-bit)

## Repo Structure

```
pi/
├── README.md
├── provision/
│   ├── user-data           # cloud-init user config (SSH keys, user creation)
│   ├── network-config      # cloud-init WiFi config (netplan format)
│   └── NOTES.md            # what worked and what didn't
├── system/
│   ├── services/           # systemd service files
│   └── config/             # system config files
└── services/
    ├── webserver/           # web server config (nginx/caddy)
    └── cloudflare/          # cloudflare tunnel config
```

## Provisioning

The Pi is set up headless using cloud-init. Config files live in `provision/`.

### What worked

- **User creation** via `user-data` — user, sudo group, and SSH authorized key all applied correctly on first boot
- **SSH key auth** — passwordless login with ed25519 key worked out of the box
- **`avahi-daemon`** — installed automatically, `pi.local` hostname resolution works

### What didn't work

- **WiFi via `network-config`** — the netplan cloud-init config did not apply on first boot (likely a Trixie/cloud-init compatibility issue). WiFi had to be configured manually on the Pi after booting with a monitor.
- **`rpi-imager` on Arch Linux** — the GUI failed to launch under sudo due to Wayland/X11 display permission issues, and also triggered io_uring errors when writing. Ended up flashing with `dd` instead (see below).

### Flashing the SD card (Arch Linux)

The official Raspberry Pi Imager had issues on Arch with the Zen kernel — io_uring errors caused the write to hang. Use `dd` directly instead:

```bash
# Decompress and flash in one step
xz -dc 2026-04-21-raspios-trixie-arm64.img.xz | sudo dd of=/dev/sdX bs=4M status=progress conv=fsync
```

Then mount the boot partition and drop in your cloud-init configs before first boot:

```bash
sudo mkdir -p /mnt/piboot
sudo mount /dev/sdX1 /mnt/piboot

# Copy configs
sudo cp provision/user-data /mnt/piboot/user-data
sudo cp provision/network-config /mnt/piboot/network-config

sudo umount /mnt/piboot
```

### Connecting after first boot

```bash
ssh haakon@pi.local
```

## Services

### Web Server

> Work in progress

### Cloudflare Tunnel

> Work in progress — goal is to expose the web server publicly without port forwarding.
