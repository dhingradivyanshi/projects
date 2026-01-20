from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from threading import Lock
from queue import Queue
from typing import Dict, Optional
import uuid

# Enums
class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"

class SlotType(Enum):
    COMPACT = "COMPACT"
    BIKE = "BIKE"

# Vehicle
class Vehicle:
    def __init__(self, number: str, vehicle_type: VehicleType):
        self.number = number
        self.type = vehicle_type

# Parking Slot
class ParkingSlot:
    def __init__(self, slot_id: str, slot_type: SlotType):
        self.slot_id = slot_id
        self.type = slot_type
        self.is_occupied = False
        self.vehicle: Optional[Vehicle] = None
        self.lock = Lock()

    def park(self, vehicle: Vehicle):
        with self.lock:
            self.is_occupied = True
            self.vehicle = vehicle

    def unpark(self):
        with self.lock:
            self.is_occupied = False
            self.vehicle = None

# Parking Strategy
class ParkingStrategy(ABC):
    @abstractmethod
    def find_slot(self, available_slots: Dict[SlotType, Queue], vehicle: Vehicle) -> Optional[ParkingSlot]:
        pass

class NearestSlotStrategy(ParkingStrategy):
    def find_slot(self, available_slots: Dict[SlotType, Queue], vehicle: Vehicle) -> Optional[ParkingSlot]:
        slot_type = SlotType.COMPACT if vehicle.type == VehicleType.CAR else SlotType.BIKE
        queue = available_slots.get(slot_type)
        if queue and not queue.empty():
            return queue.get()
        return None

# Pricing Strategy
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        pass

class HourlyPricing(PricingStrategy):
    def calculate_fee(self, entry_time: datetime, exit_time: datetime) -> float:
        duration = (exit_time - entry_time).seconds
        hours = duration // 3600 + 1  # ceil to next hour
        return hours * 20

# Ticket
class Ticket:
    def __init__(self, ticket_id: str, vehicle: Vehicle, slot: ParkingSlot, entry_time: datetime, pricing_strategy: PricingStrategy):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.slot = slot
        self.entry_time = entry_time
        self.exit_time: Optional[datetime] = None
        self.pricing_strategy = pricing_strategy

    def close_ticket(self, exit_time: datetime) -> float:
        self.exit_time = exit_time
        return self.pricing_strategy.calculate_fee(self.entry_time, self.exit_time)

# Level
class Level:
    def __init__(self, level_id: int, slot_counts: Dict[SlotType, int]):
        self.level_id = level_id
        self.available_slots: Dict[SlotType, Queue] = {slot_type: Queue() for slot_type in slot_counts}
        self.all_slots: Dict[str, ParkingSlot] = {}
        for slot_type, count in slot_counts.items():
            for i in range(count):
                slot_id = f"L{level_id}-{slot_type.name[:1]}{i}"
                slot = ParkingSlot(slot_id, slot_type)
                self.available_slots[slot_type].put(slot)
                self.all_slots[slot_id] = slot

# Parking Lot
class ParkingLot:
    def __init__(self, parking_strategy: ParkingStrategy, pricing_strategy: PricingStrategy):
        self.levels: Dict[int, Level] = {}
        self.parking_strategy = parking_strategy
        self.pricing_strategy = pricing_strategy
        self.active_tickets: Dict[str, Ticket] = {}
        self.lock = Lock()

    def add_level(self, level_id: int, slot_counts: Dict[SlotType, int]):
        self.levels[level_id] = Level(level_id, slot_counts)

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        with self.lock:
            for level in self.levels.values():
                slot = self.parking_strategy.find_slot(level.available_slots, vehicle)
                if slot:
                    slot.park(vehicle)
                    ticket_id = str(uuid.uuid4())
                    ticket = Ticket(ticket_id, vehicle, slot, datetime.now(), self.pricing_strategy)
                    self.active_tickets[vehicle.number] = ticket
                    print(f"[INFO] Parked at {slot.slot_id}, Ticket: {ticket_id}")
                    return ticket
        print("[WARN] No slot available")
        return None

    def unpark_vehicle(self, vehicle_number: str) -> Optional[float]:
        with self.lock:
            ticket = self.active_tickets.get(vehicle_number)
            if not ticket:
                print("[ERROR] No active ticket found")
                return None
            slot = ticket.slot
            slot.unpark()
            fee = ticket.close_ticket(datetime.now())
            level = self.get_level_for_slot_id(slot.slot_id)
            if level:
                level.available_slots[slot.type].put(slot)
            del self.active_tickets[vehicle_number]
            print(f"[INFO] Unparked from {slot.slot_id}, Fee: {fee}")
            return fee

    def get_level_for_slot_id(self, slot_id: str) -> Optional[Level]:
        for level in self.levels.values():
            if slot_id in level.all_slots:
                return level
        return None

# Example Usage
if __name__ == "__main__":
    lot = ParkingLot(parking_strategy=NearestSlotStrategy(), pricing_strategy=HourlyPricing())
    lot.add_level(1, {
        SlotType.COMPACT: 2,
        SlotType.BIKE: 2
    })

    car1 = Vehicle("KA-01", VehicleType.CAR)
    bike1 = Vehicle("KA-02", VehicleType.BIKE)

    ticket1 = lot.park_vehicle(car1)
    ticket2 = lot.park_vehicle(bike1)

    import time; time.sleep(1)  # simulate time

    lot.unpark_vehicle("KA-01")
    lot.unpark_vehicle("KA-02")
