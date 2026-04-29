# Pub/Sub Automation Demo

This project is a simple Publisher–Subscriber prototype built using Python standard libraries only.

## Features
- Publisher and Subscriber desktop applications
- TCP socket communication
- Subscribe / Unsubscribe functionality
- Event-driven notifications
- On-demand polling using "Check Status"
- No background polling
- Simple Tkinter UI for demonstration

## Architecture
- Publisher acts as a TCP server
- Subscriber acts as a TCP client
- Communication is implemented using raw Python sockets

## Files
- `publisher.py` → Publisher UI and connection state
- `subscriber.py` → Subscriber UI and event handling
- `socket_server.py` → Socket communication layer
- `main.py` → Launches Publisher and Subscriber together

## How to Run

Run both applications:

```bash
python main.py
```
## Or run separately:
```bash
python publisher.py
python subscriber.py
