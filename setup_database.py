from parking_system.database.schema import (
    create_default_slots,
    create_tables,
)


def main():
    print("Creating database tables...")
    create_tables()

    print("Creating parking slots...")
    create_default_slots()

    print("Database setup complete.")


if __name__ == "__main__":
    main()