from parking_system.models import VehicleType
from parking_system.services import ParkingService
from parking_system.utils import format_record, format_slot, format_vehicle


def print_menu() -> None:
    print("\n========== Parking Lot Management ==========")
    print("1. Park Vehicle")
    print("2. Exit Vehicle")
    print("3. Display Parked Vehicles")
    print("4. Display Available Slots")
    print("5. Display Parking History")
    print("6. Display Dashboard")
    print("7. Exit")


def choose_vehicle_type() -> VehicleType | None:
    print("\nVehicle Type")
    print("1. Bike")
    print("2. Car")
    print("3. Truck")

    choice = input("Choice: ").strip()

    mapping = {
        "1": VehicleType.BIKE,
        "2": VehicleType.CAR,
        "3": VehicleType.TRUCK,
    }

    return mapping.get(choice)


def park_vehicle(service: ParkingService) -> None:
    number = input("Vehicle Number: ").strip()
    vehicle_type = choose_vehicle_type()

    if vehicle_type is None:
        print("Invalid vehicle type.")
        return

    success, message, slot_id = service.park_vehicle(number, vehicle_type)
    print(message)

    if success:
        print(f"Assigned Slot: {slot_id}")


def exit_vehicle(service: ParkingService) -> None:
    number = input("Vehicle Number: ").strip()

    success, message, fee = service.exit_vehicle(number)
    print(message)

    if success:
        print(f"Parking Fee: Rs {fee:.2f}")


def display_parked_vehicles(service: ParkingService) -> None:
    vehicles = service.get_active_vehicles()

    if not vehicles:
        print("No vehicles parked.")
        return

    print("\n------ Parked Vehicles ------")

    for vehicle, slot_id in vehicles:
        print(format_vehicle(vehicle, slot_id))


def display_available_slots(service: ParkingService) -> None:
    slots = service.get_available_slots()

    print("\n------ Available Slots ------")

    if not slots:
        print("Parking lot is full.")
        return

    for slot in slots:
        print(format_slot(slot))


def display_history(service: ParkingService) -> None:
    history = service.get_parking_history()

    if not history:
        print("No completed parking records.")
        return

    print("\n------ Parking History ------")

    for record in history:
        print(format_record(record))


def display_dashboard(service: ParkingService) -> None:
    print("\n------ Parking Dashboard ------")
    print(f"Total Slots     : {service.get_total_slots()}")
    print(f"Occupied Slots  : {service.get_occupied_count()}")
    print(f"Available Slots : {service.get_available_count()}")
    print(f"Occupancy Rate  : {service.get_occupancy_rate():.2f}%")
    print(f"Total Revenue   : Rs {service.get_total_revenue():.2f}")


def main() -> None:
    service = ParkingService()

    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            park_vehicle(service)
        elif choice == "2":
            exit_vehicle(service)
        elif choice == "3":
            display_parked_vehicles(service)
        elif choice == "4":
            display_available_slots(service)
        elif choice == "5":
            display_history(service)
        elif choice == "6":
            display_dashboard(service)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
