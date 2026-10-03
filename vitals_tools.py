"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic readings stored in encounter records."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings

def mean_systolic(readings):
    """Return mean systolic"""
    if len(readings) == 0:
        return None
    return sum(readings) / len(readings)

def count_patients(encounters):
    """Counting the patients"""

    ids = []

    for encounter in encounters:
        ids.append(encounter["patient_id"])

    unique = set(ids)

    return unique

def patients_at_or_above(encounters, cutoff):
    """Check if patient systolic reading is at or above cutoff"""

    patients = []
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patients.append(encounter["patient_id"])

    return patients
