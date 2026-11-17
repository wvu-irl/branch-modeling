#!/usr/bin/env python3
import argparse
import csv
import pathlib
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def load_trace(csv_path):
    times = []
    elastic = []
    kinetic = []
    px = []
    py = []
    pz = []

    if not csv_path.exists():
        return times, elastic, kinetic, px, py, pz

    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                times.append(float(row["time"]))
                elastic.append(float(row["elastic_energy"]))
                kinetic.append(float(row["kinetic_energy"]))
                px.append(float(row["endpoint_x"]))
                py.append(float(row["endpoint_y"]))
                pz.append(float(row["endpoint_z"]))
            except (KeyError, ValueError):
                # Skip malformed rows.
                continue

    return times, elastic, kinetic, px, py, pz


def draw_plot(ax_energy, ax_pos, times, elastic, kinetic, px, py, pz):
    ax_energy.clear()
    ax_pos.clear()

    if times:
        ax_energy.plot(times, elastic, label="Elastic (Eel)", linewidth=1.5)
        ax_energy.plot(times, kinetic, label="Kinetic (Ek)", linewidth=1.0, alpha=0.8)
        ax_pos.plot(times, px, label="x", linewidth=1.2)
        ax_pos.plot(times, py, label="y", linewidth=1.2)
        ax_pos.plot(times, pz, label="z", linewidth=1.2)

    ax_energy.set_title("Deformation Energy")
    ax_energy.set_ylabel("Energy")
    ax_energy.grid(True, alpha=0.25)
    ax_energy.legend(loc="best")

    ax_pos.set_title("Endpoint Position")
    ax_pos.set_xlabel("Time [s]")
    ax_pos.set_ylabel("Position")
    ax_pos.grid(True, alpha=0.25)
    ax_pos.legend(loc="best")


def main():
    parser = argparse.ArgumentParser(description="Plot deformation energy and endpoint position trace.")
    parser.add_argument(
        "csv",
        nargs="?",
        default="stiff_trace.csv",
        help="Path to trace CSV (default: stiff_trace.csv)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Live-refresh the plot while simulation is writing the CSV.",
    )
    parser.add_argument(
        "--interval-ms",
        type=int,
        default=400,
        help="Refresh interval for --live mode in milliseconds (default: 400).",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output image path (e.g. trace.png). If set without --live, saves and exits.",
    )

    args = parser.parse_args()
    csv_path = pathlib.Path(args.csv)

    fig, (ax_energy, ax_pos) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.tight_layout()

    if args.live:
        def _update(_):
            times, elastic, kinetic, px, py, pz = load_trace(csv_path)
            draw_plot(ax_energy, ax_pos, times, elastic, kinetic, px, py, pz)

        _update(0)
        FuncAnimation(fig, _update, interval=max(args.interval_ms, 50), cache_frame_data=False)
        plt.show()
        return 0

    times, elastic, kinetic, px, py, pz = load_trace(csv_path)
    if not times:
        print(f"No data found in {csv_path}. Run the simulator first.", file=sys.stderr)
        return 1

    draw_plot(ax_energy, ax_pos, times, elastic, kinetic, px, py, pz)

    if args.save:
        fig.savefig(args.save, dpi=150)
        print(f"Saved plot to {args.save}")
        return 0

    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

