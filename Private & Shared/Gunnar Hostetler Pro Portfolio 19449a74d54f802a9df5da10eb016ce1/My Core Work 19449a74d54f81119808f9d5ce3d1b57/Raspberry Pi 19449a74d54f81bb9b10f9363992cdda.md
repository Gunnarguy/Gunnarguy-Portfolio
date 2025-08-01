# Raspberry Pi

Industry: Embedded Systems
Key skills: Linux, Python, SSH

## **PiAutomation - Raspberry Pi Automation, Vision & Monitoring Platform**

### **Overview**

A self-driven embedded systems build centered on Raspberry Pi 4B, combining automation, sensor feedback, and custom wiring for future computer vision, timelapse capture, and hardware introspection. The system is fully wired with display, sensor, and camera integration, and now includes a completed setup for direct SPI flash access - ready for future firmware analysis experiments.

### **Key Features**

- 🔍 **Sensor-driven display:**
    - OLED I2C display wired and fully operational
    - Pulls real-time temperature, humidity, and pressure from BME280 sensor
- 🎥 **Camera and timelapse stack:**
    - 12MP IMX708 autofocus camera (Camera Module 3) set up with Picamera2
    - FFmpeg pipelines tested for image/video capture
- 🧪 **Firmware dumping kit ready to deploy:**
    - SOIC-8 clip, BSS138 level shifter, and SPI wiring mapped and tested
    - All tools installed: flashrom, binwalk, openocd
    - Final wiring verified; next step is attaching to a live board for first firmware dump
- 🖥️ **Touch display and remote access:**
    - Waveshare 4” HDMI touchscreen (480x800) in place
    - Fully headless operation via SSH + RealVNC
    - Access via LAN/WAN (10.0.0.170, 98.33.117.246)

### **Tech Stack**

**Hardware:** Raspberry Pi 4B (4GB RAM), IMX708 camera, BME280 sensor, SSD1306 OLED

**OS:** Debian 12 Bookworm (64-bit)

**Software:** Python, FFmpeg, Picamera2, Flashrom, Binwalk

**Remote Tools:** SSH (key-auth), RealVNC

**Dev Tools:** VS Code (arm64), Git

### **Project Milestones**

| **Area** | **Status** | **Notes** |
| --- | --- | --- |
| OLED sensor display | ✅ Complete | Live temp/humidity/pressure on screen |
| Camera integration | ✅ Operational | Autofocus camera active, basic captures working |
| Timelapse setup | 🟡 In progress | FFmpeg + Picamera2 configured |
| SPI flash dump rig | ✅ Wired + staged | Final pinout saved; ready to clip onto first target |
| Firmware extraction | ❌ Not started | Awaiting real hardware to test against |

### **Intentions & Direction**

This project is a personal sandbox - built to explore how far a Raspberry Pi can go when treated as both a vision node and hardware lab.  I’m not a reverse engineer yet, but I’m setting myself up to try things that used to feel out of reach.  The OLED and sensor readouts were my way of learning I2C and GPIO; the flash-dump rig is my entry point into hardware-level introspection.