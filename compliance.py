#!/usr/bin/env python3
"""Check saved configs against simple regex compliance rules."""
import argparse, re, sys, yaml

def check(cfg_text, rules):
    findings = []
    for r in rules:
        if "must_match" in r and not re.search(r["must_match"], cfg_text, re.M):
            findings.append(f"MISSING: {r['name']}")
        if "must_not_match" in r and re.search(r["must_not_match"], cfg_text, re.M):
            findings.append(f"VIOLATION: {r['name']}")
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default="rules.yml")
    ap.add_argument("configs", nargs="+")
    a = ap.parse_args()
    rules = yaml.safe_load(open(a.rules))["rules"]
    bad = 0
    for path in a.configs:
        findings = check(open(path).read(), rules)
        status = "PASS" if not findings else "FAIL"
        print(f"{status} {path}")
        for f in findings:
            print(f"   - {f}"); bad += 1
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
