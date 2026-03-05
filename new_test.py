import asyncio
#import logging
import sys

# Force the local files, not pip installed lib
sys.path.insert(0, r'custom_components\goodwe')
import goodwe

async def get_runtime_data():

    inverter = await goodwe.connect('192.168.0.23', 502)
    runtime_data = await inverter.read_runtime_data()

    for sensor in inverter.sensors():
        if sensor.id_ in runtime_data:
            print(f"{sensor.id_}: \t\t {sensor.name} = {runtime_data[sensor.id_]} {sensor.unit}")
    
    print("\n\n Settings: \n\n")
    settings_data = await inverter.read_settings_data()
    for settings in inverter.settings():
        if settings.id_ in settings_data:
            print(f"{settings.id_}: \t\t {settings.name} = {settings_data[settings.id_]} {settings.unit}") 


    '''
    # Clear eco modes 2-4
    for slot in ["eco_mode_2", "eco_mode_3", "eco_mode_4"]:
        setting = inverter._settings.get(slot)
        if setting:
            off_bytes = setting.encode_off()
            print(f"Writing {slot}: {off_bytes.hex()}")
            await inverter.write_setting(slot, off_bytes)
            print(f"  {slot} cleared OK")
        else:
            print(f"  {slot} not found in settings")
    '''

    '''
    # Read raw registers 35103-35120 (PV1-PV4 voltage/current/power + PV mode)
    print("\n\n Raw registers: \n\n")
    response = await inverter._read_from_socket(inverter._read_command(35103, 18))
    raw = response.response_data()

    for i in range(18):
        reg = 35103 + i
        val_u16 = int.from_bytes(raw[i*2:i*2+2], 'big', signed=False)
        val_s16 = int.from_bytes(raw[i*2:i*2+2], 'big', signed=True)
        print(f"  {reg}: raw={raw[i*2:i*2+2].hex()}  u16={val_u16}  s16={val_s16}  (÷10={val_u16/10})")            

    print("\n\n Raw registers 2: \n\n")
    response = await inverter._read_from_socket(inverter._read_command(35337, 4))
    raw = response.response_data()
    for i in range(4):
        reg = 35337 + i
        val_u16 = int.from_bytes(raw[i*2:i*2+2], 'big', signed=False)
        print(f"  {reg}: raw={raw[i*2:i*2+2].hex()}  u16={val_u16}")
    '''

asyncio.run(get_runtime_data())