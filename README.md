# DevNet_3841
# Cisco Live DevNet Session DEVNET-3841 Code Repo


**"Project WhatsOp - A Messaging Platform for Network Devices"**


**WhatsOp**

The session will present a real-time messaging platform concept for network devices.
This platform will enable network engineers to approach network management using creative, new methods and automate common troubleshooting workflows.


**The Challenge:**
 - Slow time to respond to outages
 - Cost for creating, updating, troubleshooting and closing tickets

**The Goal:**
 - Automated detection of issues and tickets operations
 - Troubleshoot and configure the customer network directly from ServiceNow
 - Automate the collection of relevant info
 
**The Solution:**
 - Integration between Cisco IOS XE, Guest Shell, DNA Center, ServiceNow, PubNub, and Webex Teams

**Workflow:**
 "monitor_route.py"
 - EEM triggers execution when monitored route missing from routing table
 - Find the IOS XE device management IP address, Gi0/0 – Python CLI
 - Not the VPG IP address
 - Find the device hostname using RESTCONF 
 - Create a new ServiceNow incident - REST APIs
 - Get Cisco DNA Center Auth Token – REST APIs
 - Get device details, health and location from Cisco DNA Center - REST APIs
 - Update the ServiceNow incident - REST APIs
 - Will download pre-defined CLI commands from Cisco DNA Center - REST APIs
 - Execute each command and update ServiceNow incident - REST APIs
 - Identify if any configuration drifting from established baseline – Python CLI
 - Update ticket with changes and the engineer identity - REST APIs
 
 "subscriber_listener.py"
 - Use of PubNub Python SDK
 - Find out the IOS XE device management IP address and hostname
 - Initialize the PubNub channel and subscribe with the hostname as the PubNub “uuid”
 - Process messages as received
 - If the “device” value equals the device hostname execute commands
 - If the “device” value equals ”all” – execute commands
 - If not a match – ignore
 - The Ticket to be updated equals the value received
 - Commands output will update the ticket directly


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
