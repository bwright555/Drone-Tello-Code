"""
Here we import the necessary modules.
Modules are essetntially libraries that allow us to utilize
certain chunks of code.
"""

import socket
import threading
import time

tello_address = ('192.168.10.1', 8889) # IP and port of Tello

local_address = ('', 9000) # IP and port of local computer

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #This sets up the UDP connection
sock.bind(local_address) #And this binds to the IP address and port of the computer

# Send the message to Tello and allow for a delay in seconds
def send(message, delay):
  #If the message is sending, we will see the results of the first print statement
    #If not, we will see the results of the error print statement
  try:
    sock.sendto(message.encode(), tello_address)
    print("Sending message: " + message)
  except Exception as e:
    print("Error sending: " + str(e))

  # Delay for a user-defined period of time
  time.sleep(delay)

# Receive the message from Tello
def receive():
  # Continuously loop and listen for incoming messages
  while True:
    # Try to receive the message otherwise print the exception
    try:
      response, ip_address = sock.recvfrom(128)
      print("Received message: " + response.decode(encoding='utf-8'))
    except Exception as e:
      # If there's an error close the socket and break out of the loop
      sock.close()
      print("Error receiving: " + str(e))
      break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming messages
receiveThread = threading.Thread(target=receive)
receiveThread.daemon = True
receiveThread.start()


#HERE IS WHERE YOU PUT THE CODE FOR THE MISSION

#Note, this current mission flies in a box formation

#First you can establish how far forward we are traveling and what the Yaw or turning angle will be, as well as its direction
forward_distance = 100
yaw_angle = 90
yaw_direction = "cw"

#FIRST TWO COMMANDS: WE NEED TO PUT IT IN COMMAND MODE AND HAVE IT TAKEOFF
send("command", 3)
send("takeoff", 5)


send("forward " + str(forward_distance), 4) #forward
send("cw " + str(yaw_angle), 3) #Turn right in place
send("forward " + str(forward_distance), 4) #forward
send("cw " + str(yaw_angle), 3) #Turn right in place
send("forward " + str(forward_distance), 4) #forward
send("cw " + str(yaw_angle), 3) #Turn right in place
send("forward " + str(forward_distance), 4) #forward
send("cw " + str(yaw_angle), 3) #Turn right in place

"""
As you can see, this mission is a simple box command. Follow the SDK commands and this format
of writing the code if you wish to send the drone on a different route
"""
#LAND
send("land", 5)

print("Mission complete")

# Close the socket
sock.close()