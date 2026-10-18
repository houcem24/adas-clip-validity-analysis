"""Generate synthetic example clips and a synthetic sample dataset.

The real recording annotations used in the thesis are confidential and are not part of this repository.
This script produces stand-in data with the same structure, so the notebook and the web app can be run
and explored. Every identifier, position, timestamp and label combination is randomly generated.

Usage:
    python scripts/make_synthetic_clips.py            # 5 clips in Clips/, 60-row sample CSV
    python scripts/make_synthetic_clips.py --clips 50 --rows 200
"""

import argparse
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Scenario attributes read by the notebook, with example label codes.
SCENARIO_LABELS = {
    "Deviation": ["DEV_1_NO_DEVIATION", "DEV_2_SMALLER_0_5", "DEV_3_FIXED_0_75", "DEV_4_FIXED_1_25"],
    "Maneuver": ["MAN_1_STRAIGHT", "MAN_2_S_SHAPE", "MAN_3_CURVED"],
    "WeatherCondition": ["WEA_1_CLEAR", "WEA_2_CLOUDY", "WEA_3_RAIN", "WEA_4_FOG", "WEA_5_SNOWING"],
    "ParkingGarage": ["GAR_1_GARAGE_CARPORT", "GAR_2_OUTSIDE"],
    "DrivingMode": ["DRVM_1_00_TO_10_KPH", "DRVM_3_20_TO_40_KPH"],
    "ArtificialLight": ["STL_1_STREET_LIGHTS", "STL_2_NO_STREET_LIGHTS"],
    "DynamicObjects": ["DOBJ_1_DOBJ_IN_SCENE", "DOBJ_2_NO_DOBJ_IN_SCENE"],
    "DirectionChange": ["DIR_1_DIRECTION_CHANGE", "DIR_2_FORWARD", "DIR_3_BACKWARDS"],
    "LightCondition": ["LC_1_DAY", "LC_2_NIGHT", "LC_3_TWILIGHT"],
    "ParkingManeuver": ["PIO_1_PARK_IN", "PIO_2_PARK_OUT"],
    "Seasons": ["SEA_1_GREEN_TREES", "SEA_2_LEAVES_ON_GROUND", "SEA_3_TREES_WITHOUT_LEAVES", "SEA_4_SNOW_ON_GROUND"],
    "StaticObjects": ["SOBJ_1_NO_SOBJ_PRESENT", "SOBJ_2_SOBJ_PRESENT"],
    "Location": [f"LOC_{i:02d}" for i in range(1, 11)],
}

FPS = 30
NS_PER_FRAME = 1_000_000_000 // FPS


def position(rng: random.Random, lat: float, lng: float) -> dict:
    """A made-up position near (lat, lng); not a real recording location."""
    return {
        "latitude": round(lat + rng.uniform(-0.002, 0.002), 7),
        "elevation": round(rng.uniform(80, 400), 2),
        "longitude": round(lng + rng.uniform(-0.002, 0.002), 7),
    }


def prelabel(category, label, state, frame, timestamp, pos, kind="multi-select", conditions=None):
    return {
        "category": category,
        "postion_coordinates": pos,  # (sic) key name as in the original annotation format
        "timestamp": timestamp,
        "clipnumber": -1,
        "label": label,
        "clipname_video": "N/A",
        "state": state,
        "conditions": conditions or {},
        "type": kind,
        "frame_number": frame,
    }


def make_clip(rng: random.Random, index: int) -> tuple[str, dict]:
    """Build one synthetic clip annotation in the same layout as the real recordings."""
    labels = {category: rng.choice(options) for category, options in SCENARIO_LABELS.items()}
    lat, lng = rng.uniform(49.0, 51.0), rng.uniform(7.0, 10.0)

    start_frame = rng.randint(10_000, 200_000)
    start_ts = 1_600_000_000_000_000_000 + rng.randint(0, 40_000_000) * 1_000_000_000
    scene_start = start_frame + rng.randint(200, 1_500)
    scene_stop = scene_start + rng.randint(1_500, 4_000)
    end_frame = scene_stop + rng.randint(50, 400)

    def ts(frame):
        return start_ts + (frame - start_frame) * NS_PER_FRAME

    prelabels = []
    for category, label in labels.items():
        prelabels.append(prelabel(category, label, "activated", start_frame, ts(start_frame), position(rng, lat, lng)))
    conditions = {category: [label] for category, label in labels.items()}
    prelabels.append(prelabel("SceneStartStop", "SCN_1_START", "activated", scene_start, ts(scene_start),
                              position(rng, lat, lng), "single", conditions))
    prelabels.append(prelabel("SceneStartStop", "SCN_2_STOP", "deactivated", scene_stop, ts(scene_stop),
                              position(rng, lat, lng), "single", conditions))
    for category, label in labels.items():
        prelabels.append(prelabel(category, label, "deactivated", end_frame, ts(end_frame), position(rng, lat, lng)))

    clip_id = f"W00_SYNTHETIC_{index:03d}"
    metadata = {
        "comment": "SYNTHETIC EXAMPLE - not real recording data",
        "campaign": "EXAMPLE_CAMPAIGN",
        "driver_id": f"DRIVER_{rng.randint(1, 20):03d}",
        "vehicle_id": f"SYNTHETIC-VEHICLE-{rng.randint(1, 5):02d}",
        "vehicle_number_plate": "XX-XX 0000",
        "brand": "OEM",
        "model": "EXAMPLE_MODEL",
        "group_project_name": "EXAMPLE_PROJECT",
        "governance": {"location": "EXAMPLE_SITE", "pool": "example_pool"},
        "logger": "EXAMPLE_LOGGER",
        "meta_data_version": "1.0.0",
        "driving_side": "RIGHT_DRIVING_SIDE",
        "steering_wheel_side": "LEFT_HAND_DRIVE",
        "tire_type": rng.choice(["SUMMER_TIRE", "WINTER_TIRE"]),
    }
    return clip_id, {"metadata": metadata, "prelabels": prelabels}


def sample_row(rng: random.Random, clip_id: str) -> dict:
    """One synthetic row in the layout of the flattened dataset (flask_data_no_encoder.csv)."""
    clip = make_clip(rng, 0)[1]
    row = {"Clip": clip_id}
    for p in clip["prelabels"]:
        if p["category"] in SCENARIO_LABELS and p["state"] == "activated":
            row[p["category"]] = p["label"]
    parts = {
        "VID_START": next(p for p in clip["prelabels"] if p["category"] == "Deviation" and p["state"] == "activated"),
        "SCN_START": next(p for p in clip["prelabels"] if p["label"] == "SCN_1_START"),
        "VID_END": next(p for p in clip["prelabels"] if p["category"] == "Deviation" and p["state"] == "deactivated"),
        "SCN_END": next(p for p in clip["prelabels"] if p["label"] == "SCN_2_STOP"),
    }
    for prefix, p in parts.items():
        row[f"{prefix}_FRAME"] = p["frame_number"]
        row[f"{prefix}_ELV"] = p["postion_coordinates"]["elevation"]
        row[f"{prefix}_LAT"] = p["postion_coordinates"]["latitude"]
        row[f"{prefix}_LNG"] = p["postion_coordinates"]["longitude"]
        row[f"{prefix}_TSTMP"] = p["timestamp"]
    start_ok, end_ok = rng.random() < 0.8, rng.random() < 0.8
    row["VALIDITY_SCN_START"] = "Valid" if start_ok else "Invalid"
    row["VALIDITY_SCN_END"] = "Valid" if end_ok else "Invalid"
    row["CLIP_VALIDITY"] = "Valid" if start_ok and end_ok else "Invalid"
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--clips", type=int, default=5, help="Number of example clip folders to create")
    parser.add_argument("--rows", type=int, default=60, help="Number of rows in the sample dataset")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    for i in range(1, args.clips + 1):
        clip_id, clip = make_clip(rng, i)
        folder = ROOT / "Clips" / clip_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{clip_id}_PRLBL_000000.json").write_text(json.dumps(clip, indent=4) + "\n", encoding="utf-8")

    rows = [sample_row(rng, f"W00_SYNTHETIC_{i:03d}") for i in range(1, args.rows + 1)]
    out = ROOT / "apps" / "authentication" / "flask_data_no_encoder.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.clips} clips to Clips/ and {len(rows)} rows to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
