# # import csv
# # import re
# # from pathlib import Path
# # import argparse

# # PANEL_NAMES = ["AdPanel", "AdPanel (1)", "AdPanel (2)"]

# # def extract_ar_id(filename_stem):
# #     m = re.match(r'^(ar_[^_]+)', filename_stem, re.IGNORECASE)
# #     return m.group(1) if m else filename_stem

# # def analyze_file(path):
# #     counts = {p: 0 for p in PANEL_NAMES}
# #     durations = {p: 0.0 for p in PANEL_NAMES}
# #     rows = 0
# #     with path.open(newline='', encoding='utf-8') as f:
# #         reader = csv.DictReader(f)
# #         for r in reader:
# #             rows += 1
# #             name = (r.get("panel_name") or "").strip()
# #             try:
# #                 dur = float(r.get("duration_sec") or 0)
# #             except Exception:
# #                 try:
# #                     start = float(r.get("start_unix") or 0)
# #                     end = float(r.get("end_unix") or 0)
# #                     dur = max(0.0, end - start)
# #                 except Exception:
# #                     dur = 0.0
# #             if name in PANEL_NAMES:
# #                 counts[name] += 1
# #                 durations[name] += dur
# #     return {
# #         "file": str(path),
# #         "rows": rows,
# #         "counts": counts,
# #         "durations": durations,
# #         "ar_id": extract_ar_id(path.stem)
# #     }

# # def main(dirpath, outcsv):
# #     base = Path(dirpath)
# #     files = sorted(base.rglob("*.csv"))
# #     fieldnames = [
# #         "file", "ar_id", "rows",
# #         "AdPanel_exist", "AdPanel_count", "AdPanel_total_duration_sec",
# #         "AdPanel (1)_exist", "AdPanel (1)_count", "AdPanel (1)_total_duration_sec",
# #         "AdPanel (2)_exist", "AdPanel (2)_count", "AdPanel (2)_total_duration_sec"
# #     ]
# #     totals_counts = {p:0 for p in PANEL_NAMES}
# #     totals_durs = {p:0.0 for p in PANEL_NAMES}
# #     with open(outcsv, "w", newline='', encoding='utf-8') as out:
# #         writer = csv.DictWriter(out, fieldnames=fieldnames)
# #         writer.writeheader()
# #         for f in files:
# #             res = analyze_file(f)
# #             row = {
# #                 "file": res["file"],
# #                 "ar_id": res["ar_id"],
# #                 "rows": res["rows"],
# #                 "AdPanel_exist": "Yes" if res["counts"]["AdPanel"] > 0 else "No",
# #                 "AdPanel_count": res["counts"]["AdPanel"],
# #                 "AdPanel_total_duration_sec": round(res["durations"]["AdPanel"], 6),
# #                 "AdPanel (1)_exist": "Yes" if res["counts"]["AdPanel (1)"] > 0 else "No",
# #                 "AdPanel (1)_count": res["counts"]["AdPanel (1)"],
# #                 "AdPanel (1)_total_duration_sec": round(res["durations"]["AdPanel (1)"], 6),
# #                 "AdPanel (2)_exist": "Yes" if res["counts"]["AdPanel (2)"] > 0 else "No",
# #                 "AdPanel (2)_count": res["counts"]["AdPanel (2)"],
# #                 "AdPanel (2)_total_duration_sec": round(res["durations"]["AdPanel (2)"], 6),
# #             }
# #             writer.writerow(row)
# #             for p in PANEL_NAMES:
# #                 totals_counts[p] += res["counts"][p]
# #                 totals_durs[p] += res["durations"][p]
# #         totals_row = {
# #             "file": "TOTAL",
# #             "ar_id": "",
# #             "rows": "",
# #             "AdPanel_exist": "Yes" if totals_counts["AdPanel"] > 0 else "No",
# #             "AdPanel_count": totals_counts["AdPanel"],
# #             "AdPanel_total_duration_sec": round(totals_durs["AdPanel"], 6),
# #             "AdPanel (1)_exist": "Yes" if totals_counts["AdPanel (1)"] > 0 else "No",
# #             "AdPanel (1)_count": totals_counts["AdPanel (1)"],
# #             "AdPanel (1)_total_duration_sec": round(totals_durs["AdPanel (1)"], 6),
# #             "AdPanel (2)_exist": "Yes" if totals_counts["AdPanel (2)"] > 0 else "No",
# #             "AdPanel (2)_count": totals_counts["AdPanel (2)"],
# #             "AdPanel (2)_total_duration_sec": round(totals_durs["AdPanel (2)"], 6),
# #         }
# #         writer.writerow(totals_row)
# #     print(f"Wrote summary to {outcsv} ({len(files)} CSV files scanned)")

# # if __name__ == "__main__":
# #     ap = argparse.ArgumentParser(description="Summarize AdPanel occurrences in CSV gaze logs and include ar_xxx id per row.")
# #     ap.add_argument("--dir", "-d", default=".", help="Directory to scan (default: current).")
# #     ap.add_argument("--out", "-o", default="ar_adpanel_summary.csv", help="Output CSV path.")
# #     args = ap.parse_args()
# #     main(args.dir, args.out)


# # ...existing code...
# import csv
# import re
# from pathlib import Path
# import argparse
# from datetime import datetime

# PANEL_NAMES = ["AdPanel", "AdPanel (1)", "AdPanel (2)"]

# def extract_ar_id(filename_stem):
#     m = re.match(r'^(ar_[^_]+)', filename_stem, re.IGNORECASE)
#     return m.group(1) if m else filename_stem

# def _parse_start(r):
#     # try numeric unix first, then ISO
#     val = r.get("start_unix") or ""
#     if val:
#         try:
#             return float(val)
#         except Exception:
#             pass
#     iso = r.get("start_iso") or ""
#     if iso:
#         try:
#             # Python's fromisoformat supports the format in your CSV
#             dt = datetime.fromisoformat(iso)
#             return dt.timestamp()
#         except Exception:
#             pass
#     return None

# def analyze_file(path):
#     counts = {p: 0 for p in PANEL_NAMES}
#     durations = {p: 0.0 for p in PANEL_NAMES}
#     rows = 0
#     seen_events = []  # list of (start_time, panel_name)
#     with path.open(newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         for r in reader:
#             rows += 1
#             name = (r.get("panel_name") or "").strip()
#             try:
#                 dur = float(r.get("duration_sec") or 0)
#             except Exception:
#                 try:
#                     start = float(r.get("start_unix") or 0)
#                     end = float(r.get("end_unix") or 0)
#                     dur = max(0.0, end - start)
#                 except Exception:
#                     dur = 0.0
#             if name in PANEL_NAMES:
#                 counts[name] += 1
#                 durations[name] += dur
#                 start_ts = _parse_start(r)
#                 if start_ts is not None:
#                     seen_events.append((start_ts, name))
#     # determine first/second/third unique seen by earliest start
#     first, second, third = "NA", "NA", "NA"
#     if seen_events:
#         seen_events.sort(key=lambda x: x[0])
#         unique_order = []
#         for _, pname in seen_events:
#             if pname not in unique_order:
#                 unique_order.append(pname)
#             if len(unique_order) >= 3:
#                 break
#         if len(unique_order) > 0:
#             first = unique_order[0]
#         if len(unique_order) > 1:
#             second = unique_order[1]
#         if len(unique_order) > 2:
#             third = unique_order[2]
#     return {
#         "file": str(path),
#         "rows": rows,
#         "counts": counts,
#         "durations": durations,
#         "ar_id": extract_ar_id(path.stem),
#         "first_seen": first,
#         "second_seen": second,
#         "third_seen": third
#     }

# def main(dirpath, outcsv):
#     base = Path(dirpath)
#     files = sorted(base.rglob("*.csv"))
#     fieldnames = [
#         "file", "ar_id", "rows",
#         "AdPanel_exist", "AdPanel_count", "AdPanel_total_duration_sec",
#         "AdPanel (1)_exist", "AdPanel (1)_count", "AdPanel (1)_total_duration_sec",
#         "AdPanel (2)_exist", "AdPanel (2)_count", "AdPanel (2)_total_duration_sec",
#         "first_seen", "second_seen", "third_seen"
#     ]
#     totals_counts = {p:0 for p in PANEL_NAMES}
#     totals_durs = {p:0.0 for p in PANEL_NAMES}
#     with open(outcsv, "w", newline='', encoding='utf-8') as out:
#         writer = csv.DictWriter(out, fieldnames=fieldnames)
#         writer.writeheader()
#         for f in files:
#             res = analyze_file(f)
#             row = {
#                 "file": res["file"],
#                 "ar_id": res["ar_id"],
#                 "rows": res["rows"],
#                 "AdPanel_exist": "Yes" if res["counts"]["AdPanel"] > 0 else "No",
#                 "AdPanel_count": res["counts"]["AdPanel"],
#                 "AdPanel_total_duration_sec": round(res["durations"]["AdPanel"], 6),
#                 "AdPanel (1)_exist": "Yes" if res["counts"]["AdPanel (1)"] > 0 else "No",
#                 "AdPanel (1)_count": res["counts"]["AdPanel (1)"],
#                 "AdPanel (1)_total_duration_sec": round(res["durations"]["AdPanel (1)"], 6),
#                 "AdPanel (2)_exist": "Yes" if res["counts"]["AdPanel (2)"] > 0 else "No",
#                 "AdPanel (2)_count": res["counts"]["AdPanel (2)"],
#                 "AdPanel (2)_total_duration_sec": round(res["durations"]["AdPanel (2)"], 6),
#                 "first_seen": res["first_seen"],
#                 "second_seen": res["second_seen"],
#                 "third_seen": res["third_seen"]
#             }
#             writer.writerow(row)
#             for p in PANEL_NAMES:
#                 totals_counts[p] += res["counts"][p]
#                 totals_durs[p] += res["durations"][p]
#         totals_row = {
#             "file": "TOTAL",
#             "ar_id": "",
#             "rows": "",
#             "AdPanel_exist": "Yes" if totals_counts["AdPanel"] > 0 else "No",
#             "AdPanel_count": totals_counts["AdPanel"],
#             "AdPanel_total_duration_sec": round(totals_durs["AdPanel"], 6),
#             "AdPanel (1)_exist": "Yes" if totals_counts["AdPanel (1)"] > 0 else "No",
#             "AdPanel (1)_count": totals_counts["AdPanel (1)"],
#             "AdPanel (1)_total_duration_sec": round(totals_durs["AdPanel (1)"], 6),
#             "AdPanel (2)_exist": "Yes" if totals_counts["AdPanel (2)"] > 0 else "No",
#             "AdPanel (2)_count": totals_counts["AdPanel (2)"],
#             "AdPanel (2)_total_duration_sec": round(totals_durs["AdPanel (2)"], 6),
#             "first_seen": "NA",
#             "second_seen": "NA",
#             "third_seen": "NA"
#         }
#         writer.writerow(totals_row)
#     print(f"Wrote summary to {outcsv} ({len(files)} CSV files scanned)")

# if __name__ == "__main__":
#     ap = argparse.ArgumentParser(description="Summarize AdPanel occurrences in CSV gaze logs and include ar_xxx id per row.")
#     ap.add_argument("--dir", "-d", default=".", help="Directory to scan (default: current).")
#     ap.add_argument("--out", "-o", default="ar_adpanel_summary.csv", help="Output CSV path.")
#     args = ap.parse_args()
#     main(args.dir, args.out)




import csv
import re
from pathlib import Path
import argparse
from datetime import datetime

PANEL_NAMES = ["AdPanel", "AdPanel (1)", "AdPanel (2)"]
NAME_TO_LABEL = {"AdPanel": "AD1", "AdPanel (1)": "AD2", "AdPanel (2)": "AD3"}

def extract_ar_id(filename_stem):
    m = re.match(r'^(ar_[^_]+)', filename_stem, re.IGNORECASE)
    return m.group(1) if m else filename_stem

def _parse_start(r):
    val = r.get("start_unix") or ""
    if val:
        try:
            return float(val)
        except Exception:
            pass
    iso = r.get("start_iso") or ""
    if iso:
        try:
            dt = datetime.fromisoformat(iso)
            return dt.timestamp()
        except Exception:
            pass
    return None

def _map_seen_label(name):
    if name is None:
        return "NA"
    if name == "NA":
        return "NA"
    return NAME_TO_LABEL.get(name, name)

def analyze_file(path):
    counts = {p: 0 for p in PANEL_NAMES}
    durations = {p: 0.0 for p in PANEL_NAMES}
    rows = 0
    seen_events = []  # list of (start_time, panel_name)
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows += 1
            name = (r.get("panel_name") or "").strip()
            try:
                dur = float(r.get("duration_sec") or 0)
            except Exception:
                try:
                    start = float(r.get("start_unix") or 0)
                    end = float(r.get("end_unix") or 0)
                    dur = max(0.0, end - start)
                except Exception:
                    dur = 0.0
            if name in PANEL_NAMES:
                counts[name] += 1
                durations[name] += dur
                start_ts = _parse_start(r)
                if start_ts is not None:
                    seen_events.append((start_ts, name))
    first, second, third = "NA", "NA", "NA"
    if seen_events:
        seen_events.sort(key=lambda x: x[0])
        unique_order = []
        for _, pname in seen_events:
            if pname not in unique_order:
                unique_order.append(pname)
            if len(unique_order) >= 3:
                break
        if len(unique_order) > 0:
            first = unique_order[0]
        if len(unique_order) > 1:
            second = unique_order[1]
        if len(unique_order) > 2:
            third = unique_order[2]
    return {
        "file": str(path),
        "rows": rows,
        "counts": counts,
        "durations": durations,
        "ar_id": extract_ar_id(path.stem),
        "first_seen": first,
        "second_seen": second,
        "third_seen": third
    }

def main(dirpath, outcsv):
    base = Path(dirpath)
    files = sorted(base.rglob("*.csv"))
    fieldnames = [
        "file", "ar_id", "rows",
        "AdPanel_exist", "AdPanel_count", "AdPanel_total_duration_sec",
        "AdPanel (1)_exist", "AdPanel (1)_count", "AdPanel (1)_total_duration_sec",
        "AdPanel (2)_exist", "AdPanel (2)_count", "AdPanel (2)_total_duration_sec",
        "first_seen", "second_seen", "third_seen"
    ]
    totals_counts = {p:0 for p in PANEL_NAMES}
    totals_durs = {p:0.0 for p in PANEL_NAMES}
    with open(outcsv, "w", newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        for f in files:
            res = analyze_file(f)
            row = {
                "file": res["file"],
                "ar_id": res["ar_id"],
                "rows": res["rows"],
                "AdPanel_exist": "Yes" if res["counts"]["AdPanel"] > 0 else "No",
                "AdPanel_count": res["counts"]["AdPanel"],
                "AdPanel_total_duration_sec": round(res["durations"]["AdPanel"], 6),
                "AdPanel (1)_exist": "Yes" if res["counts"]["AdPanel (1)"] > 0 else "No",
                "AdPanel (1)_count": res["counts"]["AdPanel (1)"],
                "AdPanel (1)_total_duration_sec": round(res["durations"]["AdPanel (1)"], 6),
                "AdPanel (2)_exist": "Yes" if res["counts"]["AdPanel (2)"] > 0 else "No",
                "AdPanel (2)_count": res["counts"]["AdPanel (2)"],
                "AdPanel (2)_total_duration_sec": round(res["durations"]["AdPanel (2)"], 6),
                "first_seen": _map_seen_label(res["first_seen"]),
                "second_seen": _map_seen_label(res["second_seen"]),
                "third_seen": _map_seen_label(res["third_seen"])
            }
            writer.writerow(row)
            for p in PANEL_NAMES:
                totals_counts[p] += res["counts"][p]
                totals_durs[p] += res["durations"][p]
        totals_row = {
            "file": "TOTAL",
            "ar_id": "",
            "rows": "",
            "AdPanel_exist": "Yes" if totals_counts["AdPanel"] > 0 else "No",
            "AdPanel_count": totals_counts["AdPanel"],
            "AdPanel_total_duration_sec": round(totals_durs["AdPanel"], 6),
            "AdPanel (1)_exist": "Yes" if totals_counts["AdPanel (1)"] > 0 else "No",
            "AdPanel (1)_count": totals_counts["AdPanel (1)"],
            "AdPanel (1)_total_duration_sec": round(totals_durs["AdPanel (1)"], 6),
            "AdPanel (2)_exist": "Yes" if totals_counts["AdPanel (2)"] > 0 else "No",
            "AdPanel (2)_count": totals_counts["AdPanel (2)"],
            "AdPanel (2)_total_duration_sec": round(totals_durs["AdPanel (2)"], 6),
            "first_seen": "NA",
            "second_seen": "NA",
            "third_seen": "NA"
        }
        writer.writerow(totals_row)
    print(f"Wrote summary to {outcsv} ({len(files)} CSV files scanned)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Summarize AdPanel occurrences in CSV gaze logs and include ar_xxx id per row.")
    ap.add_argument("--dir", "-d", default=".", help="Directory to scan (default: current).")
    ap.add_argument("--out", "-o", default="ar_adpanel_summary.csv", help="Output CSV path.")
    args = ap.parse_args()
    main(args.dir, args.out)
