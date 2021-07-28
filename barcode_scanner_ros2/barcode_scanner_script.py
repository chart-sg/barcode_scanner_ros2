#!/usr/bin/env python3

import rclpy
import time
import os
import sys
from rclpy.node import Node
from std_msgs.msg import String
from evdev import InputDevice, ecodes, list_devices
from select import select


class BarcodeReader(Node):

    def __init__(self):
        super().__init__('barcode_reader')
        self.get_logger().info("Reading parameters")
        self.key_mapping = "XX1234567890-=XXqwertyuiop[]XXasdfghjkl:'XX\zxcvbnm,./XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        try:
            self.declare_parameter("input_port")
            self.input = self.get_parameter_or("input_port")
            self.dev = InputDevice(self.input.value)
            # self.declare_parameter("key_mapping")
            # self.keys = self.get_paramter_or("key_mapping")
            # self.get_logger().info("Successfully loaded parameters from param file")
        except:
            self.get_logger().info("Error loading from param file!! Setting to system determined InputDevice")
            self.input = self.getInputPortName()
            self.dev = InputDevice(self.input)
            self.get_logger().info("Successfully loaded input device as '%s'" %self.input)
            # self.keys = "XX1234567890-=XXqwertyuiop[]XXasdfghjkl:'XX\zxcvbnm,./XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            # self.get_logger().info("Successfully loaded default keys")
            pass
        self.barcode = ""
        self.msg = String()
        self.msg.data = ""
        self.publisher_ = self.create_publisher(String, 'barcode_last_scan', 10)
        timer_track_event_period = 0.1  # seconds
        timer_publish_period = 5  # seconds
        self.timer_track_event = self.create_timer(timer_track_event_period, self.timer_track_event_callback)
        self.timer_publish_event = self.create_timer(timer_publish_period, self.timer_publish_callback)
        self.CapsOn = False

    def timer_publish_callback(self):
        """Periodic callback method to update the FM with the latest Barcode scan"""
        #self.msg.header.stamp.sec = int(time.time())
        self.publisher_.publish(self.msg)
        # self.get_logger().info('[Periodic Update] Publishing: "%s"' % self.msg.data)


    def timer_track_event_callback(self):
        """Event based callback method to update the FM when the new Barcode is scanned"""
        # self.get_logger().info("Checking if any card event found")
        try:
            read,write,execute = select([self.dev], [], [], 0.5)
            for event in self.dev.read():
                # print(events)
                """To sieve out the irrelevant event signals"""
                if (event.type != 1 or event.value != 1):
                    continue
                """To determine the end event signal"""
                if event.code == 28:
                    """ROS Publisher"""
                    self.msg.data = self.barcode
                    self.publisher_.publish(self.msg)
                    self.get_logger().info('[Event Based Update] Publishing: "%s"' % self.msg.data)
                    self.barcode = ""
                    break
                """To determine if a shift key stroke is trigger and register action for next event"""
                if (event.code == 42 or event.code == 54):
                    self.CapsOn = True
                    continue
                eventchar = self.key_mapping[event.code]
                """Set alphabet to caps if shift key stroke was triggered"""
                if self.CapsOn:
                    eventchar = eventchar.upper()
                    self.CapsOn = False
                """Appending the char to the barcode string"""
                self.barcode += eventchar
        except BlockingIOError:
            pass

    def getInputPortName(self):
        self.get_logger().info("Obtaining Barcode Scanner Input Port Name...")
        root_path = "/dev/input/by-id/"
        os.chdir(root_path)
        event_list = os.listdir('.')
        dev_event_id = [name for name in event_list if 'usb-Datalogic' in name]
        if len(dev_event_id) == 0:
            self.get_logger().info("Required device not found, please ensure device is properly connected")
            sys.exit(1)
        return (root_path + dev_event_id[0])


def main(args=None):
    rclpy.init(args=args)

    print("Running Barcode reader script")
    barcode_reader = BarcodeReader()

    rclpy.spin(barcode_reader)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    barcode_reader.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
