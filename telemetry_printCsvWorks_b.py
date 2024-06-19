import csv
import os
import psutil
import subprocess
import time

def get_vcgencmd_output(command):
    result = subprocess.check_output(command, shell=True)
    return result.decode().strip()

def get_cpu_usage():
    # Retrieve and return the CPU usage percentage per core
    return psutil.cpu_percent(interval=1, percpu=True)

def decode_throttling(throttle_hex_value):

    error_messages = {
      0: "UV",
      1: "ArmFreqCap",
      2: "CurThrottle",
      3: "SoftTempLimit",
      16: "UV_occured",
      17: "ArmFreqCap_occured",
      18: "Throttle_occured",
      19: "SoftTempLimit_occured",
    }
    try:
        # Convert hex value to binary string (remove leading '0b')
        binary_value = bin(int(throttle_hex_value, 16))[2:]
    except ValueError:
        return [("Invalid hex value", "N/A")]

    # Invert binary string (active bits are 1s)
    binary_value = binary_value[::-1]

    # Pad binary string with leading zeros to ensure consistent length
    binary_value = binary_value.zfill(20)

    # Initialize empty list for results
    results = []
    for i, message in error_messages.items():
        # Check if index is within binary string length (avoid out-of-range access)
        if i < len(binary_value):
            result = (message, "Yes" if binary_value[i] == "1" else "No")
        else:
            result = (message, "No (bit out of range)")  # Indicate missing bit
        results.append(result)

    return results

def pmic_read_adc():
    try:
        # Run the command and capture the output
        output = subprocess.check_output(['vcgencmd', 'pmic_read_adc'], stderr=subprocess.STDOUT)
        # Decode byte output to string and split by spaces
        parts = output.decode('utf-8').strip().split()
        # Initialize an empty list to store (label, value) tuples
        result = []
        # Iterate over pairs of label and value
        for i in range(0, len(parts), 2):
            label = parts[i]
            value = parts[i + 1]
            result.append((label, value))
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing vcgencmd: {e}")
        return []

def main():
    filename = "telemetry_data.csv"

    fieldnames = [
        "timestamp",
        "cpu_percent",
        "arm_mhz",
        "core_mhz",
        "h264_mhz",
        "isp_mhz",
        "v3d_mhz",
        "uart_mhz",
        "pwm_mhz",
        "emmc_mhz",
        "pixel_mhz",
        "vec_mhz",
        "hdmi_mhz",
        "dpi_mhz",
        "arm_temp",
        "core_volt",
        "sdram_c_volt",
        "sdram_i_volt",
        "sdram_p_volt",
        "3V7_WL_SW_A",
        "3V3_SYS_A",
        "1V8_SYS_A",
        "DDR_VDD2_A",
        "DDR_VDDQ_A",
        "1V1_SYS_A",
        "0V8_SW_A",
        "VDD_CORE_A",
        "3V3_DAC_A",
        "3V3_ADC_A",
        "0V8_AON_A",
        "HDMI_A",
        "3V7_WL_SW_V",
        "3V3_SYS_V",
        "1V8_SYS_V",
        "DDR_VDD2_V",
        "DDR_VDDQ_V",
        "1V1_SYS_V",
        "0V8_SW_V",
        "VDD_CORE_V",
        "3V3_DAC_V",
        "3V3_ADC_V",
        "0V8_AON_V",
        "HDMI_V",
        "EXT5V_V",
        "BATT_V",
        "throttle_hex",
        "UV",
        "ArmFreqCap",
        "CurThrottle",
        "SoftTempLimit",
        "UV_occured",
        "ArmFreqCap_occured",
        "Throttle_occured",
        "SoftTempLimit_occured",
    ]
    
    if not os.path.exists(filename):
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
    while True:

        ### GET ALL DATA BEFORE PRINTING ###

        # Get status information
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        fw_version = get_vcgencmd_output("vcgencmd version")

        # Get processor usage information
        cpu_percent = psutil.cpu_percent(interval=1)

        # Get Vcgencmd metrics
        arm_mhz = get_vcgencmd_output("vcgencmd measure_clock arm | sed -e 's/frequency(0)=//'")
        core_mhz = get_vcgencmd_output("vcgencmd measure_clock core | sed -e 's/frequency(0)=//'")
        h264_mhz = get_vcgencmd_output("vcgencmd measure_clock h264 | sed -e 's/frequency(0)=//'")
        isp_mhz = get_vcgencmd_output("vcgencmd measure_clock isp | sed -e 's/frequency(0)=//'")
        v3d_mhz = get_vcgencmd_output("vcgencmd measure_clock v3d | sed -e 's/frequency(0)=//'")
        uart_mhz = get_vcgencmd_output("vcgencmd measure_clock uart | sed -e 's/frequency(0)=//'")
        pwm_mhz = get_vcgencmd_output("vcgencmd measure_clock pwm | sed -e 's/frequency(0)=//'")
        emmc_mhz = get_vcgencmd_output("vcgencmd measure_clock emmc | sed -e 's/frequency(0)=//'")
        pixel_mhz = get_vcgencmd_output("vcgencmd measure_clock pixel | sed -e 's/frequency(0)=//'")
        vec_mhz = get_vcgencmd_output("vcgencmd measure_clock vec | sed -e 's/frequency(0)=//'")
        hdmi_mhz = get_vcgencmd_output("vcgencmd measure_clock hdmi | sed -e 's/frequency(0)=//'")
        dpi_mhz = get_vcgencmd_output("vcgencmd measure_clock dpi | sed -e 's/frequency(0)=//'")
        arm_temp = get_vcgencmd_output("vcgencmd measure_temp | sed -e 's/temp=//; s/C//'")
        core_volt = get_vcgencmd_output("vcgencmd measure_volts core | sed -e 's/volt=//; s/V//'")
        sdram_c_volt = get_vcgencmd_output("vcgencmd measure_volts sdram_c | sed -e 's/volt=//; s/V//'")
        sdram_i_volt = get_vcgencmd_output("vcgencmd measure_volts sdram_i | sed -e 's/volt=//; s/V//'")
        sdram_p_volt = get_vcgencmd_output("vcgencmd measure_volts sdram_p | sed -e 's/volt=//; s/V//'")

        # Check for throttling
        throttle_hex_value = get_vcgencmd_output("vcgencmd get_throttled | sed -e 's/throttled=//'")
        throttling_status = decode_throttling(throttle_hex_value)

        # Measure PMIC telemetry
        adc_values = pmic_read_adc()

        ### CLEAR THE TERMINAL BEFORE PRINTING ###
        os.system("clear")  # Use "cls" for Windows

        ### PRINT ALL THE DATA ###        
        print("## System Info ##")
        print(f"timestamp: \t\t{timestamp}")
        print(f"FW Version: {fw_version}")
        print("")

        print("## Usage ##")
        #cpu_usage = get_cpu_usage()
        #for core, usage in enumerate(cpu_usage):
        #    print(f"Core {core}: {usage:.2f}%")
        print("")

        print("## Frequencies ##")
        print(f"arm: \t\t{arm_mhz[:-6]} MHz")
        print(f"core: \t\t{core_mhz[:-6]} MHz")
        print(f"h264: \t\t{h264_mhz[:-6]} MHz") 
        print(f"isp: \t\t{isp_mhz[:-6]} MHz") 
        print(f"v3d: \t\t{v3d_mhz[:-6]} MHz") 
        print(f"uart: \t\t{uart_mhz[:-6]} MHz") 
        print(f"pwm: \t\t{pwm_mhz[:-6]} MHz") 
        print(f"emmc: \t\t{emmc_mhz[:-6]} MHz") 
        print(f"pixel: \t\t{pixel_mhz[:-6]} MHz")         
        print(f"vec: \t\t{vec_mhz[:-6]} MHz")         
        print(f"hdmi: \t\t{hdmi_mhz[:-6]} MHz")         
        print(f"dpi: \t\t{dpi_mhz[:-6]} MHz")
        print("")

        print("## Temperature ##")
        print(f"arm: \t\t{arm_temp[:-1]}")
        print("") 
            
        print("## Voltages ##")
        print(f"core: \t\t{core_volt}")
        print(f"sdram_c: \t{sdram_c_volt}")
        print(f"sdram_i: \t{sdram_i_volt}")
        print(f"sdram_p: \t{sdram_p_volt}")
        print("")
            
        print("## Throttle Info ##")
        print(f"Throttle Hex: {throttle_hex_value}")
        for message, status in throttling_status:
            print(f"{message}: {status}")
        print("")   
            
        print("## PMIC Telemetry ##")
        for label, value in adc_values:
            value = value.split('=')[-1]
            value = value[:-1]
            print(f"{label}: {value}")

        with open(filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
            
            # Create a dictionary for the row data
            row_data = {
                "timestamp": timestamp,
                "cpu_percent": cpu_percent,
                "arm_mhz": arm_mhz,
                "core_mhz": core_mhz,
                "h264_mhz": h264_mhz,
                "isp_mhz": isp_mhz,
                "v3d_mhz": v3d_mhz,
                "uart_mhz": uart_mhz,
                "pwm_mhz": pwm_mhz,
                "emmc_mhz": emmc_mhz,
                "pixel_mhz": pixel_mhz,
                "vec_mhz": vec_mhz,
                "hdmi_mhz": hdmi_mhz,
                "dpi_mhz": dpi_mhz,
                "arm_temp": arm_temp[:-1],
                "core_volt": core_volt,
                "sdram_c_volt": sdram_c_volt,
                "sdram_i_volt": sdram_i_volt,
                "sdram_p_volt": sdram_p_volt,
                "throttle_hex": throttle_hex_value,
                "UV": "No",
                "ArmFreqCap": "No",
                "CurThrottle": "No",
                "SoftTempLimit": "No",
                "UV_occured": "No",
                "ArmFreqCap_occured": "No",
                "Throttle_occured": "No",
                "SoftTempLimit_occured": "No",
            }

            # Add pmic_read_adc() data dynamically to row_data
            for label, value in adc_values:
                row_data[label] = value.split('=')[-1][:-1]

            # Update row_data with decode_throttling() results
            for message, status in throttling_status:
                row_data[message] = status

            writer.writerow(row_data)

            time.sleep(1)  # Wait for 1 second

if __name__ == "__main__":
    main()
