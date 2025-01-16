import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tty, termios,sys,select
settings = termios.tcgetattr(sys.stdin)
msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   q    w    e
   a    s    d
   z    x    c

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   Q    W    E
   A    S    D
   Z    X    C


anything else : stop

k/l or K/L: increase/decrease only linear speed by 10%
n/m or N/M: increase/decrease only angular speed by 10%

CTRL-C to quit
"""
e = """
Communications Failed
"""
MAX_LINEAR_SPEED = 5.0
MIN_LINEAR_SPEED = 0.1

MAX_ANGULAR_SPEED = 10.0
MIN_ANGULAR_SPEED = 0.1


class OmniTeleopKeyboard(Node):
    def __init__(self):
        super().__init__('omni_teleop_keyboard')
        print(msg)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.move()


    # 키 입력 받기
    def getkey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def current_vels(self,linear_speed,angular_speed):
        return "currently_speed: linear_speed {:.2f} \a ngular_speed {:.2f} ".format(linear_speed, angular_speed)

    def move(self):
        twist = Twist()

        linear_speed = 0.5
        angular_speed = 1.0
        x = 0
        y = 0
        z = 0
        theta = 0
        try:
            while(1):
                key = self.getkey()
                if key == 'w': # forward
                    x = 1
                elif key == 'a': # back
                    theta = 1
                elif key == 'd': # right rotation
                    theta = -1
                elif key == 'x': # left rotation
                    x = -1
                elif key == 'W': # forward
                    x = 1
                elif key == 'A': # side left
                    y = 1
                elif key == 'D': # side right
                    y = -1
                elif key == 'X': # back
                     x = -1
                elif key == 'q' or key == 'Q': # diagonal left forward
                    x = 1
                    y = 1
                elif key == 'e' or key == 'E': # diagonal right forward
                    x = 1
                    y = -1
                elif key == 'z' or key == 'Z': # diagonal left back
                    x = -1
                    y = 1
                elif key == 'c' or key == 'C': # diagonal right back
                    x = -1
                    y = -1
                elif key == 'k' or key == 'K': # decrease linear speed
                    linear_speed = linear_speed * 0.9
                    angular_speed = angular_speed * 1

                    print(self.current_vels(linear_speed,angular_speed))
                elif key == 'l' or key == 'L': # increase linear speed
                    linear_speed = linear_speed * 1.1
                    angular_speed = angular_speed * 1

                    print(self.current_vels(linear_speed,angular_speed))
                elif key == 'n' or key == 'N': # decrease angular speed
                    linear_speed = linear_speed * 1
                    angular_speed = angular_speed * 0.9

                    print(self.current_vels(linear_speed,angular_speed))
                elif key == 'm' or key == 'M': # increase angular speed
                    linear_speed = linear_speed * 1
                    angular_speed = angular_speed * 1.1

                    print(self.current_vels(linear_speed,angular_speed))
                else:
                    x = 0
                    y = 0
                    z = 0
                    theta = 0
                    if key == '\x03': # ctrl + c
                        break

                twist = Twist()
                twist.linear.x = x*linear_speed
                twist.linear.y = y*linear_speed
                twist.linear.z = z*linear_speed
                twist.angular.x = 0.0
                twist.angular.y = 0.0
                twist.angular.z = theta*angular_speed

                self.publisher_.publish(twist)
        except:
            print(e)
        finally:
            twist = Twist()
            twist.linear.x = x*linear_speed
            twist.linear.y = y*linear_speed
            twist.linear.z = z*linear_speed
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = theta*angular_speed

            self.publisher_.publish(twist)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


def main(args=None):
    rclpy.init(args=args)
    OmniTeleopKeyboard()

if __name__ == '__main__':
    main()