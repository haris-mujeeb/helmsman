#!/usr/bin/env python3
"""Hold-to-drive keyboard teleop for Helmsman.

A small pygame window captures the real keyboard state each frame, so the
robot moves only while a key is physically held and stops the instant it is
released. This avoids the latched behaviour of teleop_twist_keyboard (press
once, keep moving) and the auto-repeat guesswork a terminal would force.
Keep this window focused while driving.
"""

import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame


class HoldTeleop(Node):
    def __init__(self):
        super().__init__("keyboard_teleop")
        self.declare_parameter("linear_speed", 0.4)
        self.declare_parameter("angular_speed", 0.8)
        self.declare_parameter("publish_rate", 20.0)
        self.linear_speed = float(self.get_parameter("linear_speed").value)
        self.angular_speed = float(self.get_parameter("angular_speed").value)
        self.rate = float(self.get_parameter("publish_rate").value)
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)

    def publish(self, lin, ang):
        t = Twist()
        t.linear.x = lin
        t.angular.z = ang
        self.pub.publish(t)


# key -> (linear factor, angular factor)
KEYMAP = {
    pygame.K_w: (1.0, 0.0),
    pygame.K_s: (-1.0, 0.0),
    pygame.K_a: (0.0, 1.0),
    pygame.K_d: (0.0, -1.0),
    pygame.K_UP: (1.0, 0.0),
    pygame.K_DOWN: (-1.0, 0.0),
    pygame.K_LEFT: (0.0, 1.0),
    pygame.K_RIGHT: (0.0, -1.0),
}


def main():
    rclpy.init()
    node = HoldTeleop()

    # Init only display + font (skip audio, which has no device in the container).
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((430, 210))
    pygame.display.set_caption("Helmsman teleop - keep focused")
    font = pygame.font.SysFont("monospace", 18)
    clock = pygame.time.Clock()

    running = True
    while running and rclpy.ok():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Read the true physical key state every frame.
        pressed = pygame.key.get_pressed()
        lin = ang = 0.0
        for key, (lf, af) in KEYMAP.items():
            if pressed[key]:
                lin += lf * node.linear_speed
                ang += af * node.angular_speed

        node.publish(lin, ang)
        rclpy.spin_once(node, timeout_sec=0.0)

        screen.fill((25, 25, 28))
        lines = [
            "Hold to drive  (release = stop)",
            "W / S  or  Up / Down : forward / back",
            "A / D  or  Lft / Rgt : turn",
            f"linear   {lin:+.2f} m/s",
            f"angular  {ang:+.2f} rad/s",
            "ESC or close window to quit",
        ]
        for i, text in enumerate(lines):
            color = (0, 200, 150) if i == 0 else (210, 210, 210)
            screen.blit(font.render(text, True, color), (16, 16 + i * 30))
        pygame.display.flip()
        clock.tick(node.rate)

    node.publish(0.0, 0.0)  # final stop on the way out
    pygame.quit()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()