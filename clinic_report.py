#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """A usable encounter splits into three fields, where the third field is an integer and range from 60 to 250 mmHg"""
    
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        rows = file.readlines()

    encounters = []
    skipped = 0

    for row in rows[1:]:
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue
        fields = row.strip().split(",")
        if len(fields) != 3:
            print(f"Skipping a row with {len(fields)} fields: {row.strip()}")
            skipped += 1
            continue
        patient_id, visit_date, raw_systolic = fields
        try:
            systolic = int(raw_systolic)
        except ValueError as error:
            print(f"Skipping {patient_id}: {error}")
            skipped += 1
        else:
            if systolic < 60 or systolic > 250: 
                print(f"Skipping {patient_id}: invalid systolic")
                skipped += 1
                continue
            encounters.append({"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic})
    
    return encounters, skipped

def main():
    """This writes the patient report"""
    encounters, skipped = read_encounters(DATA_PATH)

    usable_enc = len(encounters)
    unique_id = len(count_patients(encounters))
    readings = systolic_readings(encounters)
    mean_sys = mean_systolic(readings)
    high_sys = max(readings)
    low_sys = min(readings)

    output_path = f"{OUTPUT_DIR}/vitals_report.txt"
    with open(output_path, "w", encoding="utf-8") as report_file:
        report_file.write(f"Usable encounters: {usable_enc}\n")
        report_file.write(f"Skipped rows: {skipped}\n")
        report_file.write(f"Patients seen: {unique_id}\n")
        report_file.write(f"Mean systolic: {mean_sys} mmHg\n")
        report_file.write(f"Highest systolic: {high_sys} mmHg\n")
        report_file.write(f"Lowest systolic: {low_sys} mmHg\n")

    with open(output_path, "r", encoding="utf-8") as report_file:
        rows = report_file.readlines()
        for row in rows:
            print(row)

    cutoff = int(input("Cutoff (mmHg): "))
    follow_up = patients_at_or_above(encounters, cutoff)

    follow_up_path = f"{OUTPUT_DIR}/followup_list.txt"
    with open(follow_up_path, "w", encoding="utf-8") as report_file:
        report_file.write(f"Cutoff: {cutoff}\n")
        report_file.write(f"Reason: patients needs followup\n")
        for patient_id in follow_up:
            report_file.write(f"{patient_id}\n")

if __name__ == "__main__":
    main()
