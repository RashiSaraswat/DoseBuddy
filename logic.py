def check_conflicts(name, time, food):
    warnings = []

    # Check spacing: Example rule (you can expand)
    hour = int(time.split(":")[0])

    if hour < 7:
        warnings.append("This medicine is scheduled too early. Consider after 7 AM.")

    if food == "before" and hour > 20:
        warnings.append("Before-food medicine shouldn't be taken late at night.")

    if food == "after" and hour < 7:
        warnings.append("After-food medicine shouldn’t be taken early morning.")

    if warnings:
        return warnings
    return ["No conflicts detected ✔"]
