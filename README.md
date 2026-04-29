# Pub/Sub Automation Demo

A simple Publisher–Subscriber prototype built using Python standard libraries only.

## Overview

This project demonstrates:
- Publisher and Subscriber communication
- Subscribe / Unsubscribe behavior
- Event-driven notifications
- On-demand polling
- TCP socket communication
- Basic desktop UI using Tkinter

The implementation focuses on communication plumbing rather than UI styling.

---

## Architecture

- Publisher acts as a TCP socket server
- Subscriber acts as a TCP socket client
- Communication is implemented using raw Python sockets
- UI is implemented using Tkinter

---

## Features

### Publisher
- Connect button
- Disconnect button
- Connection state visualization
- Event broadcasting to subscribed clients

### Subscriber
- Subscribe button
- Unsubscribe button
- Check Status button
- Text box displaying received events and polling results

---

## Event Behavior

- Events are delivered only when Subscriber is subscribed
- No events are received in unsubscribed mode
- Status polling occurs only when "Check Status" is pressed
- No background polling is implemented

---

## Run the Application

Run both applications:

```bash
python main.py
```
## Or run separately:
```bash
python publisher.py
python subscriber.py
