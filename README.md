# netconf-backup-automation

Scheduled configuration backup, diff and compliance checks for Cisco IOS/IOS-XE, Juniper Junos
and Linux hosts. Backups are committed to Git so every change is versioned and auditable.

* `backup.py` – pulls running configs over SSH (netmiko), writes `backups/<host>.cfg`, commits to Git
* `compliance.py` – checks each config against rules in `rules.yml` (e.g. no telnet, banner present, NTP set)
* `ansible/backup.yml` – the same backup done with the `cisco.ios` / `junipernetworks.junos` collections
* `systemd/` – timer that runs the backup nightly at 01:00

```bash
pip install -r requirements.txt
export NET_USER=backup NET_PASS='...'    # or use a vault / secrets manager
python backup.py --inventory inventory.yml
python compliance.py --rules rules.yml backups/*.cfg
```
