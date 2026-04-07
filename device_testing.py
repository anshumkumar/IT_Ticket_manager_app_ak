from models.devices import Device

device = Device(
    None,
    "Dell Latitude 5420",
    "Laptop",
    1,
    "SN123456",
    "Room 101",
    "2026-04-07"
)

device.add_device()
print("Added:", device)

all_devices = Device.get_all_devices()
print("All devices:", all_devices)

one_device = Device.get_device_by_id(device.device_id)
print("One device:", one_device)

if one_device:
    one_device.location = "Room 202"
    one_device.update_device()
    print("Updated:", Device.get_device_by_id(one_device.device_id))

# Device.delete_device(device.device_id)
# print("Deleted")