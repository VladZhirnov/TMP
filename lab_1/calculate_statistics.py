
import statistics


def total_time(builds):
    all_times = (b.time_taken_in_seconds() for b in builds)
    seconds = sum(all_times)
    return seconds


def total_build_count(builds):
    return len(builds)


def median_time(builds):
    all_times = [b.time_taken_in_seconds() for b in builds]
    if not all_times:
        return None
    median_time = statistics.median(all_times)
    return median_time


def pretty_print_timedelta(seconds):
    if not seconds:
        return ""
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    milliseconds = round((seconds % 1) * 1000)
    if days > 0:
        return '%d d %d h %d m %d s %d ms' % (days, hours, minutes, seconds,
                                              milliseconds)
    elif hours > 0:
        return '%d h %d m %d s %d ms' % (hours, minutes, seconds, milliseconds)
    elif minutes > 0:
        return '%d m %d s %d ms' % (minutes, seconds, milliseconds)
    elif seconds >= 1:
        return '%d s %d ms' % (seconds, milliseconds)
    else:
        return '%d ms' % (milliseconds)


def summary_statistics(builds):
    builds_excluding_clean = [
        b for b in builds if not b.is_a_clean() and not b.is_a_sync()
    ]
    syncs = [b for b in builds if b.is_a_sync()]
    summary = (
        f"\nBuilds (excluding 'clean')\n"
        f"----------------------------------\n"
        f"Total number: {total_build_count(builds_excluding_clean)}\n"
        f"Total time: {pretty_print_timedelta(total_time(builds_excluding_clean))}\n"
        f"Median time: {pretty_print_timedelta(median_time(builds_excluding_clean))}\n"
        f"\nSyncs\n------\n"
        f"Total number: {total_build_count(syncs)}\n"
        f"Total time: {pretty_print_timedelta(total_time(syncs))}\n"
        f"Median time: {pretty_print_timedelta(median_time(syncs))}\n"
        f"\nAll builds and syncs\n--------------------\n"
        f"Total number: {total_build_count(builds)}\n"
        f"Total time: {pretty_print_timedelta(total_time(builds))}\n"
        f"Median time: {pretty_print_timedelta(median_time(builds))}\n"
    )
    return summary


def remove_clean_builds(builds):
    return (b for b in builds if b.is_a_clean_or_sync())
