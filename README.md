# Python3 script to measure and log Raspberry Pi 5 telemetry

To use, put on RPI and use: sudo python3 <filename>. Logging to .csv will start immediately and file is stored in same folder as the script.

Current version supports:

- vcgencmd measure_clock {arm,core,h264,isp,v3d,uart,pwm,emmc,pixel,vec,hdmi,dpi}
- vcgencmd measure_temp {arm}
- vcgencmd measure_volts {core,sdram_c,sdram_i,sdram_p}
- vcgencmd get_throttled
- vcgencmd pmic_read_adc
- vcgencmd readmr
- psutil.cpu_percent

Telemetry is formatted so it's more easily readible when monitoring. The csv data is formatted so it's immediately usable in Excel.

Might add more telemetry in the future.
