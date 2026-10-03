import heapq
from dataclasses import dataclass


@dataclass
class Vehicle:
    vehicle_id: str
    urgency: int
    arrival: int
    departure: int
    duration: int


def time_to_minutes(time_string):
    """Convert HH:MM to minutes."""

    hours, minutes = map(int, time_string.split(":"))

    return hours * 60 + minutes


def minutes_to_time(minutes):
    """Convert minutes to HH:MM."""

    hours = minutes // 60
    minutes = minutes % 60

    return f"{hours:02d}:{minutes:02d}"


def calculate_priority(vehicle):
    """
    Higher urgency gets higher priority.
    Earlier departure gets higher priority.
    Shorter duration gets higher priority.
    """

    return (
        vehicle.urgency * 1000000
        - vehicle.departure * 100
        - vehicle.duration
    )


def schedule_vehicles(vehicles, number_of_slots):
    """
    Priority Queue + Greedy + Job Sequencing
    """

    priority_queue = []

    # ------------------------------------------------
    # STEP 1: INSERT VEHICLES INTO PRIORITY QUEUE
    # ------------------------------------------------

    for vehicle in vehicles:

        priority = calculate_priority(vehicle)

        # Python heap is a min-heap,
        # so use negative priority.
        heapq.heappush(
            priority_queue,
            (
                -priority,
                vehicle.departure,
                vehicle.duration,
                vehicle.vehicle_id,
                vehicle
            )
        )

    # ------------------------------------------------
    # STEP 2: INITIALIZE CHARGING SLOTS
    # ------------------------------------------------

    # Each slot stores its next available time.
    slot_available = [0] * number_of_slots

    schedule = []
    execution_log = []

    step = 1

    # ------------------------------------------------
    # STEP 3: PROCESS PRIORITY QUEUE
    # ------------------------------------------------

    while priority_queue:

        (
            negative_priority,
            _,
            _,
            _,
            vehicle
        ) = heapq.heappop(priority_queue)

        priority = -negative_priority

        execution_log.append(
            f"Step {step}: {vehicle.vehicle_id} selected "
            f"from Priority Queue. "
            f"Priority = {priority}"
        )

        step += 1

        best_slot = None
        best_start = None
        best_end = None

        # ------------------------------------------------
        # STEP 4: GREEDY SLOT SELECTION
        # ------------------------------------------------

        for slot in range(number_of_slots):

            start = max(
                vehicle.arrival,
                slot_available[slot]
            )

            end = start + vehicle.duration

            execution_log.append(
                f"Checking Slot {slot + 1}: "
                f"{minutes_to_time(start)} - "
                f"{minutes_to_time(end)}"
            )

            # ------------------------------------------------
            # STEP 5: DEADLINE CHECK
            # ------------------------------------------------

            if end <= vehicle.departure:

                if (
                    best_start is None
                    or start < best_start
                ):
                    best_slot = slot
                    best_start = start
                    best_end = end

        # ------------------------------------------------
        # STEP 6: ASSIGN SLOT
        # ------------------------------------------------

        if best_slot is not None:

            slot_available[best_slot] = best_end

            schedule.append({
                "vehicle_id": vehicle.vehicle_id,
                "slot": best_slot + 1,
                "start": minutes_to_time(best_start),
                "end": minutes_to_time(best_end),
                "departure": minutes_to_time(
                    vehicle.departure
                ),
                "urgency": vehicle.urgency,
                "duration": vehicle.duration,
                "priority": priority,
                "status": "Scheduled"
            })

            execution_log.append(
                f"Greedy Decision: "
                f"{vehicle.vehicle_id} assigned to "
                f"Slot {best_slot + 1} "
                f"from {minutes_to_time(best_start)} "
                f"to {minutes_to_time(best_end)}."
            )

        else:

            schedule.append({
                "vehicle_id": vehicle.vehicle_id,
                "slot": "-",
                "start": "-",
                "end": "-",
                "departure": minutes_to_time(
                    vehicle.departure
                ),
                "urgency": vehicle.urgency,
                "duration": vehicle.duration,
                "priority": priority,
                "status": "Not Scheduled"
            })

            execution_log.append(
                f"Job Sequencing: "
                f"{vehicle.vehicle_id} cannot be scheduled "
                f"before its deadline."
            )

        step += 1

    return schedule, execution_log
if __name__ == "__main__":

    vehicles = [
        Vehicle(
            "EV001",
            5,
            time_to_minutes("08:00"),
            time_to_minutes("10:00"),
            120
        ),

        Vehicle(
            "EV002",
            3,
            time_to_minutes("08:15"),
            time_to_minutes("12:00"),
            60
        ),

        Vehicle(
            "EV003",
            5,
            time_to_minutes("08:30"),
            time_to_minutes("09:30"),
            60
        ),

        Vehicle(
            "EV004",
            2,
            time_to_minutes("09:00"),
            time_to_minutes("13:00"),
            120
        ),

        Vehicle(
            "EV005",
            4,
            time_to_minutes("09:15"),
            time_to_minutes("11:30"),
            60
        ),

        Vehicle(
            "EV006",
            1,
            time_to_minutes("09:30"),
            time_to_minutes("14:00"),
            120
        )
    ]

    schedule, execution_log = schedule_vehicles(
        vehicles,
        number_of_slots=3
    )

    print("\n========== FINAL SCHEDULE ==========\n")

    for item in schedule:

        print(
            f"{item['vehicle_id']} | "
            f"Slot: {item['slot']} | "
            f"{item['start']} - {item['end']} | "
            f"Deadline: {item['departure']} | "
            f"Status: {item['status']}"
        )

    print("\n========== ALGORITHM EXECUTION ==========\n")

    for log in execution_log:
        print(log)