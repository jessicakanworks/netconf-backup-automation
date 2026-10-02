#!/usr/bin/env python3
"""Back up device running configurations and commit them to Git."""
import argparse, datetime, os, pathlib, sys
import yaml
from netmiko import ConnectHandler
import git

SHOW_CMD = {"cisco_ios": "show running-config", "cisco_xe": "show running-config",
            "juniper_junos": "show configuration | display set"}

def backup(dev, outdir):
    conn = ConnectHandler(device_type=dev["device_type"], host=dev["ip"],
                          username=os.environ["NET_USER"], password=os.environ["NET_PASS"])
    try:
        cfg = conn.send_command(SHOW_CMD[dev["device_type"]], read_timeout=90)
    finally:
        conn.disconnect()
    path = outdir / f"{dev['host']}.cfg"
    path.write_text(cfg)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", default="inventory.yml")
    ap.add_argument("--outdir", default="backups")
    args = ap.parse_args()
    outdir = pathlib.Path(args.outdir); outdir.mkdir(exist_ok=True)
    devices = yaml.safe_load(open(args.inventory))["devices"]
    ok, failed = [], []
    for dev in devices:
        try:
            backup(dev, outdir); ok.append(dev["host"])
        except Exception as e:  # keep going, report at end
            failed.append((dev["host"], str(e)))
    repo = git.Repo(".")
    repo.git.add(str(outdir))
    if repo.is_dirty(untracked_files=True):
        repo.index.commit(f"config backup {datetime.date.today()} ({len(ok)} ok, {len(failed)} failed)")
    print(f"backed up: {ok}")
    for h, err in failed:
        print(f"FAILED {h}: {err}", file=sys.stderr)
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
