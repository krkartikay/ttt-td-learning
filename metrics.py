import json

# Configuration Constants
LOG_INTERVAL = 1  # Log metrics every 1,000 ticks
EXPORT_INTERVAL = 10000  # Export metrics every 10,000 ticks

metrics = {}
logical_time = 0  # Initialize logical clock
counters = {}  # Track counters separately to handle increments on every tick


def tick():
    """
    Advances the logical clock by 1 unit.
    If the logical time is a multiple of EXPORT_INTERVAL, export metrics.
    """
    global logical_time
    logical_time += 1
    if logical_time % EXPORT_INTERVAL == 0:
        export_metrics()


def log_metric(name, value, slice=""):
    """
    Logs a metric with the given name and value, using the logical timestamp,
    only if the logical time is a multiple of LOG_INTERVAL.
    """
    if logical_time % LOG_INTERVAL != 0:
        return  # Only log data at intervals defined by LOG_INTERVAL

    slice = str(slice)
    if name not in metrics:
        metrics[name] = []
    metrics[name].append((logical_time, value, slice))
    print("Log: ", name, value, slice)


def increment_metric(name, slice=""):
    """
    Increments a counter metric by 1 at the current logical time,
    and logs it only if the logical time is a multiple of LOG_INTERVAL.
    """
    slice = str(slice)
    if name not in counters:
        counters[name] = {}  # Track counts by slice within the counters dictionary
    if slice not in counters[name]:
        counters[name][slice] = 0

    # Increment the counter
    counters[name][slice] += 1

    # Log only at intervals defined by LOG_INTERVAL
    if logical_time % LOG_INTERVAL == 0:
        if name not in metrics:
            metrics[name] = []
        metrics[name].append((logical_time, counters[name][slice], slice))
        print("Log: ", name, counters[name][slice], slice)


def export_metrics():
    """
    Exports all the logged metrics to a JSON file.
    """
    with open("metrics.json", "w") as f:
        json.dump(metrics, f)
    print(f"Exported metrics at logical time {logical_time}")
