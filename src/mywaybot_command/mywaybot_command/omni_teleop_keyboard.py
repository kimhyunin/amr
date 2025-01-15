import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import tty, termios,sys,select
settings = termios.tcgetattr(sys.stdin)

class OmniTeleopKeyboard(Node):
    def __init__(self):
        super().__init__('omni_teleop_keyboard')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)
    
    # 키 입력 받기
    def getkey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def timer_callback(self):
        twist = Twist()
        
        linear_speed = 1.0
        angular_speed = 1.0
        x = 0
        y = 0
        z = 0
        theta = 0

        key = self.getkey()

        if key == 'w':
            x = 1
        else:
            x = 0
            y = 0
            z = 0
            theta = 0
        
        twist.linear.x = x*linear_speed
        twist.linear.y = y*linear_speed
        twist.linear.z = z*linear_speed
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = theta*angular_speed

        self.publisher_.publish(twist)





def main(args=None):
    rclpy.init(args=args)
    omni_teleop_keyboard = OmniTeleopKeyboard()
    rclpy.spin(omni_teleop_keyboard)
    omni_teleop_keyboard.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()