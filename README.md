# DevNet_3841
# Cisco Live DevNet Session DEVNET-3841 Code Repo


**"Project WhatsOp - A Messaging Platform for Network Devices"**


**WhatsOp**

The session will present a real-time messaging platform concept for network devices.
This platform will enable network engineers to approach network management using creative, new methods and automate common troubleshooting workflows.

---
The Challenge

The Goal

The Solution

The Results
Lower Mean Time to Repair
Lower cost of providing service to customer
---

**The Challenge:**
 - Slow time to respond to outages
 - Cost for creating, updating, troubleshooting and closing tickets

**The Goal:**
 - Automated detection of issues and tickets operations
 - Troubleshoot and configure the customer network directly from ServiceNow

**The Solution:**
 - Integration between Cisco IOS XE, Guest Shell, DNA Center, ServiceNow, PubNub, and Webex Teams

**Workflow:**
 - Embedded Event Manager will trigger execution of Python Script when condition match
  - collect device management IPv4 address
  - collect device details from Cisco DNA Center
  - create new incident
  - subscribe to PubNub channel to listen for CLI commands
  - execute received EXEC or Config mode commands and update the ServiceNow incident

**The Results:**
 - Lower Mean Time to Repair

**Setup and Configuration:**
 - The requirements.txt file include all the Python libraries needed for this application
 - This application requires:
   - Cisco DNA Center
   - IOS XE devices configured for NETCONF and RESTCONF, IOX and Guest Shell
   - Cisco Webex Teams account
   - ServiceNow developer account
   - PubNub developer account

**Cisco Products & Services:**

- Cisco DNA Center
- IOS XE Network Devices
- Webex Teams

**Other Platforms:**

- ServiceNow, PubNub


**License:**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
